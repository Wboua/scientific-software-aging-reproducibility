#!/usr/bin/env python3
from pathlib import Path
import hashlib, sys
ROOT=Path(__file__).resolve().parents[1]
errors=[]
for case in sorted((ROOT/'evidence').glob('PS[0-9][0-9][0-9]')):
    manifest=case/'hashes'/'SHA256SUMS_EVIDENCE.txt'
    if not manifest.exists():
        errors.append(f'{case.name}: missing manifest'); continue
    for line in manifest.read_text(encoding='utf-8-sig').splitlines():
        if not line.strip(): continue
        expected, rel=line.split(None,1); rel=rel.strip()
        p=case/rel
        if not p.exists(): errors.append(f'{case.name}: missing {rel}'); continue
        actual=hashlib.sha256(p.read_bytes()).hexdigest()
        if actual != expected: errors.append(f'{case.name}: hash mismatch {rel}')
if errors:
    print('\n'.join(errors)); sys.exit(1)
print('Evidence hashes: PASS')
