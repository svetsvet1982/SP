#!/usr/bin/env python3
"""patch.py <원고.txt> <패치.txt>
패치 형식: 'DROP 접두어' 줄은 삭제, '접두어|새 포르투갈어[|새 한국어]' 줄은 교체,
'AFTER 접두어|새 줄 전체(NAME: pt || ko)' 는 삽입. 15단어 초과 시 중단."""
import re,sys
src,pf=sys.argv[1],sys.argv[2]
L=open(src,encoding='utf-8').read().split('\n')
def find(pre):
    idx=[i for i,l in enumerate(L) if l.startswith(pre)]
    assert len(idx)==1,(pre,len(idx)); return idx[0]
def wc(s): return len(re.findall(r"[\wÀ-ÿ'-]+",s))
for line in open(pf,encoding='utf-8').read().splitlines():
    if not line.strip(): continue
    if line.startswith('DROP '):
        del L[find(line[5:])]
    elif line.startswith('AFTER '):
        pre,new=line[6:].split('|',1)
        pt=new.split(': ',1)[1].split(' || ')[0]; assert wc(pt)<=15,(wc(pt),pt)
        L.insert(find(pre)+1,new)
    else:
        parts=line.split('|'); pre,newpt=parts[0],parts[1]
        assert wc(newpt)<=15,(wc(newpt),newpt)
        i=find(pre); spk,_,rest=L[i].partition(': '); pt,_,ko=rest.partition(' || ')
        L[i]=f'{spk}: {newpt} || {parts[2] if len(parts)>2 else ko}'
open(src,'w',encoding='utf-8').write('\n'.join(L))
print('ok')
