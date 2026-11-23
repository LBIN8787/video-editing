"""기억 편 보완 (2026-11-19) — 가까운 샷 완성 장면 주문 → orders_memory_shots.json.

사용자: "전체적인 화면 퀄리티 자체는 codex가 우세하지만 편집법 연출법 자체는 클로드가 좋았다" — 화풍은 그대로(합격한 셀 화풍),
화면 완성도를 올린다: 넓은 배경 판 위에 자른 인물을 세우는 장면만 계속되지 않게, 이야기의 핵심 순간은
인물·배경·빛이 한 장에 함께 그려진 가까운 샷(손·어깨 너머·표정)으로. 같은 인물은 이미 그린 인물 시트를 참조로 붙여 유지.
실제 사건 당사자의 얼굴은 그리지 않는다(법정 장면은 손·서류만).
    python scripts/anim/orders_memory_shots.py && python scripts/anim/gen_art.py <art> --orders scripts/anim/orders_memory_shots.json
"""
import json
from pathlib import Path

H = Path(__file__).resolve().parent
base = json.loads((H / "orders_memory.json").read_text(encoding="utf-8"))
V = "curiosity"
SHOT = ("A finished cinematic anime film frame, characters and background painted together in one image with consistent light "
        "and shadow, shallow depth of field, no text. ")


def S(i, t, ref=()):
    return {"video": V, "id": i, "kind": "plate", "prompt": SHOT + t, "ref": list(ref)}


orders = [
    S("sh_hand86", "Close-up over a 1986 university wooden desk in morning window light: an older professor's hand in a brown tweed sleeve placing a single blank sheet of lined paper in front of a curly-haired student whose hands hold a pencil. Faces out of frame.", ["neisser_sheet.png", "stu86_sheet.png"]),
    S("sh_write86", "Over-the-shoulder medium close-up of the same curly brown-haired college student in a cream cable-knit sweater writing quickly on a sheet of lined paper at a wooden classroom desk, soft winter morning light from tall windows, other students blurred in the background.", ["stu86_sheet.png"]),
    S("sh_shock88", "Medium close-up of the same curly brown-haired student in a cream cable-knit sweater holding an old handwritten sheet of paper in both hands, staring at it in disbelief, a warm classroom softly blurred behind her.", ["stu86_sheet.png"]),
    S("sh_bart32", "Medium two-shot in a 1932 Cambridge wood-paneled room with gothic windows: the same British psychologist with round glasses and grey three-piece suit reading a typed story aloud from a sheet, while the same young student in a tweed jacket listens across a table, warm afternoon light.", ["bartlett_sheet.png", "stud32_sheet.png"]),
    S("sh_film74", "View from behind a row of 1970s college students sitting in a dim classroom, their silhouettes in the foreground, watching a projected film on a pull-down screen that shows two sedans about to meet at an intersection, a beam of light from a 16mm projector.", ["stud74_sheet.png"]),
    S("sh_check74", "Extreme close-up of a 1970s student's hand holding a pencil, hesitating above a printed questionnaire with yes and no checkboxes on a wooden desk (no readable words), striped shirt cuff visible, soft light.", ["stud74_sheet.png"]),
    S("sh_mall", "Wide-medium shot inside a 1970s indoor shopping mall with a fountain: the same small boy in a striped t-shirt crying alone, and the same kind elderly woman in a flowered dress bending down and reaching out her hand to him, warm hazy nostalgic light like an old memory.", ["mallkid_sheet.png"]),
    S("sh_interview95", "Medium shot in a 1995 interview room: the same young man in a green sweater sitting with eyes closed, fingers on his temple, trying to remember, a cassette recorder and booklet on the table, the woman interviewer softly out of focus in the foreground.", ["particip_sheet.png"]),
    S("sh_rat00", "Medium close-up in a 2000 neuroscience lab: the same scientist in a white lab coat leaning toward a clear-walled test chamber where a small white rat crouches frozen on a metal grid floor, a small speaker on the chamber wall, cool fluorescent light.", ["rat_sheet.png"]),
    S("sh_write01", "Medium shot of the same college student woman in a grey hoodie writing on a clipboard in a 2001 college lounge, autumn light, other students writing at a table blurred behind her, a TV with a dark screen in the background. Calm, quiet mood.", ["stud01_sheet.png"]),
    S("sh_lineup84", "Close-up of hands of an anonymous person resting on a 1980s police table next to a photo lineup card of six small anonymous grey silhouettes (no faces), a pen and an official form, dim office light. No faces in frame.", []),
    S("sh_family", "Medium shot of the same Korean brother and sister in their 40s sitting on a sofa in a warm living room in the evening, laughing while disagreeing about an old memory, an old family photo album open on the low table.", ["family_sheet.png"]),
    S("sh_ask", "Medium shot in a warm Korean living room: the same young mother kneeling to her child's eye level and gently asking a question, the same 7-year-old in a yellow t-shirt answering with small hand gestures, soft lamp light.", ["family_sheet.png"]),
    S("sh_drawer", "Close-up of an open wooden desk drawer at night under warm lamp light, a single old handwritten sheet of lined paper with blue ink lying inside (no readable words), slight dust in the light.", ["props86_sheet.png"]),
]

out = H / "orders_memory_shots.json"
out.write_text(json.dumps({"styles": base["styles"], "orders": orders}, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(orders), "→", out)
