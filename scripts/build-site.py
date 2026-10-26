#!/usr/bin/env python3
"""Build index.html: src/main.html + src/tail.html, with every room in
experiences/ embedded so the site opens each one inside itself.

    python3 scripts/build-site.py
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
site = (ROOT / "src/main.html").read_text(encoding="utf-8") + (ROOT / "src/tail.html").read_text(encoding="utf-8")

for f in sorted((ROOT / "experiences").glob("experience-*.html")):
    key = f.stem.removeprefix("experience-")
    tag = f'<script type="text/html" id="exp-src-{key}">'
    if tag not in site:
        print(f"skip {f.name}: no slot for it in src/tail.html")
        continue
    body = f.read_text(encoding="utf-8")
    assert "<!--SCRIPT_END-->" not in body, f.name
    body = body.replace("</script>", "<!--SCRIPT_END-->")      # the site turns these back when it opens a room
    i = site.index(tag)
    j = site.index("</script>", i) + len("</script>")
    site = site[:i] + tag + "\n" + body + "\n</script>" + site[j:]

# a stamp for this build: an open page that finds a newer stamp on the server reloads itself,
# so a browser (or the Pages cache, which keeps pages up to ten minutes) never shows an old museum
import time
ver = time.strftime("%Y%m%d%H%M%S", time.gmtime())
check = ("<script>(function(){var V=\"" + ver + "\";if(!/^https?:$/.test(location.protocol)||/claude/i.test(location.hostname))return;"
         "fetch(\"experiences/version.txt?t=\"+Date.now(),{cache:\"no-store\"}).then(function(r){return r.ok?r.text():\"\"}).then(function(t){t=(t||\"\").trim();"
         "if(!t||t===V)return;var u=new URL(location.href);if(u.searchParams.get(\"v\")===t)return;u.searchParams.set(\"v\",t);location.replace(u.toString());})"
         ".catch(function(){});})();</script>")
k = site.index("<head>") + len("<head>")
site = site[:k] + "\n" + check + site[k:]
(ROOT / "experiences/version.txt").write_text(ver + "\n", encoding="utf-8")
(ROOT / "index.html").write_text(site, encoding="utf-8")
print(f"index.html: {len(site):,} bytes")
