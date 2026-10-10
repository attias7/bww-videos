"""Render individual boards to PNG (one file per situation).
Usage: python3 render_boards.py <js_file> <out_prefix> [--reveal]
<js_file> must assign an array to QS2.mid (same format as more_*.js).
Writes <out_prefix>-1.png, -2.png ... (question view; with --reveal also <out_prefix>-N-answer.png showing the pro arrow)."""
import sys, io, os, tempfile
from playwright.sync_api import sync_playwright
from PIL import Image
HERE=os.path.dirname(os.path.abspath(__file__))
js_file, prefix = sys.argv[1], sys.argv[2]; reveal='--reveal' in sys.argv
page=open(os.path.join(HERE,'..','pause-decide-test.html')).read()
inj="var QS2={};\n"+open(js_file).read()+"\nQS.mid=QS2.mid;\n"
page=page.replace("var Q=[];",inj+"var Q=[];",1).replace("var TIME=15","var TIME=9999").replace("s._ord=o;","o=[0,1,2];s._ord=o;window.__S=s;",1)
fd,tmp=tempfile.mkstemp(suffix='.html',dir=HERE); os.close(fd)
open(tmp,'w').write('<!doctype html><html><head><meta charset="utf-8"><style>body{margin:0;font-family:system-ui,sans-serif}</style></head><body>'+page+'</body></html>')
try:
  with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1300,'height':900},device_scale_factor=2); errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    pg.goto('file://'+tmp)
    pg.click('#ust-pos button[data-p=mid]'); pg.click('#ust-start'); pg.wait_for_timeout(250)
    n=int(pg.evaluate("document.getElementById('ust-n').textContent").split('/')[1])
    for k in range(n):
        pg.wait_for_timeout(150)
        pg.locator('#ust-pitch svg').screenshot(path=f'{prefix}-{k+1}.png')
        pro=pg.evaluate("__S._ord.indexOf(__S.pro)")
        pg.locator('#ust-opts .opt').nth(pro).click(); pg.wait_for_timeout(250)
        if reveal: pg.locator('#ust-pitch svg').screenshot(path=f'{prefix}-{k+1}-answer.png')
        print(k+1, pg.inner_text('#ust-q')[:90])
        pg.click('#ust-next')
    if errs: print('JS ERRORS:',errs); sys.exit(1)
    b.close()
finally: os.remove(tmp)
