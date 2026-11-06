from pathlib import Path
import json,math,subprocess
import numpy as np
from supertonic import TTS
from faster_whisper import WhisperModel
R=Path(__file__).resolve().parent.parent
samples={
 'AI001Review':[(x['name'],x['text']) for x in json.loads((R/'research/timeline.json').read_text())],
 'Quiz001':[
 ('Question','둘레가 같으면, 넓이도 같을까요? 에이와 비 중에 골라 보세요.'),
 ('Conditions','에이는 가로 세로 오. 비는 가로 칠, 세로 삼입니다. 둘레는 둘 다 이십이에요.'),
 ('Think','그런데 안쪽을 채우는 칸의 수를 세어 보면, 답이 달라져요.'),
 ('Solve','에이는 오 곱하기 오, 이십오. 비는 칠 곱하기 삼, 이십일이죠.'),
 ('Answer','정답은 에이. 둘레가 같다고 넓이까지 같은 건 아니에요.'),
 ('Comment','어느 쪽을 골랐나요? 처음 생각한 이유도 알려 주세요.')],
 'Quiz002':[
 ('Question','이십 퍼센트 할인하고, 다시 이십 퍼센트 올리면 원래 가격일까요?'),
 ('Conditions','가격을 백 원이라고 해 볼게요. 이십 퍼센트 할인하면 팔십 원이 됩니다.'),
 ('Think','그다음 올리는 이십 퍼센트는, 백 원이 아니라 팔십 원을 기준으로 계산해요.'),
 ('Solve','팔십 원의 이십 퍼센트는 십육 원. 그래서 팔십 더하기 십육은 구십육 원이에요.'),
 ('Answer','정답은 구십육 원. 같은 비율이라도 기준 금액이 달라서, 원래 가격으로 돌아오지 않아요.'),
 ('Comment','처음에는 백 원이라고 생각했나요? 헷갈렸던 지점을 알려 주세요.')]
}
tts=TTS(auto_download=True,intra_op_num_threads=2,inter_op_num_threads=1);style=tts.get_voice_style(voice_name='F3')
for key,lines in samples.items():
 folder=R/'public/review-samples'/key;folder.mkdir(parents=True,exist_ok=True);items=[]
 for i,(name,text) in enumerate(lines):
  wav,d=tts.synthesize(text=text,voice_style=style,lang='ko',total_steps=14,speed=1.05,silence_duration=.2)
  file=folder/f'voice-{i}.wav';tts.save_audio(wav,str(file));seconds=float(np.asarray(d).reshape(-1)[0])
  items.append(dict(name=name,text=text,audio=str(file.relative_to(R/'public')),frames=math.ceil(seconds*30)+3))
 (folder/'timing.json').write_text(json.dumps(items,ensure_ascii=False,indent=2));print(key,'voice ready',sum(x['frames'] for x in items)/30,flush=True)
m=WhisperModel('small',device='cpu',compute_type='int8',cpu_threads=3)
for key in samples:
 folder=R/'public/review-samples'/key;items=json.loads((folder/'timing.json').read_text())
 for item in items:
  raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(R/'public'/item['audio']),'-ar','16000','-ac','1','-f','f32le','-'])
  segments,_=m.transcribe(np.frombuffer(raw,dtype=np.float32),language='ko',word_timestamps=True,beam_size=4,initial_prompt=item['text'])
  words=[];recognized=[]
  for s in segments:
   recognized.append(s.text);words.extend(dict(text=w.word,startMs=round(w.start*1000),endMs=round(w.end*1000)) for w in s.words)
  caps=[];g=[]
  for j,w in enumerate(words):
   g.append(w);text=''.join(t['text'] for t in g).strip()
   if len(text)>=16 or j==len(words)-1 or w['text'].endswith(('.', '?', '!')):
    for a,b in [('에이아이','AI'),('에이는','A는'),('비는','B는'),('에이와 비','A와 B'),('정답은 에이','정답은 A'),('이십 퍼센트','20%'),('피피티','PPT')]:text=text.replace(a,b)
    caps.append(dict(text=text,startMs=g[0]['startMs'],endMs=max(g[0]['startMs']+50,g[-1]['endMs']),timestampMs=g[0]['startMs'],confidence=None,pageBreakAfter=True));g=[]
  for a,b in zip(caps,caps[1:]):a['endMs']=min(a['endMs'],b['startMs']-1)
  item.update(captions=caps,recognizedText=' '.join(recognized));print(key,item['name'],item['recognizedText'],flush=True)
 (folder/'timing.json').write_text(json.dumps(items,ensure_ascii=False,indent=2))
