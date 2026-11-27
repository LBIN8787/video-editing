"""두 실화 영상의 장면 삽화 — 사용자 Codex $imagegen. 결과: E:/ytflow-local/books-video/<편>/art/<id>.png (1920x1080) + _raw."""
import re, shutil, subprocess, time, pathlib, sys, concurrent.futures as cf
from PIL import Image

ROOT = pathlib.Path(r"E:\ytflow-local\books-video")
GEN = pathlib.Path.home() / ".codex" / "generated_images"
HEAD = "Use $imagegen to create exactly one image as described below. Do not write any code and do not edit any file; just generate the image.\n\n"
TAIL = ("\n\nFRAMING: wide 16:9 landscape, cinematic composition with depth, the main subject clearly readable even when the frame is cropped to its central 70%. "
        "Absolutely no text, letters, numbers, captions, labels, signatures, borders or watermarks anywhere in the image.")

STYLE_A = ("STYLE: early 20th-century polar expedition record illustration — ink drawing with grey and faded sepia wash, the look of a hand-tinted glass-plate photograph, "
           "muted cold palette of slate blue, grey and bone white, fine paper grain, realistic proportions, restrained and documentary, painterly but precise.")
STYLE_B = ("STYLE: 1950s Soviet magazine documentary illustration — graphite pencil and black ink on off-white paper with a single muted blue-grey wash, "
           "realistic, restrained, quiet and respectful mood, visible pencil hatching, no gore.")

A = {  # 섀클턴 (1914–1916)
 "a01_boat_waves": "A tiny open wooden lifeboat about 7 metres long with a makeshift canvas cover and six men in it, riding high on the crest of an enormous grey Southern Ocean swell; "
                   "towering waves, spray, low dark clouds. The boat is in the centre-left third, small but detailed; vast sea all around.",
 "a02_chart_antarctica": "An old hand-drawn nautical chart on aged parchment showing the whole Antarctic continent seen from above as a pale icy landmass, with surrounding ocean hatching and compass rose; schematic, no writing at all.",
 "a03_ship_departing": "A three-masted wooden barquentine with a steam funnel leaving a harbour in 1914, crew waving on deck, gulls, morning light, the ship large in the right half.",
 "a04_ship_trapped_night": "The same wooden three-masted ship frozen solid in Antarctic pack ice at night, lit by a bright flash from the ice so that frost glitters on every rope and spar, dark sky; ship centred.",
 "a05_football_ice": "Expedition men in heavy wool clothes playing football on flat sea ice beside a wooden ship locked in the ice, sled dogs watching, low winter sun, long shadows.",
 "a06_ship_crushed": "The wooden ship crushed and listing heavily between huge buckled pressure ridges of ice, masts tilted and tangled, timbers broken; men watching from the ice at a distance.",
 "a07_ice_camp": "A camp of small canvas tents on a vast drifting ice floe, three wooden lifeboats on sledges, men hauling one boat with ropes, grey light, endless white horizon.",
 "a08_tent_bags": "Inside a cramped canvas tent lit by a single candle: a weathered expedition leader hands out fur sleeping bags to tired men crowded together; warm candlelight inside, blue darkness at the tent flap.",
 "a09_boats_floes": "Three small open lifeboats rowing between jagged ice floes in a dark choppy sea, men with frostbitten faces pulling oars, spray freezing on the gunwales.",
 "a10_elephant_island": "A bleak rocky beach under black cliffs and a glacier; exhausted men staggering ashore beside three beached lifeboats; some kneel and touch the stones.",
 "a11_worsley_sextant": "Inside a small pitching lifeboat a captain stands braced, raising a brass sextant toward a pale sun glimpsed through a gap in the clouds, while another man holds him around the waist; waves around.",
 "a12_night_ice_chip": "Night at sea: men crawl on the iced-over canvas deck of a small boat, chipping thick ice off with an axe, freezing spray flying, a lantern's faint glow.",
 "a13_sighting_georgia": "From inside a small boat looking over the bow: through breaking clouds, black jagged mountains and glaciers of a large island rise on the horizon; men in the boat reaching and pointing.",
 "a14_chart_ocean": "An old hand-drawn nautical chart on aged parchment: open ocean hatching, a small rocky island near the lower-left corner and a long mountainous island near the upper-right corner, compass rose; schematic, no writing at all.",
 "a15_ridge_moonlight": "Moonlit snowy mountain ridge, three men roped together standing on the edge of a steep icy slope, fog rolling in below, vast dark peaks.",
 "a16_dawn_station": "Dawn: three tiny figures seen from behind on a mountain ridge, looking far down at a whaling station by a fjord with chimneys, sheds and steam; first light on the snow.",
 "a17_station_door": "At the door of a whaling-station manager's wooden house, three ragged, bearded, soot-blackened men face a clean, startled manager; morning light, workers staring in the background.",
 "a18_rescue_tug": "A small steam tug approaching a bleak rocky beach; on shore, a hut made of two upturned boats, and a crowd of ragged men waving and running toward the water.",
 "a19_wreck_deep": "Deep under the sea, the stern of an old wooden ship sitting upright on the dark seabed, lit by the beams of a robotic submersible, sea anemones on the rail, drifting particles; eerie calm.",
}
B = {  # 댜틀로프 (1959)
 "b01_tent_slope": "A wide snowy mountain slope under low clouds: a half-buried canvas tent in the upper-left third, one long side of it slashed open; a line of footprints runs from the tent down and to the right toward a distant dark edge of forest.",
 "b02_cabin_skiers": "Young Soviet students in 1950s winter ski gear laughing outside a log cabin in deep snow, one playing a guitar, others fixing skis; bright cold day.",
 "b03_chart_urals": "An old hand-drawn topographic chart of a northern mountain range: ridges, rivers and forest marks, seen from above on aged paper; schematic, no writing at all.",
 "b04_pitch_tent": "Late afternoon, strong wind on a bare snowy slope: a group of young skiers dig into the slope to cut a flat shelf in the snow and raise a long canvas tent on it; blowing snow.",
 "b05_tent_inside": "Inside a long canvas tent at night lit by a single candle: young people in sweaters sitting in sleeping bags, eating and talking quietly; warm, ordinary, calm.",
 "b06_search_party": "Searchers in fur hats and padded coats stand around a half-buried, slashed canvas tent on a snowy slope, one kneeling to look inside; grey light.",
 "b07_cedar": "A huge old Siberian cedar at the edge of a snowy forest; at its foot the remains of a small extinguished campfire; several high branches are snapped off; quiet and empty, no people.",
 "b08_slope_between": "A long empty snowy slope seen from the forest edge looking uphill toward a tiny distant tent; three small dark shapes lie far apart in the snow along the way, indistinct and respectful.",
 "b09_ravine": "A deep snowy ravine in spring thaw with a stream beginning to run; in the snow, a small floor made of cut fir branches and a few scattered pieces of cloth; no people.",
 "b10_case_file": "A Soviet investigator's desk in 1959: a closed cardboard case folder tied with string, a typewriter, an ashtray and a desk lamp in a dim office.",
 "b11_scientists": "Two researchers seen from behind in a modern office at night, looking at large computer monitors that show a 3D simulation of a snow slope and a small slab sliding; faces not visible.",
 "b12_slope_diagram": "A clean scientific cross-section illustration of a snowy slope: a shelf cut into the slope with a tent on it, snow drifting over the cut wall and building up, and a thick slab of snow beginning to slide down onto the tent; arrows shown only as simple shapes, no writing.",
 "b13_tent_slash": "Inside a dark tent whose roof is pressed down under the heavy weight of snow; a hand with a small knife slashes the canvas side from inside, a cold blue night glimpsed through the cut.",
 "b14_descending": "Night on a snowy slope under faint moonlight: nine small silhouettes walking in single file down toward a dark forest, supporting each other, one being helped by two others; seen from far behind.",
 "b15_tent_light": "The same half-buried tent on the slope at early morning: pale light shines through the long slash in its side, and inside, neat rows of boots and folded coats are visible; peaceful, still.",
}

def fit169(src, dst):
    im = Image.open(src).convert("RGB"); w, h = im.size; t = 16 / 9
    if w / h > t: nw = int(h * t); im = im.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
    else: nh = int(w / t); im = im.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))
    im.save(dst)  # 원본 해상도 그대로(16:9 로만 자름) — 카메라 확대 여유

def one(job):
    proj, k, scene, style = job
    out = ROOT / proj / "art" / f"{k}.png"; out.parent.mkdir(parents=True, exist_ok=True)
    logd = ROOT / proj / "logs"; logd.mkdir(exist_ok=True)
    if out.exists(): return f"skip {k}"
    p = HEAD + "SCENE: " + scene + "\n\n" + style + TAIL
    t0 = time.time()
    for _ in range(2):
        r = subprocess.run('"codex" "exec" "--skip-git-repo-check" "-m" "gpt-6-sol"', input=p, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", shell=True, cwd=str(logd))
        log = (r.stdout or "") + "\n" + (r.stderr or ""); (logd / f"{k}.log").write_text(log, encoding="utf-8")
        m = re.search(r"session id:\s*([0-9a-f-]{36})", log)
        if m and (GEN / m.group(1)).exists():
            pngs = sorted((GEN / m.group(1)).glob("*.png"), key=lambda q: q.stat().st_mtime)
            if pngs:
                shutil.copy2(pngs[-1], out.with_name(k + "_raw.png")); fit169(pngs[-1], out)
                return f"ok {k} {time.time() - t0:.0f}s"
    return f"FAIL {k}"

jobs = [("shackleton", k, v, STYLE_A) for k, v in A.items()] + [("dyatlov", k, v, STYLE_B) for k, v in B.items()]
with cf.ThreadPoolExecutor(int(sys.argv[1]) if len(sys.argv) > 1 else 4) as ex:
    for res in ex.map(one, jobs): print(res, flush=True)
