#!/usr/bin/env python3
"""턴 길이 검사: python3 tools/check_len.py <파일.md>...
기준(부별): 평균 목표, 상한, 30단어 이상 턴 최소 개수."""
import re,sys,statistics
RULE={1:(14,35,6),2:(15,40,8),3:(16,45,9),4:(17,50,10)}  # 평균 하한, 단어 상한, 30+단어 최소 수
pat=re.compile(r'^(\d{3})\. ([A-ZÁÉÍÓÚÃÕÂÊÔÇ ]+): (.*)$')
ok_all=True
for f in sys.argv[1:]:
    b=int(re.search(r'(\d)부',f).group(1)); mean_min,cap,n30=RULE[b]
    lines=open(f).read().split('\n'); ws=[];nums=[];ko=0;over=[]
    for i,l in enumerate(lines):
        m=pat.match(l)
        if m:
            n=len(m.group(3).split()); ws.append(n); nums.append(int(m.group(1)))
            if n>cap: over.append(f'{m.group(1)}:{n}')
            if i+1<len(lines) and lines[i+1].startswith('     ') and lines[i+1].strip(): ko+=1
    short=sum(w<=8 for w in ws)/len(ws); long_=sum(w>=21 for w in ws)/len(ws); c30=sum(w>=30 for w in ws)
    mean=statistics.mean(ws)
    ok=(len(ws)==150 and nums==list(range(1,151)) and ko==150 and mean>=mean_min and not over and c30>=n30 and 0.2<=short<=0.4 and long_>=0.25)
    ok_all&=ok
    print(f"{'OK ' if ok else 'NG '}{f}: turns={len(ws)} seq={nums==list(range(1,151))} ko={ko} mean={mean:.1f}(>={mean_min}) short<=8={short:.0%}(20~40%) long>=21={long_:.0%}(>=25%) n30={c30}(>={n30}) over{cap}={over}")
sys.exit(0 if ok_all else 1)
