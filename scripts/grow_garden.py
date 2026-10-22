#!/usr/bin/env python3
"""Generate Miso's contribution garden from GitHub contribution data.

This is a self-contained SVG renderer with no external dependencies.
Use --demo for bundled sample art; otherwise provide GH_USERNAME and GH_TOKEN.
"""
import argparse
import datetime as dt
import json
import os
import random
import urllib.request
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets' / 'contribution-garden.svg'

Q = 'query($login:String!){user(login:$login){contributionsCollection{contributionCalendar{weeks{contributionDays{date contributionCount contributionLevel}}}}}}'
LEVEL = {'NONE': 0, 'FIRST_QUARTILE': 1, 'SECOND_QUARTILE': 2, 'THIRD_QUARTILE': 3, 'FOURTH_QUARTILE': 4}

BG = '#182521'
PANEL = '#292F2B'
IV = '#F3F0E7'
SAGE = '#A7B69C'
MOSS = '#677D69'
FOREST = '#34483B'
DIRT = '#695A48'
SOIL = '#405044'
BROWN = '#7A6552'

DAY_NAMES = ['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT']


def r(x, y, w, h, c, extra=''):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{c}" {extra}/>'


def text(x, y, value, size, fill, anchor='start', weight='normal'):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="monospace" font-size="{size}" font-weight="{weight}" fill="{fill}">{escape(value)}</text>'


def get_days(user, token):
    data = json.dumps({'query': Q, 'variables': {'login': user}}).encode()
    req = urllib.request.Request(
        'https://api.github.com/graphql',
        data=data,
        headers={
            'Authorization': 'Bearer ' + token,
            'Content-Type': 'application/json',
            'User-Agent': 'hayden-miso-garden',
        },
    )
    with urllib.request.urlopen(req, timeout=30) as res:
        result = json.load(res)
    if result.get('errors'):
        raise RuntimeError(str(result['errors']))
    weeks = result['data']['user']['contributionsCollection']['contributionCalendar']['weeks']
    return {d['date']: d for w in weeks for d in w['contributionDays']}


def plant_sprite(level, x, y):
    out = [r(x, y, 31, 29, SOIL), r(x + 3, y + 3, 25, 23, [DIRT, '#506B4E', '#567A55', '#658B56', '#7F9F69'][level])]
    if level == 1:
        out += [r(x + 14, y + 11, 3, 11, IV), r(x + 9, y + 10, 7, 5, SAGE)]
    elif level == 2:
        out += [r(x + 14, y + 10, 3, 12, IV), r(x + 7, y + 11, 7, 5, SAGE), r(x + 17, y + 7, 8, 5, SAGE)]
    elif level == 3:
        out += [r(x + 14, y + 11, 3, 12, IV), r(x + 8, y + 8, 5, 6, SAGE), r(x + 18, y + 8, 5, 6, SAGE), r(x + 14, y + 4, 5, 6, IV)]
    elif level == 4:
        out += [r(x + 14, y + 15, 5, 9, BROWN), r(x + 7, y + 9, 19, 9, FOREST), r(x + 10, y + 4, 13, 9, SAGE)]
    return out


def miso_svg():
    return '''
    <g class="miso">
      <ellipse cx="0" cy="2" rx="7" ry="2.2" fill="#000" opacity=".2"/>
      <g class="turn">
        <g class="bob">
          <rect class="leg" x="-4.5" y="-3" width="2.2" height="3" rx=".8" fill="#677D69"/>
          <rect class="leg b" x="2.3" y="-3" width="2.2" height="3" rx=".8" fill="#677D69"/>
          <ellipse cx="0" cy="-6.6" rx="6.6" ry="5.2" fill="#677D69"/>
          <ellipse cx="0" cy="-5.7" rx="4.8" ry="3.2" fill="#A7B69C" opacity=".95"/>
          <rect x="3.9" y="-8.8" width="3" height="4.2" rx=".8" fill="#7A6552"/>
          <line x1="4.8" y1="-8.0" x2="8.2" y2="-10.7" stroke="#7A6552" stroke-width="1.2" stroke-linecap="round"/>
          <rect x="8.0" y="-12.4" width="2.4" height="2.4" fill="#E7D487"/>
          <ellipse cx="0" cy="-12.5" rx="7.3" ry="5.6" fill="#677D69"/>
          <circle cx="-3.5" cy="-15.8" r="2.0" fill="#677D69"/>
          <circle cx="3.5" cy="-15.8" r="2.0" fill="#677D69"/>
          <circle cx="-3.5" cy="-15.6" r="1.1" fill="#F3F0E7"/>
          <circle cx="3.5" cy="-15.6" r="1.1" fill="#F3F0E7"/>
          <circle cx="-3.4" cy="-15.6" r=".45" fill="#292F2B"/>
          <circle cx="3.6" cy="-15.6" r=".45" fill="#292F2B"/>
          <path d="M-2.3 -10.8 Q0 -9.7 2.3 -10.8" fill="none" stroke="#292F2B" stroke-width=".8" stroke-linecap="round"/>
        </g>
      </g>
    </g>'''


def cloud_svg(x, y, scale=1.0):
    return f'<g class="cloud" transform="translate({x} {y}) scale({scale})"><ellipse cx="0" cy="0" rx="18" ry="7" fill="{IV}"/><ellipse cx="-12" cy="-5" rx="10" ry="7" fill="{IV}"/><ellipse cx="10" cy="-6" rx="11" ry="8" fill="{IV}"/></g>'


def draw(days, demo=False):
    now = dt.datetime.now(dt.timezone.utc).date()
    sunday = now - dt.timedelta(days=(now.weekday() + 1) % 7)
    start = sunday - dt.timedelta(weeks=25)

    svg = [f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1050 440" role="img" aria-label="Miso's contribution garden based on GitHub activity">
    <style>
      .pulse{{animation:pulse 3s ease-in-out infinite}}
      @keyframes pulse{{0%,100%{{opacity:.35}}50%{{opacity:.9}}}}
      .walk{{animation:walk linear infinite}}
      @keyframes walk{{0%,100%{{transform:translate(var(--x0),var(--y0))}}50%{{transform:translate(var(--x1),var(--y1))}}}}
      .turn{{animation:turn linear infinite}}
      @keyframes turn{{0%,49.99%{{transform:scaleX(1)}}50%,100%{{transform:scaleX(-1)}}}}
      .bob{{animation:bob .7s ease-in-out infinite}}
      @keyframes bob{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-.7px)}}}}
      .leg{{transform-box:fill-box;transform-origin:50% 0;animation:leg 1.1s ease-in-out infinite}}
      .leg.b{{animation-delay:-.55s}}
      @keyframes leg{{0%,100%{{transform:rotate(-16deg)}}50%{{transform:rotate(16deg)}}}}
      .cloud{{animation:drift 10s linear infinite}}
      @keyframes drift{{from{{transform:translateX(-12px)}}to{{transform:translateX(12px)}}}}
      @media(prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
    </style>''']
    svg += [
        r(0, 0, 1050, 440, BG),
        r(12, 12, 1026, 416, FOREST),
        r(17, 17, 1016, 406, BG),
        text(34, 52, "[ MISO'S GARDEN GRAPH ]", 26, IV, weight='bold'),
        text(34, 78, 'REAL CONTRIBUTIONS / SOIL > SPROUT > BLOOM > TREE', 14, SAGE),
        r(30, 88, 990, 3, MOSS),
        text(1015, 52, 'DEMO // NOT LIVE' if demo else 'LIVE DATA', 15, IV, anchor='end'),
    ]
    svg.append(cloud_svg(900, 60, 1.1))

    for idx, label in enumerate(DAY_NAMES):
        svg.append(text(14, 138 + idx * 34, label, 10, SAGE))
    for w in range(26):
        month_day = start + dt.timedelta(days=w * 7)
        if w == 0 or month_day.day <= 7:
            svg.append(text(49 + w * 38, 108, month_day.strftime('%b').upper(), 10, SAGE, anchor='middle'))

    rng = random.Random(19)
    total = 0
    today_tile = (34, 120)
    for w in range(26):
        for daynum in range(7):
            day = start + dt.timedelta(days=w * 7 + daynum)
            if day > now:
                continue
            record = days.get(day.isoformat(), {})
            level = rng.choices(range(5), weights=[36, 31, 16, 11, 6])[0] if demo else LEVEL.get(record.get('contributionLevel', 'NONE'), 0)
            if not demo:
                total += record.get('contributionCount', 0)
            x = 34 + w * 38
            y = 120 + daynum * 34
            svg.extend(plant_sprite(level, x, y))
            if day == now:
                today_tile = (x, y)
                svg.append(f'<rect x="{x-1}" y="{y-1}" width="33" height="31" fill="none" stroke="{IV}" stroke-width="1.5" class="pulse"/>')

    svg += [r(806, 108, 205, 150, PANEL), r(810, 112, 197, 142, BG), text(824, 133, 'LEGEND', 14, IV, weight='bold')]
    labels = [('SOIL', 0), ('SPROUT', 1), ('BLOOM', 2), ('FLOWER', 3), ('TREE', 4)]
    for i, (label, level) in enumerate(labels):
        yy = 130 + 18 + i * 22
        svg.extend(plant_sprite(level, 822, yy - 14))
        svg.append(text(860, yy + 2, label, 12, IV))
    svg.append(text(824, 240, "MISO = TODAY'S PATROL", 11, SAGE))

    tx, ty = today_tile
    walk_style = 'style="--x0:-14px;--y0:6px;--x1:14px;--y1:-6px;animation-duration:7s"'
    svg.append(f'<g class="walk" {walk_style} transform="translate({tx+16} {ty+23})">{miso_svg()}</g>')

    footer = 'SAMPLE ACTIVITY // run workflow for real contributions' if demo else f'{total:,} contributions shown // refreshed {now.isoformat()} UTC'
    svg += [r(30, 393, 990, 2, MOSS), text(35, 412, footer, 13, IV), '</svg>']
    OUT.write_text('\n'.join(svg), encoding='utf-8')
    print('Generated', OUT)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--demo', action='store_true')
    args = p.parse_args()
    if args.demo:
        draw({}, demo=True)
        return
    username = os.getenv('GH_USERNAME')
    token = os.getenv('GH_TOKEN')
    if not (username and token):
        raise SystemExit('GH_USERNAME and GH_TOKEN required; or use --demo')
    draw(get_days(username, token), demo=False)


if __name__ == '__main__':
    main()
