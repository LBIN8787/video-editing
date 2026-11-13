"""뉴스 데스크 카드 (스타일 news-desk, docs/25-reference-2611.md §1) — 장면 type "newsdesk".

어두운 바탕 위 '한 소식 = 한 장' 고정 틀:
  위 왼쪽 'NEWS 2 / 7 — 출처'와 진행 막대 · 위 오른쪽 채널 칩
  왼쪽: 꼬리표(주의·사례·지금 할 일) + 날짜 → 큰 제목(핵심 낱말 강조색) → 한 줄 요약 → 숫자 3칸 → 점 목록
  오른쪽: 증거 패널 하나 — 기사·공시 캡처(shot) / 큰 숫자 세기(bignum) / 도장(stamp)
  아래 왼쪽 출처 · 오른쪽 채널 주소. 자막은 영상 공통 자막 상자.

대본 (02_script/hybrid.json):
  {"type": "newsdesk", "idx": 2, "total": 7, "source": "OPENAI", "tag": "지금 할 일", "tag_color": "yellow", "date": "12월 전에 5분",
   "headline": "가벼운 질문은 Instant로", "hl": "Instant로", "sub": "공용 한도에서 안 깎이는 유일한 길",
   "stats": [{"label": "Instant 제한", "value": "제외", "color": "green"}, {"label": "무거운 모델", "value": "Codex에만", "color": "yellow"}],
   "bullets": ["사용량은 주 단위로 확인", "월말 막힘 줄이기"],
   "panel": {"kind": "shot", "src": "footage/notice.png", "caption": "공식 공지"}   # 또는 {"kind":"bignum","label":"..","value":"6,454"}
                                                                                # 또는 {"kind":"stamp","text":"월말에 안 막힌다","sub":".."}
   "panel_beat": 1, "footer": "출처: OpenAI 도움말 센터", "beats": [...]}
"""
from __future__ import annotations

import os
import re
import shutil
from pathlib import Path

COL = {"yellow": "#F5C518", "green": "#3DDC97", "red": "#FF5A4E", "blue": "#58A6FF", "white": "#F2F2F2"}
BG, PANEL, LINE, INK, MUTED = "#0E0F11", "#16181C", "#2A2D33", "#F2F2F2", "#8A8F98"


def _c(x: str | None, default="yellow") -> str:
    return COL.get(x or default, x or COL[default])


def s_newsdesk(D, sc: dict, bt: list, dur: float):
    from .hybrid import _e
    brand = sc.get("brand") or "이어 읽는 시장"
    acc = _c(sc.get("accent"), "yellow")
    i = D._id()
    t1 = bt[1][0] if len(bt) > 1 else 1.2
    pb = sc.get("panel_beat", 1 if len(bt) > 1 else 0)
    tp = bt[min(pb, len(bt) - 1)][0] + (0.2 if pb else 0.9)
    # 바탕 (카테고리 바탕 위를 덮음) + 바깥 틀
    D.media.append(f'<div style="position:absolute;inset:0;background:{BG}"></div>'
                   f'<div style="position:absolute;left:40px;top:40px;right:40px;bottom:40px;border:1px solid {LINE};border-radius:10px"></div>')
    # 위: 진행 막대 · NEWS n / N — 출처 · 채널 칩
    idx, total = sc.get("idx"), sc.get("total")
    if idx and total:
        D.items.append(f'<div style="position:absolute;left:40px;top:40px;right:40px;height:4px;background:{LINE}"></div>'
                       f'<div id="{i}pb" style="position:absolute;left:40px;top:40px;height:4px;width:{(1840) * (idx - 1) / total:.0f}px;background:{acc}"></div>')
        D.js.append(f'tl.to("#{i}pb",{{width:{1840 * idx / total:.0f},duration:0.8,ease:"power2.out"}},0.2);')
        head = f"NEWS {idx} / {total}" + (f" — {sc.get('source', '')}" if sc.get("source") else "")
    else:
        head = sc.get("source", "")
    D.items.append(f'<div style="position:absolute;left:96px;top:76px;font-family:sans;font-size:26px;letter-spacing:4px;color:{MUTED}">{_e(head)}</div>'
                   f'<div style="position:absolute;right:96px;top:68px;padding:6px 16px;border:1px solid {MUTED};border-radius:6px;font-family:sans-x;'
                   f'font-size:24px;color:{INK};letter-spacing:2px">▣ {_e(brand)}</div>')
    # 왼쪽 글 블록
    x0, y = 96, 190
    if sc.get("tag") or sc.get("date"):
        tc = _c(sc.get("tag_color"), "yellow")
        D.items.append(f'<div id="{i}tg" style="position:absolute;left:{x0}px;top:{y}px;font-family:sans-x;font-size:30px;white-space:nowrap">'
                       f'<span style="color:{tc}">{_e(sc.get("tag", ""))}</span>'
                       f'<span style="color:{MUTED};font-family:sans;margin-left:18px">{_e(sc.get("date", ""))}</span></div>')
        D.js.append(f'tl.fromTo("#{i}tg",{{opacity:0}},{{opacity:1,duration:0.3}},0.25);')
        y += 58
    hl = sc.get("hl", "")
    h = _e(sc.get("headline", ""))
    if hl and _e(hl) in h:
        h = h.replace(_e(hl), f'<span style="color:{acc}">{_e(hl)}</span>', 1)
    hsize = 84 if len(sc.get("headline", "")) <= 14 else 68
    D.items.append(f'<div id="{i}h" style="position:absolute;left:{x0}px;top:{y}px;width:{900 if sc.get("panel") else 1700}px;font-family:sans-x;'
                   f'font-size:{hsize}px;line-height:1.15;color:{INK};letter-spacing:-1px">{h}</div>')
    D.js.append(f'tl.fromTo("#{i}h",{{opacity:0,y:18}},{{opacity:1,y:0,duration:0.45,ease:"power3.out"}},0.35);')
    y += int(hsize * 1.25 * (1 if len(sc.get("headline", "")) <= 20 else 2)) + 16
    if sc.get("sub"):
        D.items.append(f'<div id="{i}s" style="position:absolute;left:{x0}px;top:{y}px;width:900px;font-family:sans;font-size:34px;color:#C9CDD3">{_e(sc["sub"])}</div>')
        D.js.append(f'tl.fromTo("#{i}s",{{opacity:0}},{{opacity:1,duration:0.4}},0.7);')
        y += 80
    stats = sc.get("stats") or []
    for k, st in enumerate(stats[:3]):
        sx = x0 + k * 300
        D.items.append(f'<div id="{i}st{k}" style="position:absolute;left:{sx}px;top:{y}px;width:280px">'
                       f'<div style="font-family:sans;font-size:22px;color:{MUTED}">{_e(st.get("label", ""))}</div>'
                       f'<div style="font-family:sans-x;font-size:52px;line-height:1.2;color:{_c(st.get("color"), "green")};white-space:nowrap">{_e(st.get("value", ""))}</div></div>')
        D.js.append(f'tl.fromTo("#{i}st{k}",{{opacity:0,y:14}},{{opacity:1,y:0,duration:0.35,ease:"power2.out"}},{t1 + 0.15 * k if len(bt) > 1 else 1.0 + 0.15 * k:.2f});')
    if stats:
        y += 120
    for k, b in enumerate((sc.get("bullets") or [])[:3]):
        D.items.append(f'<div id="{i}b{k}" style="position:absolute;left:{x0}px;top:{y + k * 50}px;font-family:sans-x;font-size:30px;color:{INK};white-space:nowrap">'
                       f'<span style="display:inline-block;width:14px;height:14px;background:{acc};margin-right:16px;vertical-align:middle"></span>{_e(b)}</div>')
        D.js.append(f'tl.fromTo("#{i}b{k}",{{opacity:0,x:-12}},{{opacity:1,x:0,duration:0.3}},{(bt[-1][0] if len(bt) > 1 else 1.4) + 0.2 * k:.2f});')
    # 오른쪽 증거 패널
    p = sc.get("panel") or {}
    if p:
        px, py, pw, ph = 1060, 190, 760, 560
        kind = p.get("kind", "shot")
        D.items.append(f'<div id="{i}p" style="position:absolute;left:{px}px;top:{py}px;width:{pw}px;height:{ph}px;background:{PANEL};'
                       f'border:1px solid {LINE};border-radius:12px;overflow:hidden"></div>')
        D.js.append(f'tl.fromTo("#{i}p",{{opacity:0,x:40}},{{opacity:1,x:0,duration:0.45,ease:"power3.out"}},{tp:.2f});')
        if kind == "shot" and p.get("src"):
            src = Path(sc["_project_dir"]) / "04_assets" / p["src"]
            if src.exists():
                name = f"nd_{sc['id']:03d}{src.suffix}"
                dst = D._work / "assets" / name
                if dst.exists():
                    dst.unlink()
                try:
                    os.link(src, dst)
                except OSError:
                    shutil.copy(src, dst)
                D.items.append(f'<div id="{i}ps" style="position:absolute;left:{px + 40}px;top:{py + 40}px;width:{pw - 80}px;height:{ph - 110}px;'
                               f'background:#fff;border-radius:6px;overflow:hidden;box-shadow:0 10px 30px rgba(0,0,0,.5);transform:rotate(-1deg)">'
                               f'<img src="assets/{name}" style="width:100%;height:100%;object-fit:cover;object-position:{p.get("pos", "50% 0%")}"></div>')
                D.js.append(f'tl.fromTo("#{i}ps",{{opacity:0,scale:0.96}},{{opacity:1,scale:1,duration:0.4}},{tp + 0.2:.2f});'
                            f'tl.to("#{i}ps img",{{scale:1.06,duration:{max(dur - tp, 1):.2f},ease:"none"}},{tp:.2f});')
            else:
                D.qa.append(f"newsdesk/missing-shot: 04_assets/{p['src']}")
        elif kind == "bignum":
            val = str(p.get("value", ""))
            num = re.sub(r"[^\d.]", "", val)
            D.items.append(f'<div style="position:absolute;left:{px}px;top:{py + 150}px;width:{pw}px;text-align:center;font-family:sans;font-size:28px;color:{MUTED}">{_e(p.get("label", ""))}</div>'
                           f'<div id="{i}n" style="position:absolute;left:{px}px;top:{py + 200}px;width:{pw}px;text-align:center;font-family:sans-x;font-size:150px;color:{acc};letter-spacing:4px">{_e(val)}</div>')
            if num and num.replace(".", "").isdigit():
                dec = len(num.split(".")[1]) if "." in num else 0
                pre, post = val.split(num[0], 1)[0], val[val.rfind(num[-1]) + 1:]
                comma = "," in val
                fmt = (f'Number(o.v.toFixed({dec})).toLocaleString("en-US",{{minimumFractionDigits:{dec},maximumFractionDigits:{dec}}})'
                       if comma else f'o.v.toFixed({dec})')
                D.js.append(f'(function(){{var o={{v:0}};tl.to(o,{{v:{num},duration:1.2,ease:"power2.out",onUpdate:function(){{'
                            f'document.getElementById("{i}n").textContent="{_e(pre)}"+{fmt}+"{_e(post)}";}}}},{tp + 0.3:.2f});}})();')
            D.sfx.append(("riser", tp))
        elif kind == "stamp":
            txt = p.get("text", "")
            fs = int(min(66, (pw - 220) / max(len(txt), 1) * 1.05))
            col = _c(p.get("color"), "green")
            D.items.append(f'<div style="position:absolute;left:{px}px;top:{py}px;width:{pw}px;height:{ph}px;display:flex;flex-direction:column;'
                           f'align-items:center;justify-content:center;gap:34px">'
                           f'<div id="{i}x" style="padding:16px 34px;border:8px solid {col};border-radius:12px;color:{col};font-family:sans-x;'
                           f'font-size:{fs}px;white-space:nowrap;transform:rotate(-4deg)">{_e(txt)}</div>'
                           f'<div style="font-family:sans-x;font-size:30px;color:{INK}">{_e(p.get("sub", ""))}</div></div>')
            D.js.append(f'tl.fromTo("#{i}x",{{opacity:0,scale:1.8}},{{opacity:1,scale:1,duration:0.28,ease:"power4.in"}},{tp + 0.3:.2f});')
            D.sfx.append(("pop", tp + 0.55))
        if p.get("caption"):
            D.items.append(f'<div style="position:absolute;left:{px}px;top:{py + ph + 14}px;width:{pw}px;text-align:center;font-family:sans;font-size:22px;color:{MUTED}">{_e(p["caption"])}</div>')
    # 아래: 출처 · 채널 주소
    # 출처는 자막 상자(아래 가운데)와 겹치지 않게 본문 아래 줄에 (2026-11-13 시험작에서 겹침 발견)
    D.items.append(f'<div style="position:absolute;left:96px;top:830px;width:1730px;padding-top:14px;border-top:1px solid {LINE};'
                   f'font-family:sans;font-size:22px;color:{MUTED};display:flex;justify-content:space-between">'
                   f'<span>{_e(sc.get("footer", ""))}</span><span>{_e(sc.get("handle", "@이어읽는시장"))}</span></div>')


def register():
    from . import hybrid
    hybrid.RENDER["newsdesk"] = s_newsdesk
