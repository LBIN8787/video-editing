"""유행 20년 편 장면 명세: beats.json(← beats.py script_v2.md) + 아래 표 → fashion20.json (render_full.py 의 SPEC, 화면 fashion20_overlay.html).
판테온 v5 방식 그대로: shots [그림, kw 번호(-1 = 처음부터), 카메라, 위 띠 글]. 그림 = 원화 조각 <시트>_tl|tr|bl|br (art_sheets.json 12시트),
실제 자료 photo_ktitle·photo_kfig20 (크로버 1919 논문 첫 쪽·그림 20, American Anthropologist 21(3), 퍼블릭 도메인 — 인터넷 아카이브 jstor-660477).
모션그래픽: ladder(레이버의 표 — 같은 옷 한 벌이 시간표 위를 지나감), osc(약 20년 물결 — 설명용 그림, 실제 측정값 아님), times2(숫자 두 줄).
shots 의 ['@mg', kw] = 그 구간은 모션그래픽. python make_spec.py"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
A = lambda shots, kw=(), **k: dict(mg="art", shots=shots, kw=list(kw), **k)
ALL = [-1] * 8
P = {
 1: A([["album_tl", -1, "in"], ["wardrobe_bl", 0, "in"]], ["몇 년 뒤"]),
 2: A([["wardrobe_tl", -1, "in"], ["wardrobe_tl", 0, "in", "11월의 어느 저녁"], ["wardrobe_tr", 1, "in"], ["wardrobe_bl", 2, "in", "이번 주 · 가게의 신상"]],
      ["11월의", "맨 안쪽에", "이번 주"]),
 3: A([["wardrobe_br", -1, "in"], ["album_br", 0, "in"]], ['"그거?']),
 4: A([["album_tl", -1, "in", "스무 해 전의 엄마"], ["album_tr", 0, "in", "고등학생 때 · 앨범"], ["album_bl", 1, "in"]], ["고등학생", "지금은"]),
 5: A([["wardrobe_tr", -1, "in"], ["album_bl", 0, "out"], ["album_bl", 1, "out", "유행은 왜, 스무 해쯤 지나면 돌아올까?"]], ["그런데 왜", "유행은 왜,"]),
 6: dict(mg="words", head="", lines=[["돌아온 건 옷이 아니라", 0], ["옷을 보는 눈", 1], ["'스무 해'는 생각보다 단단하지 않다", 2]],
         kw=["돌아온 건", "옷을 보는 눈입니다.", "그리고"]),
 7: A([["laver_tl", -1, "in"], ["laver_tl", 0, "in", "제임스 레이버 · 런던 빅토리아 앤드 앨버트 박물관"]], ["제임스"]),
 8: A([["laver_tr", -1, "in"], ["laver_tr", 0, "in", "그림 속 옷 = 연도의 단서"], ["laver_tr", 1, "in", "\"무엇을, 언제를 알고 나니 — 어떻게와 왜가 궁금해졌다\""]],
      ["그림 속", "그는 이렇게"]),
 9: A([["laver_br", -1, "in"], ["laver_bl", 0, "in", "1937년 책 · 그가 실었다고 전해지는 표"]], ["1937년에"]),
 10: dict(mg="ladder", img="laver_br", ladder=dict(show=[0, 1, 2, 3, None, 4, 5, 6], q=4),
          kw=["'망측하다'.", "'대담하다'.", "'세련됐다'.", "'흉하다'.", "'재밌다'가", "'낭만적이다',", "'아름답다'가"]),
 11: dict(mg="ladder", img="laver_br", ladder=dict(show=[-1, -1, -1, -1, 1, -1, -1, -1], q=-1, marker=[[2, -1], [4, 1]], hl=[[4, 0]]),
          kw=["스무 해 뒤는", "'우스꽝스럽다'입니다."]),
 12: dict(mg="ladder", img="laver_br", ladder=dict(show=ALL, marker=[[4, -1]], hl=[[4, -1]]),
          shots=[["@mg", -1, "", "스무 해 = 가장 우스워 보이는 때"], ["album_tr", 0, "in", "지우가 앨범을 보고 웃던 그 무렵"]], kw=["지우가"]),
 13: A([["phone_tl", -1, "in"], ["phone_tl", 0, "in", "사진첩을 십 년 전으로"], ["phone_tr", 1, "in", "그날 아침, 거울 앞에서는"]], ["휴대전화", "그 옷은"], hold=2.0),
 14: dict(mg="madi"),
 15: A([["phone_bl", -1, "in"], ["wardrobe_bl", 0, "in", "그럼 이번 주 가게의 신상은?"]], ["이번 주"]),
 16: A([["laver_br", -1, "out", "레이버의 표 = 눈이 어떻게 바뀌는지"], ["phone_br", 0, "in", "눈대중이 아니라, 자로"]], ["이걸"]),
 17: A([["photo_ktitle", -1, "in", "앨프리드 크로버 · 1919년 논문"], ["kroeber_tl", 0, "in", "75년 치 패션 잡지 (1844~1919)"],
       ["kroeber_tr", 1, "in", "해마다 그림 10장 · 치마 길이 · 치마 폭 · 허리"]], ["그는 75년", "치마 길이,"]),
 18: A([["photo_kfig20", -1, "in", "크로버 1919 · 치마 폭 (그림 20)"], ["kroeber_bl", 0, "in", "1850년대 말 · 종처럼 넓게"],
       ["kroeber_br", 1, "in", "1910년대 · 좁아진 치마"], ["wave_tl", 2, "in", "\"거대한 시계추처럼 — 한 번 흔들리는 데 한 세기\""]],
       ["종처럼", "반세기에", "크로버는 이렇게"]),
 19: dict(mg="times2", img="wave_tr", head="1940년 · 리처드슨과 크로버", rows=[["1605~1936년", "332년 치"], ["여섯 치수 물결의 평균", "98년"]],
          kw=["삼백 년", "98년이었습니다."]),
 20: A([["wave_tl", -1, "in", "스무 해가 아니라, 백 년 가까이"], ["wave_tl", 0, "in", "\"한 세기라는 값 자체에 큰 뜻은 없다\" — 두 저자"]], ["다만 두"]),
 21: dict(mg="times2", img="wave_bl", head="크로버가 틀린 것 · 치마 폭", rows=[["1919년 크로버의 예상", "넓어질 차례"], ["실제로 가장 좁았던 해", "1926년"]],
          kw=["그는 치마", "실제로"]),
 22: A([["wave_br", -1, "in", "1937년 · 유행 주기로 다음을 내다본 책"], ["wave_br", 0, "in", "\"주기가 가리킨 때는 이미 지나갔다\" — 저자"]], ["그 책의"]),
 23: dict(mg="madi"),
 24: A([["family_tl", -1, "in"], ["family_tl", 0, "in", "검색 · 유행 20년 주기"], ["family_tl", 1, "in", "처음 한 사람 — 확인 못 함"],
       ["wardrobe_bl", 2, "in", "패션 업계에서 오래 돌던 말"]], ["'유행 20년", "누가 처음", "패션 업계에서"]),
 25: A([["study_tl", -1, "in", "2026년 3월 · 미국 노스웨스턴대 연구 발표"], ["study_tl", 0, "in", "1869년부터 · 여성복 그림·사진 약 3만 7천 장"],
       ["study_tr", 1, "in", "치마 끝 · 목선 · 허리선의 높이"]], ["1869년부터의", "치마 끝과"]),
 26: dict(mg="osc", osc=dict(draw=0, period=1), kw=["출렁였습니다.", "약 스무"]),
 27: dict(mg="osc", osc=dict(conf=0, fan=1), shots=[["@mg", -1], ["study_bl", 2, "in", "예전 · 짧거나, 길거나"], ["study_br", 3, "in", "이제 · 여러 길이가 한꺼번에"]],
          kw=["물리학회에서", "1980년대부터는", "예전에는", "여러 길이가"]),
 28: dict(mg="times2", img="phone_br", head="재는 사람마다, 재는 시대마다", rows=[["리처드슨·크로버 1940", "약 100년"], ["노스웨스턴 2026 발표", "약 20년"]],
          shots=[["@mg", -1], ["wave_tl", 2, "in", "한쪽 끝까지 갔다가, 되돌아왔다"]], kw=["백 년에", "스무 해라는", "그들이 잰"]),
 29: A([["family_tr", -1, "in"], ["family_bl", 0, "in"], ["family_br", 1, "in"]], ["엄마는 그", "지우와는"]),
 30: A([["simmel_tl", -1, "in", "1904년 · 게오르크 짐멜 「유행」"], ["simmel_tl", 0, "in", "위쪽이 새 옷을 입고"],
       ["simmel_tr", 1, "in", "아래가 따라 입으면 → 위는 다른 옷으로"], ["simmel_tr", 2, "in", "퍼지는 만큼, 끝에 가까워진다"]], ["위쪽 계층이", "아래쪽이", "유행은 퍼지는"]),
 31: A([["simmel_bl", -1, "in"], ["simmel_bl", 0, "in", "\"반쯤 잊히고 나면, 다시 사랑받지 못할 이유가 없다\""]], ["예전 유행이"]),
 32: A([["simmel_br", -1, "in", "올해 발표 연구진의 풀이"], ["simmel_br", 0, "in", "바로 앞 시절과 달라지려는 힘 → 앞뒤로 흔들림"]], ["바로 앞"]),
 33: A([["today_tl", -1, "in", "요즘 다시 팔리는 2000년대 옷"], ["today_tl", 0, "in", "삼사십 대 · 향수"], ["today_tl", 1, "in", "십 대·이십 대 · 새로움"]], ["삼사십 대에게는", "십 대와"]),
 34: A([["today_tr", -1, "in", "스무 해 전의 엄마"], ["family_bl", 0, "in"], ["album_tl", 1, "in", "지우에게는 사진으로만 본 옷"], ["today_tr", 2, "out"]],
       ["엄마의 웃음은,", "지우에게는", "그 옷이"]),
 35: A([["today_bl", -1, "in", "미국 한 패션 대학 전문가의 풀이"], ["today_bl", 0, "in", "스무 해마다 · 지나간 시절을 그리워하는 새 손님"],
       ["today_bl", 1, "in", "재서 확인한 숫자가 아니라, 풀이"]], ["스무 해마다,", "재서"]),
 36: dict(mg="madi"),
 37: A([["mirror_tl", -1, "in"], ["wardrobe_bl", 0, "in"], ["mirror_tl", 1, "in", "어깨가 넓고, 기장이 어중간"]], ["가게에서", "어깨가"]),
 38: A([["wave_tr", -1, "in", "리처드슨·크로버의 책 (1940)"], ["mirror_tr", 0, "in", "약 200년 전 · '고대 그리스풍' 드레스"],
       ["mirror_bl", 1, "in", "고대 옷 · 짧은 치마, 넓은 목선"], ["mirror_tr", 2, "in", "자기 시대에 맞는 만큼만"]], ["이백 년", "정작", "자기 시대에"]),
 39: A([["today_br", -1, "in"], ["today_br", 0, "in", "옛 옷 + 지금 옷, 섞어 입기"]], ["지금 옷과"]),
 40: A([["mirror_br", -1, "in"]]),
 41: A([["wardrobe_tr", -1, "in", "스무 해 묵혀 두면?"], ["photo_kfig20", 0, "out", "물결을 찾은 사람들도, 다음 물결은"]], ["물결을 찾은"]),
 42: dict(mg="ladder", img="laver_br", ladder=dict(show=ALL, marker=[[3, -1]], hl=[[3, -1], [4, -1]]),
          shots=[["end_tl", -1, "in"], ["@mg", 0, "", "옷의 성질이 아니라, 시간표 위의 자리"], ["phone_tl", 1, "in"], ["end_tl", 2, "in"]],
          kw=["레이버의", "그렇다면 십", "올해 유행을"]),
 43: A([["end_tr", -1, "in"], ["end_tr", 0, "in", "올해 산, 지금 가장 흔한 옷"]], ["올해 산,"]),
 44: dict(mg="ladder", img="laver_br", ladder=dict(show=ALL, marker=[[2, -1], [3, 0]]),
          shots=[["@mg", -1, "", "올해의 옷"], ["@mg", 0, "", "십 년 뒤"], ["end_bl", 1, "in"]], kw=["흉해", "그리고 그"]),
 45: A([["end_br", -1, "in"]]),
 46: dict(mg="madi"),
}
beats = json.loads((HERE / "beats.json").read_text(encoding="utf-8"))
assert len(beats) == len(P), (len(beats), len(P))
scenes = []
for b in beats:
    s = dict(b); s.update(P[b["id"]])
    assert (s["mg"] == "madi") == (b["kind"] == "madi"), b["id"]
    for k in s.get("kw", []):
        assert k in s["text"] and s["text"].count(k) == 1, (b["id"], k)
    for sh in s.get("shots", []):
        assert sh[1] < len(s.get("kw", [])), (b["id"], sh)
    scenes.append(s)
(HERE / "fashion20.json").write_text(json.dumps({"title": "유행은 왜 20년쯤 지나면 돌아올까", "version": "v1", "scenes": scenes},
                                              ensure_ascii=False, indent=1), encoding="utf-8")
print(len(scenes), "장면")
