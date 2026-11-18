import sys

# Windows 한국어 콘솔(cp949)은 '—' 같은 글자를 못 찍어 잠금 자동 잡기가 중간에 실패했다 (2026-11-19) → 못 찍는 글자는 바꿔 찍기
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(errors="replace")
    except Exception:
        pass

from .cli import main  # noqa: E402

main()
