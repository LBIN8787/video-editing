"""판테온 편 v2 장면 명세: beats_v2.json(← beats.py script_v2.md) + 아래 표 → pantheon_v2.json (render_full.py 의 SPEC, 화면 pantheon_v2_overlay.html).
art: shots [그림, kw 번호(-1 = 처음부터), 카메라, 위 띠 글] (v1 과 같음).
dome: 돔 단면 모션그래픽(실제 비율 1m=14px) — 같은 단면이 박자마다 고쳐 지어짐. dome={요소: kw 번호}, pre=[그림, kw] 그 낱말 전까지 삽화, post=[그림, kw, 글] 그 낱말부터 삽화, labels=[[글, kw]].
그림: v1 시트(garage·dome·struct·rust·lab·history·end) + v2 시트(build1·build2·build3·lime — 지우가 짓는 과정, art_sheets_v2.json), 실제 사진 photo_* (Wikimedia Commons, Sonse · CC BY 2.0).
python make_spec_v2.py"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
P = {
 1: dict(mg="art", shots=[["garage_tl", -1, "in"], ["garage_tr", 0, "in"]], kw=["지은 지"]),
 2: dict(mg="art", shots=[["garage_tr", -1, "out"], ["garage_bl", 0, "in", "로마 · 비 오는 날"]], kw=["지금 로마에"]),
 3: dict(mg="art", shots=[["garage_br", -1, "in"], ["dome_tl", 0, "in"]], kw=["천장 한가운데가"]),
 4: dict(mg="art", shots=[["photo_dome", -1, "in", "콘크리트로 부어 만든 돔"], ["photo_dome", 0, "in", "철근 0가닥"], ["dome_br", 1, "in", "약 1,900년"]],
         kw=["철근은", "그리고 약"]),
 5: dict(mg="art", shots=[["dome_bl", -1, "in"]], think="우리 주차장은 몇십 년 만에…", thinkk=0, kw=["'우리 주차장은"]),
 6: dict(mg="words", head="", lines=[["금이 가지 않아서 버틴 게 아니다", 0], ["금이 가도 무너지지 않게 지었다", 1], ["직접 지어 보기", 2]],
         kw=["금이 가지 않아서", "금이 가도", "어떻게 지었는지"]),
 7: dict(mg="art", shots=[["build1_tr", -1, "in", "1,900년 전 로마의 건축가"], ["build1_tr", 0, "in", "숙제: 철근 없이, 콘크리트만으로"]], kw=["숙제는"]),
 8: dict(mg="dome", pre=["build1_tl", 0], dome=dict(buses=0, apt=1, ball=2), kw=["시내버스", "아파트로", "커다란 공"]),
 9: dict(mg="art", shots=[["build1_tr", -1, "out", "시도 1"], ["build1_bl", 0, "in", "같은 두께로, 고르게"]], kw=["둥근 틀을"]),
 10: dict(mg="dome", pre=["build1_br", 0], dome=dict(comp=0, spread=1), kw=["꼭대기 쪽은", "바깥으로"],
          labels=[["제 무게에 눌린다", 0], ["치마 밑단이 퍼지듯", 1]]),
 11: dict(mg="dome", dome=dict(comp=-1, spread=-1, cracks=1), kw=["누르는 힘에는", "세로로 금이"],
          labels=[["누르는 힘에 강함 · 잡아당기는 힘에 약함", 0], ["벌어지는 아래에 세로 금", 1]]),
 12: dict(mg="madi"),
 13: dict(mg="dome", pre=["build2_tl", 0, "시도 2"], dome=dict(morph=0, people=1, rings=2), kw=["6미터가", "어른 키", "계단처럼"],
          labels=[["밑단 두께 6m 넘게", 0], ["어른 키 세 사람으로도 모자람", 1], ["계단 고리로 밑단을 누른다", 2]]),
 14: dict(mg="dome", dome=dict(shell="taper", rings=-1, measure=0), kw=["1.2미터"], labels=[["위로 갈수록 얇게", -1], ["6m → 1.2m, 5분의 1쯤", 0]]),
 15: dict(mg="dome", pre=["build2_bl", 0], dome=dict(shell="taper", rings=-1, bands=[0, 1, 2], bandTags=1, light=3),
          kw=["아래에는", "중간에는", "꼭대기 가까이에는", "위로 갈수록"]),
 16: dict(mg="dome", pre=["build2_br", 0], blocks=dict(heavy=0, light=1, dome=2), kw=["맨 위에", "거꾸로", "돔도 똑같습니다"], hold=1.0),
 17: dict(mg="dome", pre=["build3_tl", 1, "다섯 줄 × 스물여덟 개"], dome=dict(shell="taper", rings=-1, bands=[-1, -1, -1], coffers=1),
          kw=["다섯 줄", "그만큼 무게가"], labels=[["천장 홈 = 무게 덜기", 1]]),
 18: dict(mg="dome", dome=dict(shell="taper", rings=-1, bands=[-1, -1, -1], coffers=-1, heavy=0), kw=["80%쯤"],
          labels=[["전부 보통 무게 콘크리트였다면?", -1], ["구조에 걸리는 힘 약 80% 더", 0]]),
 19: dict(mg="madi"),
 20: dict(mg="dome", pre=["build3_tr", 2], dome=dict(shell="taper", rings=-1, bands=[-1, -1, -1], coffers=-1, oculus=1),
          kw=["가장 멀리", "덮지 않기로", "지름 9미터쯤"], labels=[["가장 높이, 가장 멀리 매달리는 자리", 0], ["덮지 않는다", 1]],
          post=["photo_oculus", 2, "지름 약 9m · 하늘이 그대로"]),
 21: dict(mg="dome", pre=["build3_bl", 1], dome=dict(shell="taper", rings=-1, bands=[-1, -1, -1], coffers=-1, open=1, rain=-1, drains=1),
          kw=["그럼 비는", "바닥을", "막지 않고"], labels=[["막지 않고, 받아서 흘려보낸다", 2]]),
 22: dict(mg="madi"),
 23: dict(mg="art", shots=[["dome_tr", -1, "out", "완성"], ["struct_tr", 0, "in", "몇 해 뒤 · 다시 세로 금"]], kw=["다시 세로로"]),
 24: dict(mg="dome", dome=dict(shell="taper", rings=-1, bands=[-1, -1, -1], coffers=-1, open=1, cracks=0, spread=2),
          kw=["아래쪽에서부터", "콘크리트가 마르며", "첫 번째 시도에서"],
          labels=[["실제 판테온 · 아래쪽 세로 균열", 0], ["마르며 줄어듦 + 제 무게", 1], ["시도 1의 그 벌어지는 힘", 2]]),
 25: dict(mg="dome", dome=dict(shell="taper", rings=-1, bands=[-1, -1, -1], coffers=-1, open=1, cracks=-1, comp=1),
          kw=["금은 아래쪽", "서로를 꽉", "두꺼운 밑단과", "가벼워진 지붕은"],
          labels=[["금은 벌어지는 아래에만", 0], ["위쪽은 서로 누르며 버팀", 1], ["밑단과 고리가 붙잡는다", 2]],
          post=["build3_br", 3]),
 26: dict(mg="madi"),
 27: dict(mg="art", shots=[["garage_tl", -1, "in"], ["lime_bl", 0, "in", "요즘 방식 · 철근 기둥"], ["lime_bl", 1, "in", "잡아당기는 힘은 철이 맡는다"],
                          ["rust_bl", 2, "right", "날씬하고 높게"]], kw=["요즘 방식으로", "잡아당기는", "날씬하고"]),
 28: dict(mg="art", shots=[["lime_br", -1, "in", "몇십 년 뒤"], ["rust_tl", 0, "in"], ["rust_tr", 1, "in", "녹 = 철보다 부피가 크다"],
                          ["rust_tr", 2, "in", "콘크리트가 상하는 가장 흔한 이유"]], kw=["속의 철근이", "녹은 원래", "콘크리트가 상하는"]),
 29: dict(mg="art", shots=[["garage_tl", -1, "in"], ["struct_tr", 0, "in", "판테온: 녹슬 철이 없다"]], kw=["판테온에는"]),
 30: dict(mg="madi"),
 31: dict(mg="art", shots=[["lime_tl", -1, "in", "다시 로마의 공사장"], ["lime_tl", 0, "in", "생석회 = 물을 만나면 뜨거워짐"], ["lime_tr", 1, "in"]],
          kw=["물을 만나면", "다 풀리지 않은"]),
 32: dict(mg="art", shots=[["lab_tl", -1, "in", "몇 mm 크기의 하얀 점"], ["lab_tl", 0, "in", "'대충 섞은 흔적'?"], ["lab_tr", 1, "in", "MIT · 아드미르 마시치 교수 (재현)"],
                          ["lab_tr", 2, "in", "생석회를 넣고 섞은 흔적"]], kw=["오랫동안", "MIT의", "그러니까"]),
 33: dict(mg="art", shots=[["lab_bl", -1, "in"], ["lab_bl", 0, "in", "일부러 금 → 물 흘려보내기"], ["lab_bl", 1, "in", "생석회 뺀 조각도 똑같이"]],
          kw=["일부러 금을", "생석회만 빼고"]),
 34: dict(mg="art", shots=[["lab_br", -1, "in", "2주 뒤"], ["lab_br", 0, "in", "로마 방식: 메워짐"], ["lab_br", 1, "in", "생석회 없음: 계속 샘"]],
          kw=["로마 방식의", "생석회를 뺀"]),
 35: dict(mg="art", shots=[["end_bl", -1, "in"], ["end_bl", 0, "in", "물 → 석회가 녹음 → 틈 안에서 다시 굳음"], ["end_bl", 1, "in", "틈을 메울 재료를 미리 넣어 둔 상자"],
                          ["photo_dome", 2, "out", "판테온 돔에서는 아직 확인 안 됨"]], kw=["스며든 물이", "하얀 점은 틈을", "다만"]),
 36: dict(mg="madi"),
 37: dict(mg="art", shots=[["history_tl", -1, "in", "609년 · 교회가 되다"], ["history_tr", 0, "in", "1600년대 · 입구 지붕의 청동"], ["history_bl", 1, "in", "→ 대포 (전해지는 이야기)"],
                          ["history_br", 2, "in", "쓰는 사람이 있는 건물"]], kw=["1600년대에는", "대포를", "사람들은 그 아래를"]),
 38: dict(mg="art", shots=[["rust_bl", -1, "right", "로마처럼 지으면 될까?"], ["rust_bl", 0, "right", "요즘 콘크리트보다 강하지 않다"], ["dome_br", 1, "out", "남은 건물만 보인다"],
                          ["end_bl", 2, "in", "'하얀 점' 방식 → 요즘 시멘트에"]], kw=["로마 콘크리트는", "우리가 보는", "대신 연구팀은"]),
 39: dict(mg="dome", pre=["end_tl", 1], dome=dict(shell="taper", rings=-1, bands=[-1, -1, -1], coffers=-1, open=1), kw=["지우는 다시", "두꺼운 밑단,", "처음 들어왔을"],
          labels=[["두꺼운 밑단 · 가벼워지는 지붕 · 비워 둔 꼭대기", 1]], post=["end_tr", 2]),
 40: dict(mg="art", shots=[["end_br", -1, "in"], ["end_br", 0, "in", "그 금이 무엇을 만나느냐"]], kw=["중요한 건"]),
 41: dict(mg="madi"),
}
beats = json.loads((HERE / "beats_v2.json").read_text(encoding="utf-8"))
assert len(beats) == len(P), (len(beats), len(P))
scenes = []
for b in beats:
    s = dict(b); s.update(P[b["id"]])
    assert (s["mg"] == "madi") == (b["kind"] == "madi"), b["id"]
    for k in s.get("kw", []):
        assert k in s["text"], (b["id"], k)
        assert s["text"].count(k) == 1, (b["id"], k, "여러 번")
    scenes.append(s)
(HERE / "pantheon_v2.json").write_text(json.dumps({"title": "철근 하나 없는 1,900년 된 돔은 왜 아직 서 있을까?", "version": "v2", "scenes": scenes},
                                                 ensure_ascii=False, indent=1), encoding="utf-8")
print(len(scenes), "장면")
