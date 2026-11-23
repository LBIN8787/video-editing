"""Axios 클릭 주소 로컬 해독과 TLDR 평문 각주 제목 — 네트워크 없이 도는 단위 테스트.

Axios AM·Markets 는 평문 본문 없이 HTML 만 오고, 모든 링크가
    https://link.axios.com/click/<캠페인>/<목적지 base64url>/<해시>
형식이다(2026-11-24 확인). 앞 숫자 묶음은 캠페인·수신자 번호라 해독만 하고 버린다.

TLDR 평문 본문은 `제목 (5 MINUTE READ) [7]` … 끝에 `[7] https://…` 로 오기 때문에,
맨주소 줄의 제목이 각주 번호뿐이면 위쪽에서 같은 번호를 단 줄을 제목으로 쓴다.

모든 주소·번호는 가짜 값이다.
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

PREFIX = "12345678.987654"      # 캠페인 번호 자리의 가짜 값
TAIL = "6af990d0c7478af88d083a3cBb6459546"   # 해시 자리의 가짜 값


def axios(dest: str, tail: str = TAIL, pad: bool = False) -> str:
    t = base64.urlsafe_b64encode(dest.encode("utf-8")).decode()
    if not pad:
        t = t.rstrip("=")
    return f"https://link.axios.com/click/{PREFIX}/{t}/{tail}"


C = {"sources": [{"match": ["example.test"], "id": "test", "name": "Test", "brands": ["ai"]}],
     "links": {"primary": [], "data": [], "media": []}, "reuse": {}, "skip": ["unsubscribe"], "route": {}}


def msg(body: str) -> dict:
    return {"sender": "news@example.test", "subject": "Daily stories", "body": body,
            "date": "2026-11-24T02:00:00+09:00", "id": "m1"}


class AxiosUnwrapTests(unittest.TestCase):
    def test_click_link_decoded(self):
        self.assertEqual("https://www.axios.com/2026/11/23/story",
                         n.unwrap(axios("https://www.axios.com/2026/11/23/story")))

    def test_campaign_params_stripped(self):
        dest = "https://www.axios.com/2026/11/23/story?utm_source=newsletter&utm_medium=email&id=7"
        self.assertEqual("https://www.axios.com/2026/11/23/story?id=7", n.unwrap(axios(dest)))

    def test_padding_and_base64url_chars(self):
        dest = "https://www.axios.com/a?q=한글~"
        for pad in (False, True):
            with self.subTest(pad=pad):
                self.assertEqual("https://www.axios.com/a?q=%ED%95%9C%EA%B8%80~",
                                 n.unwrap(axios(dest, pad=pad)))

    def test_other_hosts_untouched(self):
        for url in ("https://link.axios.com/other/123/abc", "https://example.test/article",
                    "https://event.stibee.com/v2/click/ABC"):
            with self.subTest(url=url):
                self.assertEqual(url, n.unwrap(url))

    def test_payload_that_is_not_a_web_address_untouched(self):
        wrapped = axios("not a url")
        self.assertEqual(wrapped, n.unwrap(wrapped))

    def test_idempotent(self):
        once = n.unwrap(axios("https://www.axios.com/2026/11/23/story"))
        self.assertEqual(once, n.unwrap(once))

    def test_per_campaign_prefix_not_published(self):
        out = n.items_from(msg(f"[A long enough headline]({axios('https://www.axios.com/2026/11/23/story')})"), C)
        self.assertEqual(1, len(out))
        self.assertEqual("https://www.axios.com/2026/11/23/story", out[0]["url"])

    def test_no_network(self):
        with patch.object(n.urllib.request, "urlopen", side_effect=AssertionError("HTTP forbidden")) as http:
            n.unwrap(axios("https://www.axios.com/2026/11/23/story"))
            n.items_from(msg(f"[A long enough headline]({axios('https://www.axios.com/2026/11/23/story')})"), C)
            http.assert_not_called()


class FootnoteTitleTests(unittest.TestCase):
    BODY = ("ANTHROPIC MATHEMATICIAN SAYS AI HAS SOLVED A FAMOUS PROBLEM (5 MINUTE READ) [7]\n"
            "\n"
            " A short summary line of the story. \n"
            "\n"
            "TESLA LAUNCHES A NEW DRIVING STACK, FROM SIGNS TO POTHOLES (10 MINUTE READ) [8]\n"
            "\n"
            " Another summary. \n"
            "\n"
            "[7] https://publisher.test/riemann?utm_source=tldrnewsletter\n"
            "[8] https://publisher.test/tesla?utm_source=tldrnewsletter\n")

    def test_bare_url_title_from_footnote_marker(self):
        out = n.items_from(msg(self.BODY), C)
        self.assertEqual(["https://publisher.test/riemann", "https://publisher.test/tesla"],
                         [it["url"] for it in out])
        self.assertEqual("ANTHROPIC MATHEMATICIAN SAYS AI HAS SOLVED A FAMOUS PROBLEM",
                         out[0]["title"])
        self.assertEqual("TESLA LAUNCHES A NEW DRIVING STACK, FROM SIGNS TO POTHOLES",
                         out[1]["title"])

    def test_reference_list_line_is_not_used_as_title(self):
        body = "[7] https://publisher.test/one\n[7] https://publisher.test/two\n"
        out = n.items_from(msg(body), C)
        self.assertEqual([], [it for it in out if len(it["title"]) > 6])


class TrailingQuoteTests(unittest.TestCase):
    """메일 본문에 드물게 따라붙는 따옴표 — 주소에 남기면 추적 주소 심사를 빠져나간다."""

    def test_markdown_link_trailing_quote(self):
        out = n.items_from(msg("[An interesting story](https://publisher.test/article')"), C)
        self.assertEqual(["https://publisher.test/article"], [it["url"] for it in out])

    def test_stibee_wrapped_with_trailing_quote_still_decoded(self):
        dest = "https://n.publisher.test/article/032/0003484332"
        body = f"[약 6만4000가구]({axios(dest)}') "
        out = n.items_from(msg(body), C)
        self.assertEqual([dest], [it["url"] for it in out])
        self.assertNotIn("link.axios.com", out[0]["url"])


if __name__ == "__main__":
    unittest.main()
