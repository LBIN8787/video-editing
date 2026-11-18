"""Render a model-independent picture edit. All media paths are relative to its bundle."""
from fractions import Fraction
from pathlib import Path
from tempfile import TemporaryDirectory
import hashlib
import json
import subprocess
import sys

import av
from PIL import Image
from stage_layers import frames

def render(bundle,edition):
    folder=bundle/edition
    plan=json.loads((folder/"edition.json").read_text(encoding="utf-8-sig"))
    fps=plan["fps"]
    if fps!=30: raise ValueError("이 렌더러의 노출표는 30fps입니다.")
    total=plan["total_frames"]
    schedule=plan["shots"]
    starts=[s["at"] for s in schedule]
    if not starts or starts[0]!=0 or starts!=sorted(set(starts)) or starts[-1]>=total:
        raise ValueError("컷의 시작 또는 종료 프레임 오류")
    inputs=plan["input_sha256"]
    required={"captions.ass","voice.m4a"}
    for shot in schedule:
        if "still" in shot:
            required.add(shot["still"])
        else:
            stage=shot["composition"]
            required.add(stage["back"])
            required.update(layer["file"] for layer in stage["layers"])
    for name in required:
        path=(folder/name).resolve()
        if not path.is_relative_to(bundle) or hashlib.sha256(path.read_bytes()).hexdigest()!=inputs[name]:
            raise ValueError(f"입력 판본 확인 필요: {name}")
    with TemporaryDirectory(dir=folder) as temporary:
        tmp=Path(temporary)
        with av.open(str(tmp/"exposures.mp4"),"w") as output:
            video=output.add_stream("libx264",rate=fps)
            video.width,video.height=1920,1080
            video.pix_fmt="yuv420p"
            video.codec_context.time_base=Fraction(1,fps)
            video.options={"bf":"0","crf":"15","preset":"veryfast","threads":"5"}
            def record(image,tick):
                vf=av.VideoFrame.from_image(image).reformat(width=1920,height=1080,format="yuv420p",interpolation="BICUBIC")
                vf.pts=tick
                vf.time_base=Fraction(1,fps)
                for packet in video.encode(vf): output.mux(packet)
            for shot,end in zip(schedule,starts[1:]+[total]):
                if "still" in shot:
                    with Image.open(folder/shot["still"]) as im:
                        last=im.convert("RGB")
                    at=shot["at"]
                    record(last,at)
                else:
                    for at,last in frames(folder,shot,end): record(last,at)
            if at<total-1: record(last,total-1)
            for packet in video.encode(): output.mux(packet)
        ff=["ffmpeg","-v","error","-nostdin","-y"]
        picture=tmp/"picture.mp4"
        subprocess.run(ff+["-i",str(tmp/"exposures.mp4"),"-filter_threads","3","-vf",
                         "fps=30,setsar=1,ass=captions.ass:fontsdir=../fonts","-frames:v",str(total),
                         "-c:v","libx264","-threads","6","-preset","veryfast","-crf","17",str(picture)],cwd=folder,check=True)
        final=tmp/"review.mp4"
        subprocess.run(ff+["-i",str(picture),"-i","voice.m4a","-map","0:v:0","-map","1:a:0","-c","copy",
                           "-movflags","+faststart",str(final)],cwd=folder,check=True)
        n=subprocess.check_output(["ffprobe","-v","error","-select_streams","v","-show_entries","stream=nb_frames",
                                   "-of","csv=p=0",str(final)])
        if int(n)!=total: raise ValueError("검토본 프레임 수 불일치")
        final.replace(folder/"review.mp4")

if __name__=="__main__":
    render(Path(sys.argv[1]).resolve(),sys.argv[2])
