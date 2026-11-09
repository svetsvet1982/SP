#!/usr/bin/env python3
"""대본 검사: 턴 수 120, 번호 연속, 1턴 25단어 이내."""
import re, sys
for src in sys.argv[1:]:
    nums, bad = [], []
    for l in open(src, encoding='utf-8'):
        m = re.match(r'(\d+)\.\s*([^:]+):\s*(.+)', l)
        if m:
            n = int(m.group(1)); nums.append(n)
            w = len(re.findall(r"[\wÀ-ÿ'-]+", m.group(3)))
            if w > 25: bad.append((n, w))
    ok = nums == list(range(1, 121))
    print(src, '턴', len(nums), '연속' if ok else '번호오류', '25단어 초과:', bad)
    if not ok or bad: sys.exit(1)
