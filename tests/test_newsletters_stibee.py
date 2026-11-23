"""Stibee(스티비) 클릭 추적 주소를 네트워크 없이 해독하는지 — 로컬 base64 단위 테스트.

어피티 머니레터·미라클레터가 쓰는 형식:
    https://event.stibee.com/v2/click/<수신자 묶음 base64>/<목적지 base64url>
앞 묶음은 구독자·캠페인 번호라 해독만 하고 버린다. 실제 수신자 번호는 넣지 않는다(모두 가짜 값).
"""
import base64
import importlib.util
import sys
import types
import unittest
from pathlib import Path
from unittest.mock import patch

pkg = types.ModuleType("ytflow")
pkg.__path__ = []
sys.modules.setdefault("ytflow", pkg)
cfg = types.ModuleType("ytflow.config")
cfg.ROOT = Path(".")
sys.modules.setdefault("ytflow.config", cfg)
stages = types.ModuleType("ytflow.stages")
stages.__path__ = []
sys.modules.setdefault("ytflow.stages", stages)
spec = importlib.util.spec_from_file_location(
    "ytflow.stages.newsletters", Path(__file__).resolve().parents[1] / "ytflow" / "stages" / "newsletters.py")
n = importlib.util.module_from_spec(spec)
spec.loader.exec_module(n)

# 40802/3714674/803189/ 같은 수신자·캠페인 묶음 자리의 가짜 값
PREFIX = "MTIzNDUvNjc4OTAvMTIzNDU2Lw"


def stibee(dest: str, prefix: str = PREFIX, pad: bool = False) -> str:
    t = base64.urlsafe_b64encode(dest.encode("utf-8")).decode()
    if not pad:
        t = t.rstrip("=")
    return f"https://event.stibee.com/v2/click/{prefix}/{t}"


C = {"sources": [{"match": ["example.test"], "id": "test", "name": "Test", "brands": ["ai"]}],
     "links": {"primary": [], "data": [], "media": []}, "reuse": {}, "skip": ["list-manage.com"], "route": {}}


def msg(body: str) -> dict:
    return {"sender": "news@example.test", "subject": "Daily stories", "body": body,
            "date": "2026-11-23T06:00:00+09:00", "id": "m1"}


class StibeeUnwrapTests(unittest.TestCase):
    def test_click_link_decoded(self):
        self.assertEqual("https://publisher.test/article?id=42",
                         n.unwrap(stibee("https://publisher.test/article?id=42")))

    def test_campaign_params_stripped(self):
        dest = "https://publisher.test/story?utm_source=newsletter&utm_medium=email&id=7&ref=mail"
        self.assertEqual("https://publisher.test/story?id=7", n.unwrap(stibee(dest)))

    def test_padding_and_base64url_chars(self):
        dest = "https://publisher.test/a?q=한글 값~"
        for pad in (False, True):
            with self.subTest(pad=pad):
                self.assertEqual("https://publisher.test/a?q=%ED%95%9C%EA%B8%80+%EA%B0%92~",
                                 n.unwrap(stibee(dest, pad=pad)))

    def test_trailing_slash_and_trailing_path(self):
        self.assertEqual("https://publisher.test/x", n.unwrap(stibee("https://publisher.test/x") + "/"))
        wrapped = stibee("https://publisher.test/x") + "/extra"
        self.assertEqual(wrapped, n.unwrap(wrapped))   # 모르는 형식은 손대지 않는다

    def test_open_pixel_untouched(self):
        url = f"https://event.stibee.com/v2/open/{PREFIX}"
        self.assertEqual(url, n.unwrap(url))

    def test_payload_that_is_not_a_web_address_untouched(self):
        for dest in ("ftp://publisher.test/file", "not a url", ""):
            wrapped = stibee(dest) if dest else f"https://event.stibee.com/v2/click/{PREFIX}/%%%"
            with self.subTest(dest=dest):
                self.assertEqual(wrapped, n.unwrap(wrapped))

    def test_idempotent(self):
        once = n.unwrap(stibee("https://publisher.test/article"))
        self.assertEqual(once, n.unwrap(once))

    def test_no_network(self):
        with patch.object(n.urllib.request, "urlopen", side_effect=AssertionError("HTTP forbidden")) as http:
            n.unwrap(stibee("https://publisher.test/article"))
            n.items_from(msg(f"[A long enough headline]({stibee('https://publisher.test/article')})"), C)
            http.assert_not_called()


class StibeeIngestTests(unittest.TestCase):
    def test_markdown_label_kept_and_url_decoded(self):
        body = f"오늘의 시장: [증시 급락 이유 정리]({stibee('https://publisher.test/story?utm_source=email')})"
        self.assertEqual([("증시 급락 이유 정리", stibee("https://publisher.test/story?utm_source=email"))], n.extract(body))
        out = n.items_from(msg(body), C)
        self.assertEqual(1, len(out))
        self.assertEqual("증시 급락 이유 정리", out[0]["title"])
        self.assertEqual("https://publisher.test/story", out[0]["url"])

    def test_short_korean_label_kept(self):
        body = f"[사이드카]({stibee('https://publisher.test/sidecar')})"
        out = n.items_from(msg(body), C)
        self.assertEqual(["사이드카"], [it["title"] for it in out])

    def test_markdown_link_not_duplicated(self):
        body = f"오늘의 시장: [증시 급락 이유 정리]({stibee('https://publisher.test/story')})"
        self.assertEqual(1, len(n.extract(body)))
        self.assertEqual(1, len(n.items_from(msg(body), C)))

    def test_management_link_hidden_inside_wrapper_dropped(self):
        cases = [("Unsubscribe", "https://page.stibee.com/unsubscribe/40802?token=abc"),
                 ("이메일 변경", "https://page.stibee.com/subscribers/auth/40802"),
                 ("구독 해지", "https://page.stibee.com/unsubscribe/40802")]
        for label, dest in cases:
            with self.subTest(label=label):
                body = f"[{label}]({stibee(dest)})"
                self.assertEqual([], n.items_from(msg(body), C))
                self.assertEqual([], n.items_from(msg(body + f"\n[긴 제목의 기사 하나]({stibee(dest)})"), C)[1:])

    def test_per_recipient_prefix_not_published(self):
        out = n.items_from(msg(f"[A long enough headline]({stibee('https://publisher.test/article')})"), C)
        self.assertNotIn("event.stibee.com", out[0]["url"])
        self.assertNotIn(PREFIX, out[0]["url"])


if __name__ == "__main__":
    unittest.main()
