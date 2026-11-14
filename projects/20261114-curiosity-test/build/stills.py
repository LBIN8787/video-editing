import sys, json
sys.path.insert(0, "build")
import board as B
board = json.loads((B.PROJ/"02_script"/"board.json").read_text(encoding="utf-8"))
timings = json.loads((B.VOICE/"timings.json").read_text(encoding="utf-8"))
durs = json.loads((B.VOICE/"durations.json").read_text(encoding="utf-8"))
bg = {k: B.paper_bg(k, 7+i) for i, k in enumerate(("paper","dark","sand"))}
for spec in sys.argv[1:]:
    sid, tt = spec.split(":")
    sc = next(s for s in board["scenes"] if s["id"] == int(sid))
    B.render_scene(sc, timings[sid], bg, B.ASSETS/"x.mp4", durs[sid], still_at=float(tt))
