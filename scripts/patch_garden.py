#!/usr/bin/env python3
"""Patch upstream Garden Graph with Miso. Fails loudly if upstream changes unexpectedly."""
from pathlib import Path
import re
import sys

source = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('upstream/render.py')
text = source.read_text(encoding='utf-8')
start = text.find('def gardener(th, start, end, dur):')
stop = text.find('\ndef today_label(', start)
if start < 0 or stop < 0 or text.count('def gardener(th, start, end, dur):') != 1:
    raise SystemExit('Garden Graph gardener API has changed; update patch instead of silently rendering wrong art')

frog = '''def gardener(th, start, end, dur):
    """Miso the frog: a sage/moss pixel explorer with satchel and lantern.

    Retains Garden Graph's walk/turn/bob CSS behavior and today's tile path.
    All geometry is local to (0, 0), as expected by upstream render().
    """
    green = mix("#677D69", NIGHT, 0.12) if th.dark else "#677D69"
    sage = mix("#A7B69C", NIGHT, 0.07) if th.dark else "#A7B69C"
    ink = "#182521"
    ivory = "#F3F0E7"
    brown = "#7A6552"
    glow = "#E7D487"
    walk = (f'style="--x0:{start[0]:.1f}px;--y0:{start[1]:.1f}px;'
            f'--x1:{end[0]:.1f}px;--y1:{end[1]:.1f}px;'
            f'animation-duration:{dur:.0f}s"')
    # 14x15 logical pixel sprite. No raster images, no remote dependencies.
    rows = (
        '....GG..GG....',
        '...GSSGGSSG...',
        '..GSSSSSSSSG..',
        '..GSKSSSSKSG..',
        '..GSSSSSSSSG..',
        '...GSSSSSSG...',
        '....GSSSSG....',
        '...GGGGGGGG...',
        '..GGGSSSSGGG..',
        '..GBGSSSSGGG..',
        '..GBGGGGGGGG..',
        '...BGGGGGG....',
        '....GG..GG....',
        '....GG..GG....',
    )
    colors = {'G': green, 'S': sage, 'K': ink, 'B': brown}
    pix = []
    for yy, row in enumerate(rows):
        for xx, key in enumerate(row):
            if key in colors:
                pix.append(f'<rect x="{(xx - 7)*1.55:.2f}" y="{(yy - 13)*1.55:.2f}" '
                           f'width="1.55" height="1.55" fill="{colors[key]}"/>')
    # Small field lantern held close to Miso's front arm so it reads as hand-held, not floating.
    lantern = (
        f'<line x1="4.2" y1="-9.4" x2="5.7" y2="-8.0" stroke="{brown}" stroke-width=".7" stroke-linecap="round"/>'
        f'<rect x="5.2" y="-8.9" width="2.4" height="2.9" fill="{brown}"/>'
        f'<rect x="5.65" y="-8.35" width="1.5" height="1.7" fill="{glow}"/>'
        f'<rect x="5.65" y="-9.6" width="1.5" height=".7" fill="{ivory}"/>'
    )
    return (f'<g class="walk" {walk}>'
            '<ellipse cx="0" cy="2" rx="9.5" ry="2.1" fill="#000" opacity=".20"/>'
            f'<g class="turn" style="animation-duration:{dur:.0f}s">'
            '<g class="bob">'
            + ''.join(pix) + lantern + '</g></g></g>')

'''
patched = text[:start] + frog + text[stop + 1:]

# Preserve the original seasonal ecosystem and its seasonal variants; recolor northern seasons.
replacements = {
    'spring': '"spring": dict(ground="#DCE6D5", side="#A7B69C", leaf="#7E9A78", leaf2="#677D69", accent="#F3F0E7", heads=("#F3F0E7",), blossom="#F3F0E7"),',
    'summer': '"summer": dict(ground="#AFC79F", side="#7E9A78", leaf="#677D69", leaf2="#34483B", accent="#E7D487", heads=("#F3F0E7", "#E7D487"), core="#7A6552", fruit="#E7D487"),',
    'autumn': '"autumn": dict(ground="#C9C2A6", side="#9A8F70", leaf="#7A855F", leaf2="#5D684A", accent="#E7D487", heads=("#E7D487", "#F3F0E7")),',
    'winter': '"winter": dict(ground="#EAE9E2", side="#B8B6AA", leaf="#4F6A57", leaf2="#34483B", accent="#A7B69C", tree="pine", shrub=True, snow=True, sprout_leaf="#677D69"),',
}
# Match multiline seasonal entries; each is terminated by the next season key.
for name, new in replacements.items():
    pat = re.compile(r'^    "' + name + r'": dict\(.*?(?=^    "[a-z-]+": dict\(|^    # South Asia)', re.M | re.S)
    patched, n = pat.subn('    ' + new + '\n', patched)
    if n != 1:
        raise SystemExit(f'Could not safely update {name} palette; matched {n}')

source.write_text(patched, encoding='utf-8')
print('Applied Miso frog and sage seasons to upstream Garden Graph:', source)
