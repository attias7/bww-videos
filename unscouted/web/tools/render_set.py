"""Render every board in a scenario set (answers revealed) to a contact sheet.
Usage: python3 render_set.py <scenario_js_file> <position_key> <out.png>
The JS file must assign an array to QS2.<position_key> (or define var QS with that key)."""
import sys, io, re, os
from playwright.sync_api import sync_playwright
from PIL import Image
HERE=os.path.dirname(os.path.abspath(__file__))
js_file, pos, out = sys.argv[1], sys.argv[2], sys.argv[3]
page_html=open(os.path.join(HERE,'..','pause-decide-test.html')).read()
extra=open(js_file).read()
inject="var QS2={};\n"+extra+"\nQS['"+pos+"']=QS2['"+pos+"']||QS['"+pos+"'];\n"
page_html=page_html.replace("var Q=[];", inject+"var Q=[];",1)
tmp=os.path.join(HERE,'_render.html')
open(tmp,'w').write('<!doctype html><html><head><meta charset="utf-8"><style>body{margin:0;font-family:system-ui,sans-serif}</style></head><body>'+page_html+'</body></html>')
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1300,'height':900}); errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    pg.goto('file://'+tmp)
    if errs: print('JS ERRORS:',errs); sys.exit(1)
    pg.click(f'#ust-pos button[data-p={pos}]'); pg.click('#ust-start'); pg.wait_for_timeout(200)
    n=pg.evaluate("document.getElementById('ust-n').textContent").split('/')[1].strip()
    tiles=[]
    for k in range(int(n)):
        q=pg.inner_text('#ust-q')
        pg.locator('#ust-opts .opt').nth(0).click(); pg.wait_for_timeout(60)
        img=Image.open(io.BytesIO(pg.locator('#ust-pitch svg').screenshot())); img.thumbnail((480,480))
        canvas=Image.new('RGB',(480,img.height+4),'white'); canvas.paste(img,(0,0)); tiles.append(canvas)
        print(f"{k+1}: {q}")
        pg.click('#ust-next'); pg.wait_for_timeout(60)
    if errs: print('JS ERRORS:',errs)
    W=480;H=max(t.height for t in tiles);cols=4;rows=(len(tiles)+cols-1)//cols
    o=Image.new('RGB',(W*cols,H*rows),'white')
    for i,t in enumerate(tiles): o.paste(t,((i%cols)*W,(i//cols)*H))
    o.save(out); print('saved',out,len(tiles),'boards')
    b.close()
