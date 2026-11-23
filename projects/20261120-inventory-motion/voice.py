from pathlib import Path
import asyncio, json, subprocess
import edge_tts, numpy as np
root=Path.cwd()
lines=[
("6월 30일, 공장에서 세 상자를 포장했습니다.","유월 삼십 일, 공장에서 세 상자를 포장했습니다."),
("한 상자에 10만 원. 오늘 매출은 얼마일까요?","한 상자에 십만 원. 오늘 매출은 얼마일까요?"),
("출하가 하루 밀렸습니다.","출하가 하루 밀렸습니다."),
("문 앞에 쌓인 세 상자는 아직 재고입니다.","문 앞에 쌓인 세 상자는 아직 재고입니다."),
("이 계약에서는 고객이 물건을 받아야 매출이 됩니다.","이 계약에서는 고객이 물건을 받아야 매출이 됩니다."),
("다음 날, 트럭이 공장을 떠납니다.","다음 날, 트럭이 공장을 떠납니다."),
("고객이 세 상자를 받고 인수증에 서명합니다.","고객이 세 상자를 받고 인수증에 서명합니다."),
("그제야 7월 장부에 30만 원이 찍힙니다.","그제야 칠월 장부에 삼십만 원이 찍힙니다."),
]
async def get(i,ss):
    loc=root/f"take{i}.mp3"
    words=[]
    for trial in range(3):
        try:
            with loc.open("wb") as f:
                async for c in edge_tts.Communicate(ss,"ko-KR-InJoonNeural",rate="+0%",boundary="WordBoundary").stream():
                    if c["type"]=="audio": f.write(c["data"])
                    elif c["type"]=="WordBoundary": words.append([round(c["offset"]/1e7,3),c["text"]])
            break
        except Exception:
            if trial==2:raise
            words=[]
            await asyncio.sleep(1)
    out=subprocess.check_output(["ffmpeg","-v","error","-i",str(loc),"-f","s16le","-ac","1","-ar","48000","-"])
    pcm=np.frombuffer(out,np.int16)
    return pcm,words
async def main():
    import wave
    start=.24; audio=[np.zeros(round(48000*start),np.int16)]; timing=[]
    for i,(cap,ss) in enumerate(lines):
        pcm,w=await get(i,ss)
        idx=np.flatnonzero(abs(pcm.astype(float))>130)
        end=min(len(pcm),idx[-1]+int(.15*48000)) if len(idx) else len(pcm)
        pcm=pcm[:end]
        start=sum(len(x) for x in audio)/48000
        tail=[.4,.75,.37,.54,.63,.55,.65,1.55][i]
        audio.extend([pcm,np.zeros(round(48000*tail),np.int16)])
        timing.append(dict(cap=cap,start=start,end=start+len(pcm)/48000,words=w))
    with wave.open(str(root/"voice.wav"),"wb") as f:
        f.setparams((1,2,48000,0,"NONE","not compressed")); f.writeframes(np.concatenate(audio).tobytes())
    (root/"time.json").write_text(json.dumps(timing,ensure_ascii=False,indent=2),encoding="utf-8")
    print([(round(x['start'],2),round(x['end'],2)) for x in timing])
asyncio.run(main())
