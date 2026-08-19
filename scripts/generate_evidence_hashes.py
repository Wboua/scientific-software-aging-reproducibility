#!/usr/bin/env python3
from pathlib import Path
import hashlib
ROOT = Path(__file__).resolve().parents[1]
for case in sorted((ROOT/'evidence').glob('PS[0-9][0-9][0-9]')):
    targets=[]
    for sub in ('raw','outputs','environment','interventions'):
        d=case/sub
        if d.exists():
            targets += [p for p in d.rglob('*') if p.is_file() and p.name != '.gitkeep']
    hdir=case/'hashes'; hdir.mkdir(exist_ok=True)
    out=hdir/'SHA256SUMS_EVIDENCE.txt'
    with out.open('w',encoding='utf-8',newline='\n') as f:
        for p in sorted(targets):
            digest=hashlib.sha256(p.read_bytes()).hexdigest()
            f.write(f"{digest}  {p.relative_to(case).as_posix()}\n")
    print(case.name, len(targets), 'files')
