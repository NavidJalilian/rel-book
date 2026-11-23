"""Layout check in headless Chrome (landscape + portrait, every scene frozen at its end state).
Usage: python3 -I tools/check.py books/<book>/chNN.html [...]"""
import sys, subprocess, json, re, os, pathlib
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
bad = 0
for f in sys.argv[1:]:
    url = pathlib.Path(f).resolve().as_uri() + '?check'
    try:
        out = subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--window-size=1400,900',
                              '--virtual-time-budget=15000', '--allow-file-access-from-files', '--dump-dom', url],
                             capture_output=True, text=True, timeout=90).stdout
    except subprocess.TimeoutExpired:
        print('FAIL', f, 'chrome timed out'); bad += 1; continue
    m = re.search(r'<pre id="check-result"[^>]*>(.*?)</pre>', out, re.S)
    if not m:
        print('FAIL', f, 'no check result (script error? open the page in a browser and look at the console)'); bad += 1; continue
    import html
    r = json.loads(html.unescape(m.group(1)))
    st = 'OK  ' if not r['issues'] else 'ISSUES'
    if r['issues']: bad += 1
    print(f"{st} {f}: {r['scenes']} scenes, {r['seconds']/60:.1f} min, {len(r['issues'])} issues")
    for i in r['issues'][:40]: print('   -', i)
sys.exit(1 if bad else 0)
