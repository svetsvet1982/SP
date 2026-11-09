#!/usr/bin/env python3
"""문체 지표: 턴당 평균 단어, 문장당 평균 단어, 3단어 이하 조각문/턴, 단문 턴(≤5단어) 비율, 긴 턴(≥15단어) 비율.
목표: 문장당 ≥7.0 · 조각문/턴 ≤0.35 · 턴당 평균 11~15 · 단문 턴 10~20% · 긴 턴 ≥20%."""
import re, sys, statistics as st
wc = lambda s: len(re.findall(r"[\wÀ-ÿ'-]+", s))
bad_any = False
for md in sys.argv[1:]:
    W = []; S = 0; frag = 0
    for l in open(md, encoding='utf-8'):
        m = re.match(r'^\d+\. [^:]+: (.*)$', l.rstrip())
        if not m: continue
        pt = m.group(1); W.append(wc(pt))
        sents = [s for s in re.split(r'[.!?…]+', pt) if re.search(r'\w', s)]
        S += len(sents); frag += sum(1 for s in sents if wc(s) <= 3)
    n = len(W); wps = sum(W)/S; fpt = frag/n; avg = st.mean(W)
    short = sum(w <= 5 for w in W)/n; long_ = sum(w >= 15 for w in W)/n
    ok = wps >= 7.0 and fpt <= 0.35 and 11 <= avg <= 15 and 0.10 <= short <= 0.20 and long_ >= 0.20
    bad_any |= not ok
    print(f"{'OK ' if ok else 'NG '}{md}: 턴당 {avg:.1f} · 문장당 {wps:.1f} · 조각문/턴 {fpt:.2f} · 단문턴 {short:.0%} · 긴턴 {long_:.0%}")
sys.exit(1 if bad_any else 0)
