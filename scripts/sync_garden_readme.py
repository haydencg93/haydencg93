#!/usr/bin/env python3
"""Refresh cache-busting hashes for the Garden Graph SVGs referenced by README.md."""
from pathlib import Path
import hashlib
import re

root = Path(__file__).resolve().parents[1]
readme = root / 'README.md'
source = readme.read_text(encoding='utf-8')
pattern = re.compile(
    r'(?P<url>\./assets/(?P<file>garden(?:-year|-mobile)?-(?:dark|light)\.svg))'
    r'(?:\?v=[a-fA-F0-9]+)?'
)
seen = set()

def update(match):
    filename = match.group('file')
    image = root / 'assets' / filename
    if not image.is_file():
        raise SystemExit(f'Missing generated image: {image}')
    seen.add(filename)
    digest = hashlib.sha256(image.read_bytes()).hexdigest()[:12]
    return f"{match.group('url')}?v={digest}"

updated = pattern.sub(update, source)
if not seen:
    raise SystemExit('No Garden Graph SVG references found in README.md')
if updated != source:
    readme.write_text(updated, encoding='utf-8')
print('Synced images:', ', '.join(sorted(seen)))
