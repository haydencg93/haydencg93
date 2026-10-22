#!/usr/bin/env python3
"""Pixel garden from GitHub contributions. --demo creates marked sample data."""
import argparse,datetime as dt,json,os,random,urllib.request
from pathlib import Path
from xml.sax.saxutils import escape
OUT=Path(__file__).resolve().parents[1]/'assets'/'contribution-garden.svg'
Q='query($login:String!){user(login:$login){contributionsCollection{contributionCalendar{weeks{contributionDays{date contributionCount contributionLevel}}}}}}'
LEVEL={'NONE':0,'FIRST_QUARTILE':1,'SECOND_QUARTILE':2,'THIRD_QUARTILE':3,'FOURTH_QUARTILE':4}
DARK='#182521';IV='#F3F0E7';SAGE='#A7B69C';MOSS='#677D69';FOREST='#34483B';BROWN='#7A6552'
def r(x,y,w,h,c):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{c}"/>'
def get_days(user,token):
 data=json.dumps({'query':Q,'variables':{'login':user}}).encode()
 req=urllib.request.Request('https://api.github.com/graphql',data=data,headers={'Authorization':'Bearer '+token,'Content-Type':'application/json','User-Agent':'hayden-arcade-garden'})
 with urllib.request.urlopen(req,timeout=30) as res:result=json.load(res)
 if result.get('errors'):raise RuntimeError(str(result['errors']))
 weeks=result['data']['user']['contributionsCollection']['contributionCalendar']['weeks']
 return {d['date']:d for w in weeks for d in w['contributionDays']}
def draw(days,demo=False):
 now=dt.datetime.now(dt.timezone.utc).date();sunday=now-dt.timedelta(days=(now.weekday()+1)%7);start=sunday-dt.timedelta(weeks=25)
 a=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1050 420" role="img" aria-label="Pixel garden of 26 weeks of contributions">',r(0,0,1050,420,DARK),r(12,12,1026,396,FOREST),r(17,17,1016,386,DARK)]
 a += [f'<text x="34" y="55" font-size="26" font-family="monospace" font-weight="bold" fill="{IV}">[ CONTRIBUTION GARDEN ]</text>',f'<text x="34" y="81" font-size="14" font-family="monospace" fill="{SAGE}">26 WEEKS / SEED &gt; SPROUT &gt; LEAF &gt; BLOOM &gt; TREE</text>',r(30,91,990,3,MOSS)]
 if demo:a.append(f'<text x="1010" y="53" text-anchor="end" font-family="monospace" font-size="15" fill="{IV}">DEMO // NOT LIVE</text>')
 rng=random.Random(19);total=0
 for w in range(26):
  for daynum in range(7):
   day=start+dt.timedelta(days=w*7+daynum)
   if day>now:continue
   record=days.get(day.isoformat(),{})
   level=rng.choices(range(5),weights=[36,31,16,11,6])[0] if demo else LEVEL.get(record.get('contributionLevel','NONE'),0)
   if not demo:total+=record.get('contributionCount',0)
   x=34+w*38;y=120+daynum*34
   a.append(r(x,y,31,29,'#405044'))
   a.append(r(x+3,y+3,25,23,['#695A48','#506B4E','#567A55','#658B56','#7F9F69'][level]))
   if level==1:a += [r(x+14,y+11,3,11,IV),r(x+9,y+10,7,5,SAGE)]
   elif level==2:a += [r(x+14,y+10,3,12,IV),r(x+7,y+11,7,5,SAGE),r(x+17,y+7,8,5,SAGE)]
   elif level==3:a += [r(x+14,y+11,3,12,IV),r(x+8,y+8,5,6,SAGE),r(x+18,y+8,5,6,SAGE),r(x+14,y+4,5,6,IV)]
   elif level==4:a += [r(x+14,y+15,5,9,BROWN),r(x+7,y+9,19,9,FOREST),r(x+10,y+4,13,9,SAGE)]
 # frog sprite drawn in pixel blocks in side-corner; not representing a specific day
 sprite=['..GGGG..','.GGGGGG.','GGKGGKGG','GGGGGGGG','GGDGGDGG','.GGGGGG.','..GGGG..','.G....G.']
 pal={'G':SAGE,'K':DARK,'D':FOREST}
 for yy,line in enumerate(sprite):
  for xx,ch in enumerate(line):
   if ch in pal:a.append(r(906+xx*6,326+yy*6,6,6,pal[ch]))
 a += [r(30,383,990,2,MOSS),f'<text x="35" y="400" font-size="13" font-family="monospace" fill="{IV}">{escape("SAMPLE ACTIVITY // run workflow for real contributions" if demo else f"{total:,} contributions shown // refreshed {now.isoformat()} UTC")}</text>','</svg>']
 OUT.write_text('\n'.join(a),encoding='utf-8');print('Generated',OUT)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--demo',action='store_true');o=p.parse_args()
 if o.demo:draw({},True)
 else:
  u=os.getenv('GH_USERNAME');t=os.getenv('GH_TOKEN')
  if not (u and t):raise SystemExit('GH_USERNAME and GH_TOKEN required; or use --demo')
  draw(get_days(u,t))
