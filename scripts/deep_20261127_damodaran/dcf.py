# 다모다란 앤트로픽 평가표(2026-11-18 수정판, 블로그 그림)를 다시 짠 단순 DCF — 매출 경로만 바꿔 주당 값을 봄 (이 채널 계산)
def run(g25=0.42, m=0.265, stc1=2.75, stc2=3.0, pfail=0.10, verbose=False):
    base=35282.0; revs=[base]; gs=[1.90]+[g25]*4+[g25-(g25-0.049)*k/5 for k in range(1,6)]
    for g in gs: revs.append(revs[-1]*(1+g))
    rev_tv=revs[10]*1.049
    margins=[0.05+(m-0.05)*min(k,4)/4 for k in range(10)]
    taxes=[0]*5+[0.05*k for k in range(1,6)]
    wacc=[0.0974]*5+[0.0974-(0.0974-0.0913)*k/5 for k in range(1,6)]
    pv=0; df=1
    for t in range(1,11):
        r=revs[t]; ebit=r*margins[t-1]*(1-taxes[t-1])
        nxt=revs[t+1] if t<10 else rev_tv
        reinv=(nxt-r)/(stc1 if t<=5 else stc2)
        df/= (1+wacc[t-1]); pv+=(ebit-reinv)*df
    tv_fcff=rev_tv*m*0.75*(1-0.049/0.15)
    tv=tv_fcff/(0.0913-0.049); pvtv=tv*df
    op=pv+pvtv; op_adj=op*(1-pfail*0.5)
    eq=op_adj-485319.79+202622.13
    ps=(eq-143395.12)/15901.84
    if verbose: print(f"y10 rev {revs[10]/1e3:,.0f}B op {op/1e3:,.0f}B pvtv share {pvtv/op:.1%} equity {eq/1e3:,.0f}B per share {ps:.2f}")
    return revs[10],ps
run(verbose=True)
# find growth for target y10 revenues
import math
for target in [1004,800,600,500,400,300]:
    lo,hi=0.0,0.6
    for _ in range(60):
        mid=(lo+hi)/2
        if run(mid)[0]/1e3<target: lo=mid
        else: hi=mid
    r,ps=run(mid); print(f"target {target}B -> g2-5 {mid:.1%} per share {ps:.2f}")
# price 82.79 implied
lo,hi=0.0,0.6
for _ in range(60):
    mid=(lo+hi)/2
    if run(mid)[1]<82.79: lo=mid
    else: hi=mid
print("price 82.79 implies y10 rev", run(mid)[0]/1e3, "g", mid)
print("CAGR 35.3->1004:", (1004.4/35.282)**0.1-1)
