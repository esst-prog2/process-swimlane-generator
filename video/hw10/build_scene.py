"""Rebuild editable HyperFrames scene from the shipped workbook and SVG geometry."""
from pathlib import Path
import json, html
from xml.etree import ElementTree as ET
from openpyxl import load_workbook
ROOT=Path(__file__).resolve().parent
svg=ET.parse(ROOT/'assets/purchase-request.svg').getroot()
ns={'s':'http://www.w3.org/2000/svg'}
tasks={g.get('data-id'):g for g in svg if g.get('data-kind')=='task'}
links={g.get('data-target'):g for g in svg if g.get('data-kind')=='connection'}
rows={r[0]:r for r in list(load_workbook(ROOT/'assets/purchase_request.xlsx',data_only=True)['Process'].values)[1:]}
beats=[(0,3,'003','Who handles it next?','Requesting \u2192 Purchasing'),(3,6,'004','Check the budget','Finance'),(6,8.5,'005','Ask for quotations','Purchasing'),(8.5,11,'006','Choose a quotation','Purchasing'),(11,14,'007','Approve the spend','Finance'),(14,17,'008','Issue the order','Purchasing'),(17,20,'009','Receive the supplies','Receiving'),(20,23,'010','Check the quantities','Receiving'),(23,26,'011','Confirm the supplies','Requesting'),(26,30,'012','Complete the request','Purchasing')]
boxes={k:{a:float(v) for a,v in g.find('s:rect',ns).attrib.items() if a in ['x','y','width','height']} for k,g in tasks.items()}
# Adaptation of official pan-stations: paused timeline, explicit initial state,
# station centres, camera pan followed by a stationary reading dwell.
labels=[]; overlays=[]; moves=[]
for i,(start,end,tid,title,dept) in enumerate(beats):
    assert tasks[tid].get('data-department')==rows[tid][3]
    b=boxes[tid]; cx=b['x']+b['width']/2; cy=b['y']+b['height']/2
    labels.append(f'<div id="caption-{tid}" class="clip caption" data-beat="task-{tid}" data-start="{start}" data-duration="{end-start}" data-track-index="2" data-hold><h1>{html.escape(title)}</h1><p class="department">{html.escape(dept)}</p></div>')
    overlays.append(f'<rect id="focus-{tid}" x="{b["x"]}" y="{b["y"]}" width="{b["width"]}" height="{b["height"]}" rx="8" fill="none" stroke="#116149" stroke-width="4" opacity="0"/>')
    overlays.append(f'<path id="route-{tid}" d="{links[tid].get("d")}" fill="none" stroke="#116149" stroke-width="5" opacity="0"/>')
    at=0.5 if i==0 else start
    if i>0:
        pb=boxes[beats[i-1][2]]; px=pb['x']+pb['width']/2; py=pb['y']+pb['height']/2
        at=start-(0.85 if abs(cy-py)>160 else 0.55)
    if i>0 and abs(cy-py)>160:
        scale=300/(abs(cy-py)+112)
        moves.append(f'tl.to("#camera", {{x:{576-scale*(cx+px)/2}, y:{180-scale*(cy+py)/2}, scale:{scale}, duration:0.35, ease:"power2.inOut"}}, {at});')
        moves.append(f'tl.to("#camera", {{x:{576-2*cx}, y:{180-2*cy}, scale:2, duration:0.5, ease:"power2.inOut"}}, {at+0.35});')
    else:
        moves.append(f'tl.to("#camera", {{x:{576-2*cx}, y:{180-2*cy}, scale:2, duration:{0.7 if i==0 else 0.55}, ease:"power2.inOut"}}, {at});')
    moves.append(f'tl.set("#route-{tid}", {{opacity:1}}, {0 if i==0 else at}); tl.set("#focus-{tid}", {{opacity:1}}, {0.9 if i==0 else start});')
    if i>0:
        prev=beats[i-1][2]
        moves.append(f'tl.set("#focus-{prev}, #route-{prev}", {{opacity:0}}, {start});')
# The first framing contains complete boxes 002 and 003 and their true connecting path.
initial={'x':576-1.28*996,'y':180-1.28*304,'scale':1.28}
scene='''<template>
<style>
#root {position:absolute;inset:0;background:#f5f3eb;color:#183e33;font-family:Inter,sans-serif;overflow:hidden}
.caption{position:absolute;inset:0;pointer-events:none}
h1{position:absolute;left:128px;top:53px;margin:0;font-size:48px;font-weight:700;line-height:1.2}
.department{position:absolute;left:128px;top:125px;margin:0;font-size:30px;font-weight:700}
#window{position:absolute;left:64px;top:205px;width:1152px;height:360px;overflow:hidden;background:white;border-top:2px solid #bcc7bc;border-bottom:2px solid #bcc7bc}
#camera{position:absolute;left:0;top:0;width:5272px;height:816px;transform-origin:0 0}
#camera img,#camera svg{position:absolute;inset:0;width:5272px;height:816px}
#provenance{position:absolute;left:128px;top:605px;margin:0;font-size:22px}
#source{position:absolute;left:128px;top:648px;margin:0;font-size:22px}
</style>
<div id="root" data-composition-id="journey" data-duration="30" data-width="1280" data-height="720">
<div id="window" data-layout-allow-overflow><div id="camera" data-layout-allow-overflow><img src="assets/purchase-request.svg" alt="Actual generated purchase-request SVG"/><svg viewBox="0 0 5272 816" aria-hidden="true">OVERLAYS</svg></div></div>
LABELS
<p id="provenance">Animated highlights on the generated diagram</p>
<p id="source">Source: purchase_request.xlsx \xb7 Fictional example</p>
</div>
<script>
const tl=gsap.timeline({paused:true});
gsap.set("#camera",INITIAL);
MOVES
window.__timelines=window.__timelines||{};
window.__timelines.journey=tl;
</script>
</template>'''
scene=scene.replace('OVERLAYS',''.join(overlays)).replace('LABELS','\n'.join(labels)).replace('INITIAL',json.dumps(initial)).replace('MOVES','\n'.join(moves))
# Ending remains on the final real task, adds the product and input/output context.
scene=scene.replace('<p id="source">Source: purchase_request.xlsx \xb7 Fictional example</p>','<p id="source" class="clip" data-start="0" data-duration="26" data-track-index="3">Source: purchase_request.xlsx \xb7 Fictional example</p><div id="ending" class="clip" data-start="26" data-duration="4" data-track-index="3"><p style="position:absolute;left:128px;top:640px;margin:0;background:#f5f3eb;font-size:28px">Process Swimlane Generator \xb7 Excel \u2192 SVG + offline HTML</p></div>')
(ROOT/'compositions/journey.html').write_text(scene,encoding='utf-8')
(ROOT/'index.html').write_text('''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Follow the request</title><script src="assets/gsap.min.js"></script><style>html,body{margin:0;width:1280px;height:720px;overflow:hidden;background:#f5f3eb}</style></head><body><div id="root" data-composition-id="main" data-start="0" data-duration="30" data-width="1280" data-height="720" data-fps="30"><div id="journey" class="clip" data-composition-id="journey" data-composition-src="compositions/journey.html" data-start="0" data-duration="30" data-track-index="0" data-track-kind="graphics" data-width="1280" data-height="720"></div></div><script>window.__timelines=window.__timelines||{};window.__timelines.main=gsap.timeline({paused:true});</script></body></html>''',encoding='utf-8')
(ROOT/'beats.json').write_text(json.dumps([{'start':a,'end':b,'task_id':t,'caption':c,'department':rows[t][3],'description':rows[t][2]} for a,b,t,c,d in beats],indent=2),encoding='utf-8')
print('Built journey with 10 exact task anchors, workbook-checked departments and actual SVG connections.')
