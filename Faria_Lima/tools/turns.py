#!/usr/bin/env python3
"""대본 턴 내보내기/적용.
  export <대본.md> <턴.tsv>   : 번호\t화자\t포르투갈어\t한국어 (한국어는 화자명 제외)
  apply  <대본.md> <턴.tsv>   : tsv 내용으로 대본 턴을 교체. 화자 순서·턴 수가 바뀌면 중단.
"""
import re, sys
TURN = re.compile(r'^(\d+)\. ([^:]+): (.*)$')
KO = re.compile(r'^    ([^:]+): (.*)$')
def parse(md):
    L = open(md, encoding='utf-8').read().split('\n'); out = []
    for i, l in enumerate(L):
        m = TURN.match(l)
        if m:
            k = KO.match(L[i+1]); assert k, (md, i+1, L[i+1])
            out.append((i, int(m.group(1)), m.group(2), m.group(3), k.group(1), k.group(2)))
    return L, out
cmd, md, tsv = sys.argv[1:4]
L, T = parse(md)
if cmd == 'export':
    with open(tsv, 'w', encoding='utf-8') as f:
        for _, n, spk, pt, _, ko in T: f.write(f'{n}\t{spk}\t{pt}\t{ko}\n')
    print(md, len(T), 'turns exported')
elif cmd == 'apply':
    rows = [r.split('\t') for r in open(tsv, encoding='utf-8').read().split('\n') if r.strip()]
    assert len(rows) == len(T), ('턴 수 불일치', len(rows), len(T))
    for (i, n, spk, _, kname, _), r in zip(T, rows):
        assert len(r) == 4, ('열 수 오류', r)
        assert int(r[0]) == n and r[1] == spk, ('번호/화자 불일치', n, spk, r[:2])
        pt, ko = r[2].strip(), r[3].strip()
        assert pt and ko, ('빈 대사', n)
        w = len(re.findall(r"[\wÀ-ÿ'-]+", pt)); assert w <= 25, ('25단어 초과', n, w, pt)
        L[i] = f'{n:02d}. {spk}: {pt}'; L[i+1] = f'    {kname}: {ko}'
    open(md, 'w', encoding='utf-8').write('\n'.join(L)); print(md, 'applied')
