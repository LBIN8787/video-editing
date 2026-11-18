"""무음 영상 + 원래 목소리(승인된 대본·음성) + 효과음 + 자막 → 검토본. python finish.py <video.mp4> <voice> <captions.ass> <sfx.json> <end초> <out.mp4>"""
import json, subprocess, sys
from pathlib import Path
vid, voice, ass, sfx, end, out = sys.argv[1:7]
SFX = Path(__file__).resolve().parents[2] / ".claude/skills/media-use/audio/assets/sfx"
FONTS = Path(__file__).resolve().parents[2] / "ytflow/assets/fonts"
import os
# 효과음은 기본으로 넣지 않음 (2026-11-19 사용자: "효과음들이 전체적으로 별로 듣기 좋은 효과음이 아니야") — 넣으려면 YTFLOW_SFX=1
ev = json.loads(Path(sfx).read_text(encoding="utf-8")) if os.environ.get("YTFLOW_SFX") == "1" else []
ins = ["-i", vid, "-i", voice]
flt = [f"[1:a]atrim=0:{end},aresample=48000[v]"]
for k, (n, t, v) in enumerate(ev):
    ins += ["-i", str(SFX / f"{n}.mp3")]
    flt.append(f"[{k+2}:a]atrim=0:2,volume={v},adelay={int(t*1000)}|{int(t*1000)},aresample=48000[s{k}]")
mix = "[v]" + "".join(f"[s{k}]" for k in range(len(ev)))
flt.append(f"{mix}amix=inputs={1+len(ev)}:normalize=0,loudnorm=I=-14:TP=-1.5[a]")
a = Path(ass).resolve().as_posix().replace(":", "\:")
fd = FONTS.as_posix().replace(":", "\:")
flt.append(f"[0:v]ass='{a}':fontsdir='{fd}'[vo]")
subprocess.run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", ";".join(flt), "-map", "[vo]", "-map", "[a]",
                "-c:v", "libx264", "-preset", "slow", "-crf", "15", "-tune", "animation", "-pix_fmt", "yuv420p",
                "-c:a", "aac", "-b:a", "192k", "-t", str(end), "-movflags", "+faststart", out], check=True)
print("ok", out)
