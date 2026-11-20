from pathlib import Path
import wave, numpy as np
R=48000; root=Path.cwd()
with wave.open(str(root/'voice.wav')) as f:
    speech=np.frombuffer(f.readframes(f.getnframes()),np.int16).astype(float)/32768
rng=np.random.default_rng(722)
fx=np.zeros_like(speech)
def add(time,v):
    i=round(time*R);n=min(len(v),len(fx)-i)
    if n>0:fx[i:i+n]+=v[:n]
def thunk(t,amp,pitch=120,life=.13):
    x=np.arange(round(life*R))/R
    env=np.exp(-x/(life*.22))*np.minimum(1,x/.003)
    v=amp*env*(.75*np.sin(2*np.pi*(pitch*x+2*(1-np.exp(-x/.013))))+.25*rng.uniform(-1,1,len(x)))
    add(t,v)
def rasp(t,dur,amp,rate=1400):
    n=round(dur*R);x=np.arange(n)/R
    noise=np.interp(np.arange(n)*rate/R,np.arange(int(dur*rate)+2),rng.uniform(-1,1,int(dur*rate)+2))
    add(t,amp*noise*np.sin(np.pi*np.arange(n)/n)**1.6)
for t in (1.28,2.02,2.83):
    rasp(t-.065,.12,.025,6500);thunk(t,.074,165,.095)
rasp(9.28,.66,.037,1900)
for i in range(8):thunk(9.35+i*.09,.013,220)
thunk(10.10,.12,84,.18)
for i in range(3):thunk(10.44+.54*i,.042,130,.075)
rasp(15.16,.29,.045,3600);rasp(17.61,.26,.025,3400)
rasp(19.78,.37,.04);thunk(20.23,.07,100)
for t in (20.93,21.11,21.29,24.55,24.84,25.13):thunk(t,.055,125,.12)
xx=np.arange(round(2*R))/R
add(21.41,.021*np.sin(np.pi*xx/2)**1.3*(np.sin(2*np.pi*(50*xx+4*xx**2))+.32*np.sin(2*np.pi*93*xx)))
for t,d in [(25.63,.13),(25.80,.20),(26.03,.17)]:rasp(t,d,.045,4200)
rasp(26.86,.42,.046,4500);rasp(29.30,.15,.032,2600)
thunk(29.53,.24,91,.18);thunk(29.56,.047,190,.09)
mix=speech+fx
with wave.open(str(root/'mix.wav'),'wb') as f:
    f.setparams((1,2,R,0,'NONE','not compressed'));f.writeframes((np.clip(mix,-.995,.995)*32767).astype('<i2').tobytes())
