"""고른 Commons 파일을 내려받아 Drive real/ 에 저장 + credits.json (라이선스·작가·원본 주소)."""
import json, re, time, urllib.parse, urllib.request
from pathlib import Path
from commons import get, UA

OUT = Path(r"G:\내 드라이브\ytflow\영상\20261126-history-sohyeon\real"); OUT.mkdir(exist_ok=True)
FILES = {
 "R_sillok": "File:조선왕조실록 태백산사고본.jpg",
 "R_sillokpage": "File:조선왕조실록(중초본).jpg",
 "R_samjeondo": "File:Samjeondo Monument3.jpg",
 "R_namhan": "File:Korea Namhansanseong Fortress 35 (13956650139).jpg",
 "R_hwangyeong": "File:Korea-Seoul-Changgyeonggung-Hwangyeongjeon-01.jpg",
 "R_changgyeong": "File:Korea Changgyeonggung Daily Life 02 (8242692131).jpg",
 "R_mukden": "File:Mukden Palace drone view 1.jpg",
 "R_mukden2": "File:Mukden Palace 24465-Shenyang (30572854577).jpg",
 "R_observatory": "File:Beijing Ancient Observatory 1.jpg",
 "R_schall": "File:Portret van Johann Adam Schall von Bell, RP-P-1915-971.jpg",
 "R_shixian": "File:NCL-06339 大清順治十五年歲次戊戌時憲曆.pdf",
 "R_hongtaiji": "File:清 佚名 《清太宗崇德皇帝朝服像》.jpg",
 "R_shunzhi": "File:Emperor Shunzhi.jpg",
 "R_shanhai": "File:DV239 Shanhaiguan, China.jpg",
 "R_jingshan": "File:Stele of Emperor Chongzhen's death place in Jingshan Park.jpg",
 "R_charles": "File:The Execution of Charles I of England.jpg",
 "R_westphalia": "File:Westfaelischer Friede in Muenster (Gerard Terborch 1648).jpg",
 "R_jangneung": "File:Jangreung (Injo) 02.jpg",
 "R_yeonghoe": "File:Yeonghoewon Royal Tomb, Gwangmyeong (2020081317033300).jpg",
 "R_jeju": "File:Daepo Jusangjeolli Cliff 02.jpg",
 "R_hyojong": "File:Royal Tomb of King Hyojong 18.jpg",
 "R_obs5": "File:Beijing Ancient Observatory 5.jpg",
 "R_obs6": "File:Beijing Ancient Observatory 6.jpg",
 "R_obs3": "File:Beijing Ancient Observatory 3.jpg",
}
cred = {}
for k, t in FILES.items():
    d = get({"action": "query", "titles": t, "prop": "imageinfo", "iiprop": "url|size|extmetadata", "iiurlwidth": 1920, "format": "json"})
    p = next(iter(d.get("query", {}).get("pages", {}).values()), {})
    ii = (p.get("imageinfo") or [{}])[0]; m = ii.get("extmetadata", {})
    g = lambda x: re.sub("<[^>]+>", "", (m.get(x, {}) or {}).get("value", "")).strip()
    url = ii.get("thumburl") or ii.get("url")
    if not url: print("MISS", k); continue
    out = OUT / f"{k}.jpg"
    if not out.exists():
        for a in range(6):
            try:
                with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r: out.write_bytes(r.read())
                break
            except Exception as e:
                print("  retry", k, e); time.sleep(15 + 15 * a)
        time.sleep(6)
    cred[k] = dict(file=t, license=g("LicenseShortName"), artist=g("Artist")[:100], page=ii.get("descriptionurl"))
    print(k, cred[k]["license"], cred[k]["artist"][:40])
json.dump(cred, open(OUT / "credits.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
