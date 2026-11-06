from faster_whisper import WhisperModel
from pathlib import Path
import json,subprocess,numpy as np
r=Path(__file__).resolve().parent.parent
raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(r/'public/episode-003/voice.mp3'),'-ar','16000','-ac','1','-f','f32le','-'])
m=WhisperModel('small',device='cpu',compute_type='int8',cpu_threads=3)
segments,_=m.transcribe(np.frombuffer(raw,dtype=np.float32),language='ko',word_timestamps=True,beam_size=4,initial_prompt=(r/'research/episode-003/narration.txt').read_text())
words=[]
for seg in segments:
 print(seg.start,seg.end,seg.text,flush=True)
 words.extend(dict(text=w.word.strip(),startMs=round(w.start*1000),endMs=round(w.end*1000)) for w in seg.words)
(r/'research/episode-003/words.json').write_text(json.dumps(words,ensure_ascii=False,indent=2))
