"""Offline regression tests: no real subscriber links, HTTP, or mail."""
import importlib.util
import sys
import types
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

# Isolated source loading avoids unrelated runtime dependencies.
pkg = types.ModuleType("ytflow")
pkg.__path__ = []
sys.modules.setdefault("ytflow", pkg)
cfg = types.ModuleType("ytflow.config")
cfg.ROOT = Path(".")
sys.modules.setdefault("ytflow.config", cfg)
stages = types.ModuleType("ytflow.stages")
stages.__path__ = []
sys.modules.setdefault("ytflow.stages", stages)
source = Path(__file__).with_name("newsletters.py")
if not source.exists():
    source = Path(__file__).parents[1] / "ytflow/stages/newsletters.py"
spec = importlib.util.spec_from_file_location("ytflow.stages.newsletters", source)
n = importlib.util.module_from_spec(spec)
spec.loader.exec_module(n)

C = {"sources":[{"match":["example.test"],"id":"test","name":"Test","brands":["ai"]}],
     "links":{"primary":[],"data":[],"media":[]}, "reuse":{}, "skip":["unsubscribe"], "route":{}}
def msg(body):
    return {"sender":"news@example.test","subject":"Daily stories","body":body,"date":"2026-11-15T00:00:00Z"}

class SecurityTests(unittest.TestCase):
    def extract(self, body, mode=True):
        with patch.object(n.urllib.request, "urlopen", side_effect=AssertionError("HTTP forbidden")) as http:
            result = n.items_from(msg(body), C, do_resolve=mode)
            http.assert_not_called()
            return result

    def test_management_zero_requests(self):
        for mode in (True,False):
            for label,url in [
                ("Unsubscribe now","https://click.example.test/opaque"),
                ("Manage preferences","https://example.test/some-link"),
                ("An interesting story","https://click.example.test/unsubscribe/abc"),
                ("An interesting story","https://example.test/%75nsubscribe")]:
                self.assertEqual([], self.extract(f"[{label}]({url})",mode))

    def test_opaque_not_requested_or_published(self):
        for mode in (True,False):
            self.assertEqual([],self.extract("[An interesting story](https://click.example.test/opaque-personal-id)",mode))

    def test_direct_article(self):
        out=self.extract("[An interesting story](https://publisher.test/article?utm_source=email)")
        self.assertEqual(out[0]["url"],"https://publisher.test/article")

    def test_offline_unwrap(self):
        out=self.extract("[An interesting story](https://click.example.test/redirect/article?url=https%3A%2F%2Fpublisher.test%2Farticle)")
        self.assertEqual(out[0]["url"],"https://publisher.test/article")

    def test_private_queries_and_paths_not_published(self):
        for suffix in ("?token=private","?email=person%40example.test","?opaque=private","/"+"a"*60):
            self.assertEqual([],self.extract("[An interesting story](https://publisher.test/article"+suffix+")"))

    def test_unwrapped_management_rejected(self):
        self.assertEqual([],self.extract("[An interesting story](https://click.example.test/redirect/article?url=https%3A%2F%2Fpublisher.test%2Funsubscribe)"))

    def test_ingest_keeps_only_source_and_hashed_message_id(self):
        message = msg("[An interesting story](https://publisher.test/article)")
        message["id"] = "private-message-id"
        with TemporaryDirectory() as directory, patch.object(n, "OUT", Path(directory)):
            n.ingest_messages([message], C, do_resolve=False)
            self.assertEqual([], n.ingest_messages([message], C, do_resolve=False))
            index = n._load(n.video_day(message["date"]))
            self.assertEqual([{"id": n.message_key(message["id"]), "source": "test", "date": message["date"]}],
                             index["messages"])
            self.assertEqual(index["messages"][0]["id"], index["items"][0]["msg"])

    def test_resolve_helper_has_no_network(self):
        with patch.object(n.urllib.request,"urlopen",side_effect=AssertionError("HTTP forbidden")) as http:
            n.resolve("https://click.example.test/opaque")
            http.assert_not_called()

if __name__=="__main__":
    unittest.main()
