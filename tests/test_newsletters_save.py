"""SAVE 알림 단신 → 같은 5개 카테고리 파일 (2026-11-20 개편). 네트워크·실제 메일 없이 검사."""
import importlib.util
import json
import sys
import types
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import yaml

ROOT = Path(__file__).resolve().parents[1]
pkg = types.ModuleType("ytflow"); pkg.__path__ = []
sys.modules.setdefault("ytflow", pkg)
cfg = types.ModuleType("ytflow.config"); cfg.ROOT = ROOT
sys.modules.setdefault("ytflow.config", cfg)
stages = types.ModuleType("ytflow.stages"); stages.__path__ = []
sys.modules.setdefault("ytflow.stages", stages)
spec = importlib.util.spec_from_file_location("ytflow.stages.newsletters", ROOT / "ytflow/stages/newsletters.py")
n = importlib.util.module_from_spec(spec); spec.loader.exec_module(n)

C = yaml.safe_load((ROOT / "config/newsletters.yaml").read_text(encoding="utf-8"))
PERSONAL = "s99078634@gmail.com"


def save_msg(body, date="2026-11-20T17:18:42+09:00", mid="private-message-id"):
    # 보낸 사람은 병인 님 본인 주소 — 제목만으로 알아봐야 한다
    return {"id": mid, "sender": PERSONAL, "subject": "[save알림]", "body": body, "date": date}


class SaveConfigTests(unittest.TestCase):
    def test_source_registered_as_headline(self):
        s = next(x for x in C["sources"] if x["id"] == "save")
        self.assertTrue(s.get("headline"))
        self.assertFalse(s.get("match"))                      # 보낸 사람 주소는 저장소에 두지 않는다
        self.assertEqual({"market", "ai", "curiosity", "history", "issues"}, set(s["brands"]))

    def test_recognised_by_subject_only(self):
        src = n.which(save_msg("헤드라인 한 줄입니다"), C)
        self.assertEqual("save", (src or {}).get("id"))

    def test_noise_and_other_mail_ignored(self):
        self.assertIsNone(n.which({**save_msg("x"), "subject": "오늘의 뉴스레터"}, C))


class SaveHeadlineTests(unittest.TestCase):
    def items(self, *lines):
        body = "\n".join(lines)
        with patch.object(n.urllib.request, "urlopen", side_effect=AssertionError("HTTP forbidden")) as http:
            out = n.items_from(save_msg(body), C, do_resolve=False)
            http.assert_not_called()
        return out

    def test_template_cut_and_no_url(self):
        out = self.items("[app_name] | [notification_title] | 앤트로픽 IPO 효과 실종…글로벌 AI 관련주 매도세 확산")
        self.assertEqual(1, len(out))
        self.assertEqual("앤트로픽 IPO 효과 실종…글로벌 AI 관련주 매도세 확산", out[0]["title"])
        self.assertEqual("", out[0]["url"])
        self.assertEqual("11-20 17:18", out[0]["alarm"])
        self.assertIn(out[0]["brand"], n.BRANDS)
        self.assertEqual("SAVE 알림 (오선 단신)", out[0]["source_name"])

    def test_empty_template_line_skipped(self):
        self.assertEqual([], self.items("[app_name] | [notification_title] |"))

    def test_categories_by_words(self):
        cases = {
            "[app_name] | [notification_title] | 미국 증시, 정규장 개장 직후 변동성 급증…새로운 위험 요인 부상": "market",
            "[app_name] | [notification_title] | 금일 백악관 일정": "issues",
            "[app_name] | [notification_title] | 모건스탠리 “통신사들, AI 에이전트로 경쟁사 전략 예측”": "ai",
            "[app_name] | [notification_title] | 중세 왕조의 몰락을 둘러싼 새로운 발굴": "history",
            "[app_name] | [notification_title] | 수면 부족이 도파민 보상 회로에 미치는 영향": "curiosity",
        }
        for line, want in cases.items():
            with self.subTest(want=want):
                self.assertEqual(want, self.items(line)[0]["brand"])
        # 낱말이 없으면 시장 (SAVE 기본값 — config 의 brands 첫 칸)
        self.assertEqual("market", self.items("[app_name] | [notification_title] | SAVE 장 전 리포트｜26년 11월 20일 (금)")[0]["brand"])


class SaveStoreTests(unittest.TestCase):
    def test_distinct_headlines_kept_same_day(self):
        a = "[app_name] | [notification_title] | 첫 번째 소식 제목입니다"
        b = "[app_name] | [notification_title] | 두 번째 소식 제목입니다"
        with TemporaryDirectory() as d, patch.object(n, "OUT", Path(d)):
            n.ingest_messages([save_msg(a)], C, do_resolve=False)
            n.ingest_messages([save_msg(b, date="2026-11-20T18:03:20+09:00", mid="other-id")], C, do_resolve=False)
            day = n._load("20261121")                                   # 17시 이후 → 다음 날 파일
            self.assertEqual(2, len(day["items"]))
            self.assertTrue(all(x["url"] == "" for x in day["items"]))
            # 같은 소식이 다시 와도 한 번만 (메일 자체는 읽음 기록으로 남는다)
            n.ingest_messages([save_msg(a, mid="third-id")], C, do_resolve=False)
            self.assertEqual(2, len(n._load("20261121")["items"]))
            self.assertEqual(3, len(n._load("20261121")["messages"]))

    def test_md_has_no_empty_link_and_keeps_time_and_privacy(self):
        body = "[app_name] | [notification_title] | 미국 증시, 정규장 개장 직후 변동성 급증…새로운 위험 요인 부상"
        with TemporaryDirectory() as d, patch.object(n, "OUT", Path(d)):
            n.ingest_messages([save_msg(body)], C, do_resolve=False)
            md = Path(d, "20261121.md").read_text(encoding="utf-8")
            js = Path(d, "20261121.json").read_text(encoding="utf-8")
        self.assertIn("미국 증시, 정규장 개장 직후 변동성 급증", md)
        self.assertIn("(알림 11-20 17:18)", md)
        self.assertNotRegex(md, r"\]\(\s*\)")                            # 빈 링크 괄호 금지
        self.assertNotIn("](", md.split("새로운 위험 요인")[1].split("\n")[0])  # 그 행은 링크가 없다
        self.assertIn("## 시장", md)
        for text in (md, js):
            self.assertNotIn(PERSONAL, text)
            self.assertNotIn("private-message-id", text)                 # 메일 ID 는 해시로만
        self.assertIn(n.message_key("private-message-id"), js)
        self.assertEqual("", json.loads(js)["items"][0]["url"])

    def test_section_and_show_render_without_url(self):
        it = {"title": "금일 백악관 일정", "url": "", "kind": "news", "reuse": n.NO_LINK_REUSE,
              "brand": "issues", "source": "save", "source_name": "SAVE 알림 (오선 단신)",
              "msg": "h", "date": "2026-11-20T19:03:40+09:00", "alarm": "11-20 19:03"}
        with TemporaryDirectory() as d, patch.object(n, "OUT", Path(d)):
            n._save({"day": "20261121", "messages": [], "items": [it]})
            sec = n.section(("issues",), "2026-11-21")
        self.assertIn("금일 백악관 일정 — SAVE 알림 (오선 단신) (알림 11-20 19:03)", sec)
        self.assertNotIn("· \n", sec)
        self.assertNotIn("]( ", sec)


if __name__ == "__main__":
    unittest.main()
