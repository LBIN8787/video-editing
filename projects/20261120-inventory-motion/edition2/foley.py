from pathlib import Path
import os, wave
import numpy as np
work=Path(os.environ.get('INVENTORY_WORK',Path(__file__).resolve().parent))
audio=Path(os.environ.get('INVENTORY_AUDIO',work.parent))
with wave.open(str(audio/'voice.wav')) as f:
    r=f.getframerate()
    voice=np.frombuffer(f.readframes(f.getnframes()),'<i2').astype(float)/32768
rng=np.random.default_rng(581)
stereo=np.repeat(voice[:,None],2,axis=1)
def add(t,s,pan=0):
    i=round(t*r);n=min(len(s),len(stereo)-i)
    if n>0:stereo[i:i+n]+=s[:n,None]*np.array([np.cos((pan+1)*np.pi/4),np.sin((pan+1)*np.pi/4)])
def tap(t,pitch,amp,dec,pan):
    x=np.arange(round((dec*5)*r))/r
    wavelet=np.sin(2*np.pi*(pitch*x+1.4*(1-np.exp(-x/.016))))+.37*rng.uniform(-1,1,len(x))
    add(t,amp*wavelet*np.exp(-x/dec)*np.minimum(1,x/.003),pan)
def brush(t,seconds,amp,pan,grainrate):
    x=np.arange(round(seconds*r))/r;n=int(seconds*grainrate)+2
    noise=np.interp(x*grainrate,np.arange(n),rng.uniform(-1,1,n))
    add(t,amp*noise*np.sin(np.pi*x/seconds)**1.3,pan)
brush(1.44,.27,.065,.32,5600)
for t,pan in [(1.76,.25),(2.99,.35),(3.48,.48)]:tap(t,109,.084,.031,pan)
brush(5.70,.26,.029,.18,4200)
brush(9.30,.84,.065,.55,2600)
for t in np.arange(9.34,10.09,.09):tap(t,228,.027,.021,.54)
tap(10.14,68,.18,.056,.55)
for t,k in [(10.54,.1),(10.95,-.05),(12.02,.06)]:tap(t,111,.069,.037,k)
brush(15.12,.28,.036,-.4,5400);brush(17.66,.13,.024,.35,3500)
brush(19.63,.59,.042,-.46,2200);tap(20.29,85,.071,.039,-.39)
x=np.arange(round(2.04*r))/r
add(20.93,.023*np.sin(np.pi*x/2.04)**1.4*(np.sin(2*np.pi*(55*x+4*x*x))+.30*np.sin(2*np.pi*101*x)),.23)
for t in [23.93,24.19,24.48]:tap(t,140,.044,.027,-.35)
for t,d in [(25.53,.14),(25.73,.17),(25.98,.17)]:brush(t,d,.06,.41,5250)
brush(26.85,.48,.061,.15,3200)
brush(29.29,.19,.034,.35,2100);tap(29.55,87,.28,.043,.29);tap(29.57,159,.049,.036,.27)
with wave.open(str(work/'mix-v2.wav'),'wb') as f:
    f.setparams((2,2,r,0,'NONE','not compressed'))
    f.writeframes((np.clip(stereo,-.995,.995)*32767).astype('<i2').tobytes())
