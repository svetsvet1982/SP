import re,sys
for l in open(sys.argv[1],encoding='utf-8'):
    m=re.match(r'(\d+)\.\s*([^:]+):\s*(.+)',l)
    if m:
        w=len(re.findall(r"[\wÀ-ÿ'-]+",m.group(3)))
        if w>25: print(w, m.group(2)+': '+m.group(3))
