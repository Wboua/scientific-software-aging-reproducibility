#!/usr/bin/env python3
from pathlib import Path
import csv, re, subprocess, sys
ROOT=Path(__file__).resolve().parents[1]
errors=[]
for i in range(1,11):
    cid=f'PS{i:03d}'
    c=ROOT/'evidence'/cid
    if not c.is_dir(): errors.append(f'missing {cid}')
    for name in ('metadata.yaml','claims.csv'):
        if not (c/name).exists(): errors.append(f'{cid}: missing {name}')
# Matrix shape
m=ROOT/'results'/'normalized'/'master_matrix.csv'
if not m.exists(): errors.append('missing master_matrix.csv')
else:
    rows=list(csv.DictReader(m.open(encoding='utf-8-sig',newline='')))
    if len(rows)!=10: errors.append(f'master_matrix has {len(rows)} rows, expected 10')
# No internal tool/editorial traces in public text files.
for p in ROOT.rglob('*'):
    if p.is_file() and p.suffix.lower() in {'.md','.txt','.csv','.yaml','.yml','.py','.tex','.bib','.json','.ps1','.sh','.cff'}:
        try: txt=p.read_text(encoding='utf-8-sig',errors='ignore')
        except Exception: continue
        forbidden = ('co'+'dex', 'chat'+'gpt', 'open'+'ai')
        if any(term.lower() in txt.lower() for term in forbidden): errors.append(f'internal tooling trace: {p.relative_to(ROOT)}')
if errors:
    print('Repository validation: FAIL')
    print('\n'.join(f'- {e}' for e in errors)); sys.exit(1)
print('Repository validation: PASS')
