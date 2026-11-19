"""Adapt Gmail connector exports to the newsletter index without storing mail in Git."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timedelta, timezone
from email.utils import parseaddr
from html.parser import HTMLParser
from pathlib import Path

from . import newsletters


class ArticleLinks(HTMLParser):
    """Extract visible anchor text for HTML-only newsletters without loading the page."""

    def __init__(self) -> None:
        super().__init__()
        self.href = ""
        self.title: list[str] = []
        self.lines: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self.href = dict(attrs).get("href") or ""
            self.title.clear()

    def handle_data(self, data):
        if self.href:
            self.title.append(data)

    def handle_endtag(self, tag):
        if tag == "a" and self.href:
            title = " ".join("".join(self.title).split()).replace("[", "(").replace("]", ")")
            if title and self.href.startswith(("https://", "http://")):
                self.lines.append(f"[{title}]({self.href})")
            self.href = ""


def gmail_query(config: dict) -> str:
    senders = sorted({sender for source in config["sources"] if source.get("status") != "blocked"
                      for sender in source.get("match", [])})
    terms = " ".join(f'from:"{sender}"' for sender in senders)
    return f'newer_than:2d in:anywhere -in:trash -in:sent {{label:뉴스레터 {terms}}}'


def sender_matches(sender: str, matchers: list[str]) -> bool:
    local, separator, domain = sender.lower().rpartition("@")
    if not separator:
        return False
    for matcher in matchers:
        matcher = matcher.lower()
        if "@" in matcher and sender.lower() == matcher:
            return True
        if "." in matcher and (domain == matcher or domain.endswith("." + matcher)):
            return True
        if "." not in matcher and (domain.split(".")[0] == matcher or
                                   (domain == "substack.com" and local.split("+")[0] == matcher)):
            return True
    return False


def ingest_exports(directory: Path, config: dict, label_id: str) -> dict:
    messages, label_ids = [], []
    counts = {"candidates": 0, "unknown": 0, "no_public_links": 0, "first_issues": []}
    days = [newsletters._load(p.stem) for p in newsletters.OUT.glob("*.json")]
    seen = {m["id"] for day in days for m in day["messages"]}
    seen_sources = {item["source"] for day in days for item in day["items"] if item.get("msg") != "rss"}
    cutoff = datetime.now(timezone.utc) - timedelta(days=2)
    for path in sorted(directory.glob("*.json")):
        mail = json.loads(path.read_text(encoding="utf-8-sig"))
        counts["candidates"] += 1
        labels = set(mail.get("labels", []))
        source_msg_id = mail["id"]
        received = datetime.fromtimestamp(int(mail["internal_date"]) / 1000, timezone.utc)
        if received < cutoff:
            continue
        sender = parseaddr(mail["sender"])[1]
        message = {"id": source_msg_id, "sender": sender, "subject": mail["subject"], "date": received.isoformat()}
        source = newsletters.which(message, config)
        if not source or source.get("status") == "blocked" or not sender_matches(sender, source["match"]):
            counts["unknown"] += label_id in labels
            continue
        if newsletters.NOISE_SUBJ.search(message["subject"]):
            continue
        if label_id not in labels and not mail.get("bulk"):
            continue
        if {source_msg_id, newsletters.message_key(source_msg_id)}.isdisjoint(seen):
            message["body"] = mail.get("plain") or ""
            if not message["body"] and mail.get("html"):
                links = ArticleLinks()
                links.feed(mail["html"])
                message["body"] = "\n".join(links.lines)
            if not newsletters.items_from(message, config, do_resolve=False):
                counts["no_public_links"] += 1
                continue
            messages.append(message)
            if source["id"] not in seen_sources and (source.get("status") == "planned" or source["id"] == "tldr-tech"):
                counts["first_issues"].append(source["id"])
                seen_sources.add(source["id"])
        if label_id not in labels or {"INBOX", "SPAM"}.intersection(labels):
            label_ids.append(source_msg_id)
    newsletters.ingest_messages(messages, config, do_resolve=False)
    return {**counts, "new_messages": len(messages), "label_message_ids": label_ids}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("query")
    ingest = commands.add_parser("ingest")
    ingest.add_argument("directory", type=Path)
    ingest.add_argument("summary", type=Path)
    ingest.add_argument("label_id")
    args = parser.parse_args()
    config = newsletters.cfg()
    if args.command == "query":
        print(gmail_query(config))
    else:
        summary = ingest_exports(args.directory, config, args.label_id)
        args.summary.write_text(json.dumps(summary), encoding="utf-8")


if __name__ == "__main__":
    main()
