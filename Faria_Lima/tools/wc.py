import re,sys
for s in sys.stdin.read().splitlines():
    print(len(re.findall(r"[\wÀ-ÿ'-]+", s)), s)
