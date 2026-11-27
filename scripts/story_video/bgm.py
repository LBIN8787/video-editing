"""잔잔한 배경음악 합성 (저작권 걱정 없는 자체 제작) — 낮은 피아노풍 화음 + 느린 분산화음 + 잔향.
python bgm.py <out.wav> <길이초> [목표 RMS dB, 기본 -34 = 말보다 약 13dB 낮게]
진행은 4개를 장마다 돌려 써서 21분이 단조롭지 않게."""
import sys, wave
import numpy as np
out, dur = sys.argv[1], float(sys.argv[2]); target = float(sys.argv[3]) if len(sys.argv) > 3 else -34.0
sr = 44100; n = int(sr * dur); x = np.zeros(n, np.float32)
def note(f, t0, length, amp):
    i0 = int(t0 * sr); L = int(length * sr); t = np.arange(L) / sr
    env = np.minimum(1, t / 0.02) * np.exp(-t / 2.8)
    w = (np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * 2 * f * t) + 0.12 * np.sin(2 * np.pi * 3 * f * t)) * env * amp
    e = min(n, i0 + L); x[i0:e] += w[:e - i0]
hz = lambda m: 440 * 2 ** ((m - 69) / 12)
PROGS = [[[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]],      # Am F C G
         [[50, 53, 57], [55, 58, 62], [48, 52, 55], [53, 57, 60]],      # Dm Gm C F
         [[57, 60, 64], [52, 55, 59], [53, 57, 60], [52, 56, 59]],      # Am Em F E
         [[48, 52, 55], [45, 48, 52], [53, 57, 60], [55, 59, 62]]]      # C Am F G
t, bar, k = 0.0, 8.0, 0
while t < dur - 1:
    prog = PROGS[(k // 16) % 4]; ch = prog[k % 4]
    for m in ch: note(hz(m - 12), t, 7.5, 0.22)
    for j, m in enumerate([ch[0], ch[1], ch[2], ch[1]]): note(hz(m + 12), t + j * 2.0, 4.0, 0.10)
    t += bar; k += 1
d = int(0.23 * sr); y = x.copy()
for g, dl in ((0.35, d), (0.2, 2 * d), (0.1, 3 * d)): y[dl:] += x[:-dl] * g
y = np.convolve(y, np.ones(40) / 40, "same")
f = int(3 * sr); y[:f] *= np.linspace(0, 1, f); y[-f:] *= np.linspace(1, 0, f)
y *= 10 ** (target / 20) / np.sqrt(np.mean(y ** 2))
z = (np.stack([np.clip(y, -1, 1)] * 2, 1) * 32767).astype(np.int16)
w = wave.open(out, "wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr); w.writeframes(z.tobytes()); w.close()
print("bgm", out, dur)
