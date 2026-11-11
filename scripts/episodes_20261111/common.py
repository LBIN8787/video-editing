import json, subprocess, shutil
from pathlib import Path
ROOT=Path('/home/user/video-editing'); NASA=Path('/tmp/claude-0/-home-user/29c7e7c2-ab5e-5f3f-ac0c-a57433d47dc6/scratchpad/nasa')
NASA_META={
 "iss066e158841":("서울 야경 · NASA 국제우주정거장 사진 (2022, 퍼블릭 도메인)",),
 "iss037e005370":("서울 야경 · NASA 국제우주정거장 사진 (2013, 퍼블릭 도메인)",),
 "iss040e081462":("대만·일본 일대 야경 · NASA 국제우주정거장 사진 (2014, 퍼블릭 도메인)",),
 "iss037e002604":("샌프란시스코만 일대 야경 · NASA 국제우주정거장 사진 (2013, 퍼블릭 도메인)",),
 "STS059-50-003":("뉴욕 야경 · NASA 우주왕복선 STS-59 사진 (1994, 퍼블릭 도메인)",),
 "LRC-1957-B701_P-05391":("IBM 704 컴퓨터 · NASA 랭글리 연구소 (1957, 퍼블릭 도메인)",),
 "ARC-2008-ACD08-0272-001":("NASA 슈퍼컴퓨터 플레이아데스 · NASA 에임스 연구소 (2008, 퍼블릭 도메인)",),
 "ARC-2008-ACD08-0272-005":("NASA 슈퍼컴퓨터 플레이아데스 · NASA 에임스 연구소 (2008, 퍼블릭 도메인)",),
 "iss040e091715":("베이징 일대 야경 · NASA 국제우주정거장 사진 (2014, 퍼블릭 도메인)",),
}
def project(name, channel, skin, note, footage, brief, factsheet, spec):
    P=ROOT/'projects'/name
    for d in ('01_research','02_script','04_assets/footage/raw'): (P/d).mkdir(parents=True, exist_ok=True)
    (P/'edit.yaml').write_text(f"# {note}\nedit:\n  style: hybrid\n  style_ref: hybrid\n  family: source\n  skin: {skin}\nchannel: {channel}\nformat: longform\n",encoding='utf-8')
    (P/'state.json').write_text(json.dumps({"name":name,"created":"2026-11-11T09:00:00","done":["script"]},ensure_ascii=False,indent=1))
    fo={}
    for key,nid in footage.items():
        src=NASA/f"{nid}.jpg"; shutil.copy(src,P/f'04_assets/footage/raw/{key}.jpg')
        out=P/f'04_assets/footage/{key}.mp4'
        if not out.exists():
            subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-loop","1","-i",str(src),"-t","30","-vf","scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,fps=30","-c:v","libx264","-preset","veryfast","-crf","20","-pix_fmt","yuv420p",str(out)],check=True)
        fo[key]={"file":f"{key}.mp4","credit":NASA_META[nid][0]+f" · {nid}","url":f"https://images.nasa.gov/details/{nid}"}
    spec["footage"]=fo
    for i,s in enumerate(spec["scenes"],1): s["id"]=i
    (P/'01_research/topic_brief.json').write_text(json.dumps(brief,ensure_ascii=False,indent=1),encoding='utf-8')
    (P/'01_research/factsheet.md').write_text(factsheet,encoding='utf-8')
    (P/'02_script/hybrid.json').write_text(json.dumps(spec,ensure_ascii=False,indent=1),encoding='utf-8')
    n=sum(len(b['say']) for s in spec['scenes'] for b in s['beats'])
    print(name, len(spec['scenes']),'scenes', n,'chars')
def B(*xs): return [{"say":x} if isinstance(x,str) else x for x in xs]
