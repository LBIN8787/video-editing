"""Local Whisper transcription; keeps raw recognition for review, never calls TTS."""
import argparse, json, subprocess, time
from pathlib import Path
import numpy as np
from faster_whisper import WhisperModel

p = argparse.ArgumentParser()
p.add_argument('--audio', type=Path, required=True)
p.add_argument('--out', type=Path, required=True)
p.add_argument('--prompt', type=Path, required=True)
a = p.parse_args()
started = time.monotonic()
samples = subprocess.check_output(['ffmpeg', '-v', 'error', '-i', str(a.audio), '-ar', '16000', '-ac', '1', '-f', 'f32le', '-'])
model = WhisperModel('small', device='cpu', compute_type='int8', cpu_threads=4)
segments, info = model.transcribe(np.frombuffer(samples, dtype=np.float32), language='ko', word_timestamps=True, beam_size=5, initial_prompt=a.prompt.read_text(encoding='utf-8'))
words, lines = [], []
for segment in segments:
    lines.append({'start': segment.start, 'end': segment.end, 'text': segment.text})
    words.extend({'text': w.word.strip(), 'startMs': round(w.start * 1000), 'endMs': round(w.end * 1000)} for w in segment.words)
a.out.parent.mkdir(parents=True, exist_ok=True)
a.out.write_text(json.dumps({'model': 'small', 'implementation': 'faster-whisper', 'language': info.language, 'elapsed_seconds': round(time.monotonic() - started, 2), 'segments': lines, 'words': words}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'out': str(a.out), 'words': len(words), 'elapsed_seconds': round(time.monotonic() - started, 2)}), flush=True)
