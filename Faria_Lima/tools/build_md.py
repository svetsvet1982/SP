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
      'JUNIOR':'주니오르','MÁRCIO':'마르시우','SR. PARK':'박 사장','TATIANE':'타치아니','FÁBIO':'파비우','LURDES':'루르지스','EXPEDITO':'이스페지투','OPERÁRIO':'노동자','SANDRA':'산드라','SEU DITO':'세우 지투','EDSON':'에지송','ROGÉRIO':'호제리우','FURTADO':'푸르타두','OTÁVIO':'오타비우','MÁRCIA':'마르시아','KAUÃ':'카우앙','INGRID':'잉그리드','CRISTINA':'크리스치나','LOPES':'로피스','HAROLDO':'아롤두','OPERÁRIA':'여성 노동자','ERNESTO':'에르네스투','SEU JAIR':'세우 자이르','AUGUSTO':'아우구스투','HENRIQUE':'엔히키','VALÉRIA':'발레리아','DÉBORA':'데보라','ADVOGADO':'변호사','DONA MARIA':'도나 마리아','FARMACÊUTICO':'약사','NICOLA':'니콜라','WELLINGTON':'웰링톤','ZÉ CARLOS':'제 카를루스','BIGODE':'비고지','PAULA':'파울라','TORCEDOR':'팬','DONA NEIDE':'도나 네이지','SÓCIO':'회원','OSVALDO':'오스발두','MARIANA':'마리아나','COOPERADO':'조합원','COOPERADA':'여성 조합원','TONICO':'토니쿠','FERNANDA':'페르난다','LUCAS':'루카스','ANALISTA':'애널리스트','INVESTIDOR':'투자위원','DONA SOCORRO':'도나 소코후','GARÇOM':'웨이터','LÚCIA':'루시아','NELSON':'넬송','FRED':'프레드','RENATA':'헤나타','CARDIM':'카르딩','DONA CIDA':'도나 시다','JORNALEIRO':'신문 가판대 주인','APRESENTADOR':'앵커','GIL':'질','AURÉLIO':'아우렐리우','JURANDIR':'주란지르','TATI':'타치','SIMONE':'시모니','MEDIADOR':'사회자','RAIMUNDO':'하이문두','DURVAL':'두르바우','ELEITOR':'유권자','ELEITORA':'여성 유권자','HOMEM':'남성 참가자','MULHER':'여성 참가자','IVONE':'이보니','JEFFERSON':'제페르송','KÁTIA':'카치아','DAVI':'다비','PERITO':'감정사'}
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
