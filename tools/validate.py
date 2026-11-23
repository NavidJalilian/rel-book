"""Static checks for chapter pages. Usage: python3 -I tools/validate.py books/<book>/chNN.html [...]"""
import sys, re, json
from html.parser import HTMLParser

VOID = {'meta','link','br','img','input','hr','circle','rect','line','path','ellipse','polyline','polygon','use','stop','source','wbr'}
class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.stack=[]; s.err=[]; s.scenes=[]; s.anim_in_transform=[]; s.dr_no_pl=[]
    def handle_starttag(s, t, a):
        a = dict(a)
        cls = (a.get('class') or '').split()
        if t == 'section' and 'scene' in cls:
            s.scenes.append({k: a.get(k) for k in ('data-t','data-sec','data-title')} | {'line': s.getpos()[0]})
        if ('a' in cls or 'x' in cls) and 'transform' in a:
            s.anim_in_transform.append(s.getpos()[0])
        if 'dr' in cls and a.get('pathlength') != '1':
            s.dr_no_pl.append(s.getpos()[0])
        if t not in VOID: s.stack.append((t, s.getpos()[0]))
    def handle_startendtag(s, t, a):
        a = dict(a); cls = (a.get('class') or '').split()
        if ('a' in cls or 'x' in cls) and 'transform' in a: s.anim_in_transform.append(s.getpos()[0])
        if 'dr' in cls and a.get('pathlength') != '1': s.dr_no_pl.append(s.getpos()[0])
    def handle_endtag(s, t):
        if t in VOID: return
        if s.stack and s.stack[-1][0] == t: s.stack.pop(); return
        for i in range(len(s.stack)-1, -1, -1):
            if s.stack[i][0] == t:
                s.err.append(f'line {s.getpos()[0]}: </{t}> closes <{s.stack[-1][0]}> opened on line {s.stack[-1][1]} (unclosed tags)')
                del s.stack[i:]; return
        s.err.append(f'line {s.getpos()[0]}: stray </{t}>')

bad = 0
for path in sys.argv[1:]:
    src = open(path, encoding='utf-8').read()
    probs, warns = [], []
    m = re.search(r'<script type="application/json" id="meta">(.*?)</script>', src, re.S)
    meta = None
    try: meta = json.loads(m.group(1))
    except Exception as e: probs.append(f'meta JSON missing or invalid: {e}')
    p = P(); p.feed(src); p.close()
    probs += p.err
    for t, line in p.stack:
        if t not in ('html','body','head'): probs.append(f'<{t}> on line {line} never closed')
    if not p.scenes: probs.append('no <section class="scene"> found')
    nsec = len(meta['sections']) if meta else 0
    total = 0
    for i, sc in enumerate(p.scenes, 1):
        if not sc['data-title']: probs.append(f'scene {i} (line {sc["line"]}) has no data-title')
        try: total += float(sc['data-t'])
        except Exception: probs.append(f'scene {i} (line {sc["line"]}) has no numeric data-t')
        try:
            if not 0 <= int(sc['data-sec']) < nsec: probs.append(f'scene {i}: data-sec {sc["data-sec"]} outside meta.sections (0..{nsec-1})')
        except Exception: probs.append(f'scene {i} (line {sc["line"]}) has no data-sec')
    # each declared section is used
    used = {sc['data-sec'] for sc in p.scenes}
    for k in range(nsec):
        if str(k) not in used: warns.append(f'section {k} «{meta["sections"][k][0]}» has no scene')
    for line in p.anim_in_transform: probs.append(f'line {line}: animated element (.a/.x) also has a transform attribute; wrap it in a <g>')
    for line in p.dr_no_pl: probs.append(f'line {line}: .dr path needs pathLength="1"')
    # delays vs duration
    for sm in re.finditer(r'<section class="scene[^"]*"[^>]*data-t="([\d.]+)"(.*?)</section>', src, re.S):
        t = float(sm.group(1)); ds = [float(x) for x in re.findall(r'--d:([\d.]+)', sm.group(2))]
        if ds and max(ds) > t - 4: probs.append(f'scene at offset {sm.start()}: last element enters at {max(ds)}s but scene lasts {t}s (needs ≥4s after)')
    # Persian text hygiene (visible text only, roughly)
    body = re.sub(r'<script.*?</script>|<style.*?</style>|<[^>]+>', ' ', src, flags=re.S)
    body = re.sub(r'<span class="en">.*?</span>', ' ', body)
    vis = re.sub(r'<[^>]+>', ' ', re.sub(r'class="[^"]*en[^"]*"[^>]*>[^<]*', '', src))
    for w in ['می ', 'نمی ']:
        for mm in re.finditer(r'(?<![؀-ۿ])' + w + r'[؀-ۿ]', body):
            warns.append(f'missing ZWNJ: «{body[mm.start():mm.start()+14].strip()}»'); break
    for mm in re.finditer(r'[؀-ۿ]\s?[0-9]+|[0-9]+\s?[؀-ۿ]', body):
        warns.append(f'Latin digits next to Persian text: «{body[max(0,mm.start()-8):mm.end()+8].strip()}»'); break
    if re.search(r'[يك]', body): warns.append('Arabic ي/ك found; use Persian ی/ک')
    status = 'OK' if not probs else 'FAIL'
    if probs: bad += 1
    print(f'{status} {path}: {len(p.scenes)} scenes, {total/60:.1f} min')
    for x in probs: print('  ERROR', x)
    for x in warns[:12]: print('  warn ', x)
sys.exit(1 if bad else 0)
