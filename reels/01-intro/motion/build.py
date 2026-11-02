"""Build reel.html from src.html: inline fonts, optional voiceover + line timings.
usage: python3 build.py [voiceover.mp3] [lines.json]"""
import base64, json, sys, pathlib
here = pathlib.Path(__file__).parent
s = (here / 'src.html').read_text()
s = s.replace('/*FONTS*/', (here / 'fonts.css').read_text())
for k, f in (('LOGO_FULL', 'logo-full.png'), ('LOGO_MARK', 'logo-mark.png')):
    s = s.replace('/*%s*/' % k, 'data:image/png;base64,' + base64.b64encode((here / 'assets' / f).read_bytes()).decode())
vo = sys.argv[1] if len(sys.argv) > 1 else None
s = s.replace('/*VO*/', base64.b64encode(pathlib.Path(vo).read_bytes()).decode() if vo else '')
if len(sys.argv) > 2:
    lines = json.loads(pathlib.Path(sys.argv[2]).read_text())
    s = s.replace('/*LINES*/[', '/*LINES*/' + json.dumps(lines) + ';//[', 1)
(here / 'reel.html').write_text(s)
print('reel.html', len(s) // 1024, 'KB')
