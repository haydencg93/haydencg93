#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'
ASSETS.mkdir(exist_ok=True)

IV = '#F3F0E7'
SAGE = '#A7B69C'
MOSS = '#677D69'
FOREST = '#34483B'
DARK = '#292F2B'
BG = '#182521'
BROWN = '#7A6552'
GLOW = '#E7D487'

# Same logical sprite as patch_garden.py gardener() replacement.
FROG_ROWS = (
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

EYE_PIXELS = [(4,3), (9,3)]  # Same locations as K pixels in the graph mascot sprite.

def rect(x, y, w, h, c, extra=''):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{c}" {extra}/>'


def pixels(rows, x, y, s, palette):
    out = []
    for j, row in enumerate(rows):
        for i, key in enumerate(row):
            if key in palette:
                out.append(rect(x + i * s, y + j * s, s, s, palette[key]))
    return ''.join(out)


def same_miso_sprite(x, y, scale):
    # Draw the exact frog body colors used by the Garden Graph patch, but omit eye pixels so we can animate pupils.
    out = []
    palette = {'G': MOSS, 'S': SAGE, 'B': BROWN}
    for yy, row in enumerate(FROG_ROWS):
        for xx, key in enumerate(row):
            if key in palette:
                out.append(rect(x + xx * scale, y + yy * scale, scale, scale, palette[key]))
    eyes = []
    for ex, ey in EYE_PIXELS:
        eyes.append(rect(x + ex * scale, y + ey * scale, scale, scale, DARK))
    out.append(f'<g class="frog-eyes">{"".join(eyes)}</g>')
    return ''.join(out)


def cloud_pixels(x, y, s):
    rows = [
        '...WWW....',
        '..WWWWWW..',
        '.WWWWWWWW.',
        'WWWWWWWWWW',
        '.WWWWWWWW.',
    ]
    return pixels(rows, x, y, s, {'W': IV})

STYLE = '''<style>
@keyframes float{0%,100%{transform:translateY(0px)}50%{transform:translateY(-12px)}}
@keyframes look{0%,18%{transform:translateX(-1px)}28%,52%{transform:translateX(2px)}62%,82%{transform:translateX(0px)}100%{transform:translateX(-1px)}}
.cloud{animation:float 5s ease-in-out infinite}
.frog-eyes{animation:look 4.2s ease-in-out infinite;transform-box:fill-box;transform-origin:center}
@media(prefers-reduced-motion:reduce){.cloud,.frog-eyes{animation:none}}
</style>'''

# Header
svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 280" role="img" aria-label="Hayden Arcade Greenhouse pixel-art banner">', STYLE, rect(0,0,1000,280,BG)]
for i in range(26):
    x = (i * 173 + 53) % 950
    y = (i * 67 + 14) % 148
    svg.append(rect(x, y, 4, 4, IV if i % 3 == 0 else MOSS))
for i in range(30):
    x = i * 36 - 12
    h = 35 + ((i * 13) % 55)
    svg.append(rect(x, 245 - h, 36, h, FOREST if i % 2 else '#273C31'))
for x in (24, 90, 865, 938):
    canopy = MOSS if x < 200 else FOREST
    for layer in range(4):
        svg.append(rect(x + 20 - layer * 7, 112 + layer * 22, 28 + layer * 14, 19, canopy))
    svg.append(rect(x + 31, 196, 7, 49, BROWN))
svg.append(rect(0,247,1000,9,MOSS))
svg.append(rect(0,256,1000,24,DARK))
svg += [
    rect(145,45,647,153,DARK),
    rect(150,50,637,143,BG),
    rect(162,63,5,115,MOSS),
    rect(174,181,600,3,MOSS),
]
svg.append(f'<text x="188" y="107" fill="{IV}" font-size="38" font-family="monospace" font-weight="900" letter-spacing="2">HAYDEN // ARCADE</text>')
svg.append(f'<text x="188" y="153" fill="{SAGE}" font-size="39" font-family="monospace" font-weight="900" letter-spacing="1">GREENHOUSE</text>')
svg.append(f'<text x="188" y="175" fill="{IV}" font-size="13" font-family="monospace" letter-spacing="2">CODE  /  BUILD  /  EXPLORE  /  GROW</text>')
svg.append('<g class="cloud">' + cloud_pixels(820,42,9) + '</g>')
svg.append('<g>' + same_miso_sprite(818, 176, 6.4) + '</g>')
svg.append('</svg>')
(ASSETS/'arcade-header.svg').write_text('\n'.join(svg), encoding='utf-8')

# Footer
svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 120" role="img" aria-label="Arcade greenhouse footer with Miso and Mochi">', STYLE, rect(0,0,1000,120,BG), rect(0,98,1000,6,MOSS)]
svg += [
    f'<text x="60" y="51" fill="{IV}" font-size="25" font-family="monospace" font-weight="bold">SAVE POINT REACHED.</text>',
    f'<text x="60" y="76" fill="{SAGE}" font-size="16" font-family="monospace">small commits // big growth</text>',
]
svg.append('<g class="cloud">' + cloud_pixels(713,20,8) + '</g>')
svg.append('<g>' + same_miso_sprite(850, 42, 5.5) + '</g>')
svg.append('</svg>')
(ASSETS/'arcade-footer.svg').write_text('\n'.join(svg), encoding='utf-8')
print('Regenerated arcade-header.svg and arcade-footer.svg with the Garden Graph Miso sprite.')
