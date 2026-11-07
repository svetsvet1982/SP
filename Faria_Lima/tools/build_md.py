#!/usr/bin/env python3
"""간이 원고(.txt) → 대본 .md 빌더.
원고 형식:
  @헤더 블록은 그대로 복사 (첫 줄 ~ '## 대본' 이전)
  '### 장면' 줄은 그대로
  'NOME: frase || 번역' 줄은 번호를 자동으로 매김 (한국어 화자명은 KO 매핑 사용)
  '## 다음 화 예고' 이후는 그대로
"""
import sys, re
KO = {'HELENA':'엘레나','THIAGO':'치아구','BIA':'비아','RODRIGO':'호드리구','CAIO':'카이우',
      'ZULEICA':'조이레이카','CLÓVIS':'클로비스','WAGNER':'와그너','SÉRGIO':'세르지우','ROSE':'호지',
      'DONA ROSE':'도나 호지','EDINHO':'에지뉴','KIM':'김 여사','DANIEL':'다니엘','LEONARDO':'레오나르두',
      'RICARDO':'히카르두','ÂNGELO':'앙젤루','MARCELO':'마르셀루','GIOVANA':'지오바나','NEUSA':'네우자',
      'VALDIR':'발지르','JOSIANE':'조지아니','MARLENE':'마를레니','ELIAS':'엘리아스','DONA RITA':'도나 히타',
      'JUNIOR':'주니오르','MÁRCIO':'마르시우','SR. PARK':'박 사장','TATIANE':'타치아니','FÁBIO':'파비우','LURDES':'루르지스','EXPEDITO':'이스페지투'}
src, dst = sys.argv[1], sys.argv[2]
out, n, body = [], 0, False
for l in open(src, encoding='utf-8').read().splitlines():
    if l.startswith('## 대본'): body = True; out.append(l); continue
    if l.startswith('## 다음 화 예고'): body = False; out += ['---', '']
    m = re.match(r'([A-ZÀ-Ý. ]+):\s*(.+?)\s*\|\|\s*(.+)', l) if body else None
    if m:
        n += 1; name = m.group(1).strip()
        out += [f'{n:02d}. {name}: {m.group(2)}', f'    {KO.get(name, name)}: {m.group(3)}', '']
    elif body and l.startswith('### '):
        out += [l, '']
    elif body and not l.strip():
        continue
    else:
        out.append(l)
open(dst, 'w', encoding='utf-8').write('\n'.join(out).rstrip() + '\n')
print(dst, n, 'turns')
