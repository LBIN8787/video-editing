"""원본 영상 권리별 규칙 (manual/09 §3-5 v80): 공공·공식은 길이 제한 없음, 방송사는 20초/60초, 신고·경고 권리자는 받지 않음."""
from ytflow.stages import cliplane


def test_blocked_by_strike_and_claim():
    bl = {"claim": ["bloomberg"], "strike": ["cnbc"], "until": ""}
    assert "경고" in cliplane.blocked({"credit": "CNBC Television", "rights": "broadcast"}, bl)
    assert "Content ID" in cliplane.blocked({"url": "https://youtube.com/@BloombergTV", "rights": "broadcast"}, bl)
    assert cliplane.blocked({"credit": "Federal Reserve", "rights": "public"}, bl) == ""


def test_active_strike_blocks_broadcast_only():
    bl = {"claim": [], "strike": [], "until": "2026-12-31"}
    assert cliplane.blocked({"credit": "Fox Business", "rights": "broadcast"}, bl, today="2026-11-21")
    assert cliplane.blocked({"credit": "NVIDIA", "rights": "official"}, bl, today="2026-11-21") == ""
    assert cliplane.blocked({"credit": "Fox Business", "rights": "broadcast"}, bl, today="2027-01-02") == ""
