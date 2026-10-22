#!/usr/bin/env python3
"""Generate self-contained SVG pixel illustrations (no external dependencies)."""
from pathlib import Path
P=Path(__file__).resolve().parents[1]/'assets';P.mkdir(exist_ok=True)
IV='#F3F0E7';SAGE='#A7B69C';MOSS='#677D69';FOREST='#34483B';DARK='#292F2B'; BROWN='#7A6552';BG='#182521'
def rect(x,y,w,h,c):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{c}"/>'
def pixels(rows,x,y,s,pal):
 a=[]
 for j,row in enumerate(rows):
  for i,k in enumerate(row):
   if k in pal:a.append(rect(x+i*s,y+j*s,s,s,pal[k]))
 return ''.join(a)
FROG=['..GGGG..','.GGGGGG.','GGKGGKGG','GGGGGGGG','GGDGGDGG','.GGGGGG.','..GGGG..','.G....G.']
CLOUD=['...WWW....','..WWWWWW..','.WWWWWWWW.','WWWWWWWWWW','.WWWWWWWW.']
PAL={'G':SAGE,'K':DARK,'D':FOREST,'W':IV}
style='''<style>@keyframes float{0%,100%{transform:translateY(0px)}50%{transform:translateY(-12px)}}@keyframes hop{0%,100%{transform:translate(0,0)}50%{transform:translate(0,-6px)}}.cloud{animation:float 5s ease-in-out infinite}.frog{animation:hop 3.8s steps(2,end) infinite}@media(prefers-reduced-motion:reduce){.cloud,.frog{animation:none}}</style>'''
svg=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 280" role="img" aria-label="Hayden Arcade Greenhouse pixel-art banner">',style,rect(0,0,1000,280,BG)]
# pixels/stars
for i in range(26):
 x=(i*173+53)%950;y=(i*67+14)%148
 svg.append(rect(x,y,4,4,IV if i%3==0 else MOSS))
for i in range(30):
 x=i*36-12; h=35+((i*13)%55)
 svg.append(rect(x,245-h,36,h,FOREST if i%2 else '#273C31'))
# decorative tall pine towers
for x in (24,90,865,938):
 for layer in range(4):
  svg.append(rect(x+20-layer*7,112+layer*22,28+layer*14,19,FOREST if x%3 else MOSS))
 svg.append(rect(x+31,196,7,49,BROWN))
svg.append(rect(0,247,1000,9,MOSS)); svg.append(rect(0,256,1000,24,DARK))
# retro panel around title
svg += [rect(145,45,647,153,DARK),rect(150,50,637,143,BG),rect(162,63,5,115,MOSS),rect(174,181,600,3,MOSS)]
svg.append(f'<text x="188" y="107" fill="{IV}" font-size="38" font-family="monospace" font-weight="900" letter-spacing="2">HAYDEN // ARCADE</text>')
svg.append(f'<text x="188" y="153" fill="{SAGE}" font-size="39" font-family="monospace" font-weight="900" letter-spacing="1">GREENHOUSE</text>')
svg.append(f'<text x="188" y="175" fill="{IV}" font-size="13" font-family="monospace" letter-spacing="2">CODE  /  BUILD  /  EXPLORE  /  GROW</text>')
svg.append('<g class="cloud">'+pixels(CLOUD,820,42,9,PAL)+'</g>')
svg.append('<g class="frog">'+pixels(FROG,820,183,7,PAL)+'</g>')
svg.append('</svg>');(P/'arcade-header.svg').write_text('\n'.join(svg))
svg=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 120" role="img" aria-label="Arcade greenhouse footer with frog and cloud">',style,rect(0,0,1000,120,BG),rect(0,98,1000,6,MOSS)]
svg += [f'<text x="60" y="51" fill="{IV}" font-size="25" font-family="monospace" font-weight="bold">SAVE POINT REACHED.</text>',f'<text x="60" y="76" fill="{SAGE}" font-size="16" font-family="monospace">small commits // big growth</text>']
svg += ['<g class="cloud">'+pixels(CLOUD,713,20,8,PAL)+'</g>','<g class="frog">'+pixels(FROG,853,41,8,PAL)+'</g>','</svg>']
(P/'arcade-footer.svg').write_text('\n'.join(svg))
print('pixel assets generated')
