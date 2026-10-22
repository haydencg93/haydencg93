#!/usr/bin/env python3
"""Update image URL versions for GitHub's image-proxy cache automatically."""
from pathlib import Path
import hashlib
import re
root=Path(__file__).resolve().parents[1]
readme=root/'README.md'
s=readme.read_text(encoding='utf-8')
count=0
for name in ('garden-dark.svg','garden-light.svg','garden-mobile-dark.svg','garden-mobile-light.svg'):
    image=root/'assets'/name
    if not image.exists():
        raise SystemExit('Missing generated file '+str(image))
    ver=hashlib.sha256(image.read_bytes()).hexdigest()[:12]
    pat=r'(\./assets/'+re.escape(name)+r')(?:\?v=[a-f0-9]+)?'
    s,n=re.subn(pat,lambda m:m.group(1)+'?v='+ver,s)
    if n!=1:
        raise SystemExit(f'Expected one reference to {name}, got {n}')
    count+=n
readme.write_text(s,encoding='utf-8')
print('Synced',count,'image references')
