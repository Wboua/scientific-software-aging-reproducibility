#!/usr/bin/env python3
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
issues=[]
citation=(ROOT/'CITATION.cff').read_text(encoding='utf-8')
if 'REPLACE_WITH_REPOSITORY' in citation: issues.append('Set the public GitHub repository URL in CITATION.cff.')
if 'REPLACE_WITH_ZENODO_DOI' in citation: issues.append('Reserve/publish the Zenodo DOI and set it in CITATION.cff.')
if not any((ROOT/name).exists() for name in ('LICENSE','LICENSE.md','LICENSE.txt')):
    issues.append('Select and add a repository license before public release.')
if issues:
    print('Pre-release items still open:')
    for i in issues: print('-',i)
    sys.exit(1)
print('Pre-release metadata: PASS')
