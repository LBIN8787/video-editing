#!/usr/bin/env bash
# 긴 장면을 구간으로 나눠 동시에 렌더 → 이어 붙임 → 목소리·효과음·자막 입혀 검토본.
#   bash render_all.sh <out 폴더> <html> <voice> <ass> <끝 초> <결과.mp4> [구간 수=3]
# (Microsoft Store 판 Python 에서 node 를 띄우면 브라우저 폴더가 가려져서, node 는 셸에서 직접 띄운다)
set -e
H="$(cd "$(dirname "$0")" && pwd)"
OUT="$1"; HTML="$2"; VOICE="$3"; ASS="$4"; END="$5"; RES="$6"; N="${7:-3}"
export NODE_PATH="$H/../../tools/playwright/node_modules"
mkdir -p "$OUT"
: > "$OUT/parts.txt"
for ((i=0; i<N; i++)); do
  A=$(python -c "print(round($END*$i/$N*30)/30)")
  Z=$(python -c "print(round($END*($i+1)/$N*30)/30)")
  node "$H/render.js" "$HTML" "$OUT/part$i.mp4" "$A" "$Z" > "$OUT/part$i.log" 2>&1 &
  echo "file '$(cygpath -m "$OUT/part$i.mp4" 2>/dev/null || echo "$OUT/part$i.mp4")'" >> "$OUT/parts.txt"
done
wait
for ((i=0; i<N; i++)); do [ -s "$OUT/part$i.mp4" ] || { echo "part$i failed"; tail -5 "$OUT/part$i.log"; exit 1; }; done
ffmpeg -v error -y -f concat -safe 0 -i "$OUT/parts.txt" -c copy "$OUT/video.mp4"
python "$H/finish.py" "$OUT/video.mp4" "$VOICE" "$ASS" "${HTML%.html}.sfx.json" "$END" "$RES"
