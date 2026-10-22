#!/usr/bin/env python3
"""Generate pixel header/footer SVGs for the Arcade Greenhouse README."""
from pathlib import Path

P = Path(__file__).resolve().parents[1] / 'assets'
P.mkdir(exist_ok=True)

IV = '#F3F0E7'
SAGE = '#A7B69C'
MOSS = '#677D69'
FOREST = '#34483B'
DARK = '#292F2B'
BG = '#182521'
BROWN = '#7A6552'
LANTERN = '#E7D487'


def rect(x, y, w, h, c, extra=''):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{c}" {extra}/>'


def pixels(rows, x, y, s, palette):
    out = []
    for j, row in enumerate(rows):
        for i, key in enumerate(row):
            if key in palette:
                out.append(rect(x + i * s, y + j * s, s, s, palette[key]))
    return ''.join(out)

# Miso v1: neutral/cool frog, darker eyes, light belly, backpack and lantern.
MISO = [
    '..GGGG....',
    '.GGGGGG...',
    'GGKGGKGG..',
    'GGGGGGGG..',
    'GGDGGDGG..',
    '.GGGGGG...',
    '..GBBG.LL.',
    '.G....GLL.',
]
CLOUD = [
    '...WWW....',
    '..WWWWWW..',
    '.WWWWWWWW.',
    'WWWWWWWWWW',
    '.WWWWWWWW.',
]
palette = {'G': SAGE, 'K': DARK, 'D': FOREST, 'B': BROWN, 'L': LANTERN, 'W': IV}
style = '''<style>
@keyframes float{0%,100%{transform:translateY(0px)}50%{transform:translateY(-10px)}}
@keyframes hop{0%,100%{transform:translate(0,0)}50%{transform:translate(0,-6px)}}
.cloud{animation:float 5s ease-in-out infinite}
.miso{animation:hop 3.5s steps(2,end) infinite}
@media(prefers-reduced-motion:reduce){.cloud,.miso{animation:none}}
</style>'''

svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 280" role="img" aria-label="Hayden Arcade Greenhouse pixel-art banner">', style, rect(0, 0, 1000, 280, BG)]
for i in range(26):
    x = (i * 173 + 53) % 950
    y = (i * 67 + 14) % 148
    svg.append(rect(x, y, 4, 4, IV if i % 3 == 0 else MOSS))
for i in range(30):
    x = i * 36 - 12
    h = 35 + ((i * 13) % 55)
    svg.append(rect(x, 245 - h, 36, h, FOREST if i % 2 else '#273C31'))
for x in (24, 90, 865, 938):
    for layer in range(4):
        svg.append(rect(x + 20 - layer * 7, 112 + layer * 22, 28 + layer * 14, 19, FOREST if x % 3 else MOSS))
    svg.append(rect(x + 31, 196, 7, 49, BROWN))
svg.append(rect(0, 247, 1000, 9, MOSS))
svg.append(rect(0, 256, 1000, 24, DARK))
svg += [
    rect(145, 45, 647, 153, DARK),
    rect(150, 50, 637, 143, BG),
    rect(162, 63, 5, 115, MOSS),
    rect(174, 181, 600, 3, MOSS),
]
svg.append(f'<text x="188" y="107" fill="{IV}" font-size="38" font-family="monospace" font-weight="900" letter-spacing="2">HAYDEN // ARCADE</text>')
svg.append(f'<text x="188" y="153" fill="{SAGE}" font-size="39" font-family="monospace" font-weight="900" letter-spacing="1">GREENHOUSE</text>')
svg.append(f'<text x="188" y="175" fill="{IV}" font-size="13" font-family="monospace" letter-spacing="2">CODE / BUILD / EXPLORE / GROW</text>')
svg.append('<g class="cloud">' + pixels(CLOUD, 820, 42, 9, palette) + '</g>')
svg.append('<g class="miso">' + pixels(MISO, 810, 176, 7, palette) + '</g>')
svg.append('</svg>')
(P / 'arcade-header.svg').write_text('\n'.join(svg), encoding='utf-8')

svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 120" role="img" aria-label="Arcade greenhouse footer with Miso and Mochi">', style, rect(0, 0, 1000, 120, BG), rect(0, 98, 1000, 6, MOSS)]
svg += [
    f'<text x="60" y="51" fill="{IV}" font-size="25" font-family="monospace" font-weight="bold">SAVE POINT REACHED.</text>',
    f'<text x="60" y="76" fill="{SAGE}" font-size="16" font-family="monospace">small commits // big growth</text>',
]
svg += ['<g class="cloud">' + pixels(CLOUD, 713, 20, 8, palette) + '</g>', '<g class="miso">' + pixels(MISO, 842, 35, 7, palette) + '</g>', '</svg>']
(P / 'arcade-footer.svg').write_text('\n'.join(svg), encoding='utf-8')
print('Generated header and footer SVGs')
