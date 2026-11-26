"""A안 본 그림. Codex 샌드박스가 G: 에 못 쓰므로 생성 폴더에서 새 파일을 찾아 옮긴다."""
import subprocess, sys, time, shutil, glob, os
from pathlib import Path
OUT = Path(r"G:\내 드라이브\ytflow\영상\20261126-history-sohyeon\art")
OUT.mkdir(parents=True, exist_ok=True)
GEN = r"D:\AI-Storage\codex\generated_images"
S = Path(r"G:\내 드라이브\ytflow\영상\20261126-history-sohyeon\samples")
PRINCE = str(S / "A3_observatory.png")   # 인물 기준 그림
STYLEREF = str(S / "A1_yeomseup.png")
A = ("Cinematic historical digital painting, like a still from a prestige film: dramatic natural light, muted desaturated palette "
     "(deep indigo, ash grey, warm candle amber) with a single restrained dark-red accent, soft painterly brushwork, atmospheric haze, "
     "16:9 widescreen landscape composition, historically accurate 17th-century Joseon Korea and Qing China costume and architecture. "
     "Match the painting style of the attached reference image exactly. No text, no letters, no watermark, no gore, no visible blood.")
PR = "The crown prince must look exactly like the man in the red robe in the attached reference (same face, thin moustache, slim face, dark red royal robe with round gold dragon badge, black ikseongwan cap). "
JOBS = [
 ("A4_jeju", [STYLEREF], "1647, a windswept black-basalt coast of Jeju Island under a heavy grey sky, Hallasan mountain in the distance. Three small Joseon boys in plain white hanbok (about 11, 7 and 3 years old) stand close together looking out at the sea, seen from behind. Two Joseon soldiers stand at a distance holding spears, wearing Joseon black felt brimmed 'jeollip' hats and dark Joseon military coats (NOT Qing hats, no red tassels). Lonely wide shot; a small red ribbon on the youngest child's hair is the only color."),
 ("N1_farm", [PRINCE, STYLEREF], PR + "Around 1640, flat farmland outside Shenyang in Manchuria, early summer. Dozens of ragged Joseon captives in worn white clothes plough and plant fields; the crown prince stands on a low earthen bank watching them with a steward holding a ledger. Wide shot, hazy sun."),
 ("N2_diplomacy", [PRINCE, STYLEREF], PR + "Inside a Qing Manchu hall in Shenyang, around 1640. The crown prince stands firm before seated Manchu noblemen in Qing robes and fur-trimmed hats who are pointing at a list on a table. Tense negotiation, side light from paper windows."),
 ("N3_beijing_fall", [STYLEREF], "Spring 1644, night. The massive walls and gate towers of Ming Beijing burn; rebel soldiers with torches and banners pour through the gate; smoke over the Forbidden City roofs in the distance. Epic wide shot, orange fire against deep indigo sky."),
 ("N4_greatwall", [STYLEREF], "1644, dawn. Qing Manchu cavalry with banners stream through Shanhai Pass, the eastern gate of the Great Wall, toward the south. Mist, long shadows, wide aerial-like composition."),
 ("N5_return", [PRINCE, STYLEREF], PR + "Late winter 1645, Changgyeonggung palace in Seoul. The crown prince, travel-worn, walks into a wide stone courtyard where no officials are lined up to greet him; the courtyard is empty except for a few silent eunuchs. Ox carts with wooden chests of books and a wrapped globe wait at the gate behind him. Cold blue light."),
 ("N6_physician", [PRINCE, STYLEREF], PR + "April 1645, a dim sickroom. The crown prince lies ill under a quilt, eyes closed, pale. A court physician seen from behind (face not visible) kneels beside him, an open acupuncture needle case on the floor. Single candle."),
 ("N7_coffin", [STYLEREF], "A dark palace mourning hall, 1645. Close shot of hands closing the lid of a lacquered wooden coffin draped in white hemp; a candle flame bends as the lid comes down. Only two attendants present, the hall otherwise empty. Somber."),
 ("N8_kangbin", [STYLEREF], "1646, a small detached annex in the back garden of a Joseon palace, its door locked with a heavy iron lock and guarded by two soldiers in Joseon dress. Inside through a half-open paper window, a dignified young widow (crown princess, about 35) in white mourning hanbok sits alone, upright, looking out. Late winter dusk."),
 ("N9_tray", [STYLEREF], "1646, close still-life: on a dark floor of an empty Joseon palace room, a small red lacquer tray holds a single white porcelain bowl and a folded royal decree with a red seal cord. Morning light through paper doors. No people. Quiet and ominous."),
 ("N10_scribe", [STYLEREF], "A Joseon royal secretariat office at night, 1645. A scribe in an official's black gat and robe writes the daily court record with a brush by lamplight; stacks of bound books around him. Calm, documentary feel."),
 ("N11_injo", [STYLEREF], "1645, a dim Joseon throne hall. An aging king (about 50, King Injo) in a red royal robe sits alone on the throne before the Irworobongdo folding screen of sun, moon and five peaks, face half in shadow, staring at nothing. No courtiers. Cold light."),
 ("N12_shenyang_house", [PRINCE, STYLEREF], PR + "Around 1642, the courtyard of the Joseon residence (Simyanggwan) in Shenyang: busy like a market — Joseon servants carry sacks of grain, Manchu merchants bargain over bolts of silk and furs, the crown prince watches from a veranda. Daylight, lively."),
]
def new_check(before):
    return set(glob.glob(GEN + r"***.png", recursive=True)) - before
only = sys.argv[1:]
codex = shutil.which("codex")
for name, refs, scene in JOBS:
    if only and name not in only: continue
    out = OUT / f"{name}.png"
    if out.exists(): print("skip", name, flush=True); continue
    before = set(glob.glob(GEN + r"\**\*.png", recursive=True))
    task = f"Use the $imagegen skill to generate ONE image (landscape 16:9). Do not edit or create any other file. Prompt: {scene} Style: {A}"
    cmd = [codex, "exec", "--skip-git-repo-check", "-s", "read-only"] + sum([["-i", r] for r in refs], []) + ["--", task]
    t = time.time()
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore", timeout=1500, cwd=str(OUT))
    new = sorted(set(glob.glob(GEN + r"\**\*.png", recursive=True)) - before, key=os.path.getmtime)
    if new: shutil.copy(new[-1], out)
    else: print("  err:", (r.stderr or r.stdout or "")[-400:].replace(chr(10), " "), flush=True)
    print(name, "ok" if out.exists() else "FAIL", round(time.time() - t), "s", flush=True)
