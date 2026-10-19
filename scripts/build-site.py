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

(ROOT / "index.html").write_text(site, encoding="utf-8")
print(f"index.html: {len(site):,} bytes")
