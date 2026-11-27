import json, sys, pathlib, concurrent.futures as cf
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import importlib.util
spec = importlib.util.spec_from_file_location("aj", str(pathlib.Path(__file__).parent / "art_jobs.py"))
src = open(spec.origin, encoding="utf-8").read().split("jobs = [")[0]   # 함수만 가져옴
ns = {}; exec(src, ns)
R = json.load(open(sys.argv[1], encoding="utf-8"))
style = R["style"] + " " + R["chars"]
jobs = [("eden", k, v, style) for k, v in R["images"].items()]
with cf.ThreadPoolExecutor(4) as ex:
    for r in ex.map(ns["one"], jobs): print(r, flush=True)
