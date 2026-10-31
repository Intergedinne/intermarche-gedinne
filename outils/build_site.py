"""Construit index.html (GitHub Pages) à partir de la source de l'artifact.
Remplace Google Fonts par les polices hébergées dans fonts/ (RGPD)."""
import re, sys

import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "outils", "source-artifact.html")
OUT = os.path.join(ROOT, "index.html")

FONTS = """<style>
@font-face{font-family:"Caveat";font-weight:600;font-display:swap;src:url(fonts/caveat-latin-600-normal.woff2) format("woff2")}
@font-face{font-family:"Caveat";font-weight:700;font-display:swap;src:url(fonts/caveat-latin-700-normal.woff2) format("woff2")}
@font-face{font-family:"Fraunces";font-weight:600;font-display:swap;src:url(fonts/fraunces-latin-600-normal.woff2) format("woff2")}
@font-face{font-family:"Fraunces";font-weight:800;font-display:swap;src:url(fonts/fraunces-latin-800-normal.woff2) format("woff2")}
@font-face{font-family:"Figtree";font-weight:400;font-display:swap;src:url(fonts/figtree-latin-400-normal.woff2) format("woff2")}
@font-face{font-family:"Figtree";font-weight:500;font-display:swap;src:url(fonts/figtree-latin-500-normal.woff2) format("woff2")}
@font-face{font-family:"Figtree";font-weight:700;font-display:swap;src:url(fonts/figtree-latin-700-normal.woff2) format("woff2")}
</style>"""

# Adresse publique du site : à changer ici quand le domaine intergedinne.be sera actif.
SITE = "https://intergedinne.be/"
TITLE = "Intermarché Gedinne – le marché du village, ouvert tous les jours"
DESC = ("Promo du jour, folder de la semaine et réservation en ligne à la boucherie. "
        "Ouvert de 8 h à 19 h, 7 jours sur 7, jours fériés compris. Rue de Charleville 48, Gedinne.")
OG = f"""<link rel="canonical" href="{SITE}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Intermarché Gedinne">
<meta property="og:title" content="{TITLE}">
<meta property="og:description" content="{DESC}">
<meta property="og:url" content="{SITE}">
<meta property="og:image" content="{SITE}img/partage.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="La façade de l'Intermarché Contact de Gedinne au coucher du soleil">
<meta property="og:locale" content="fr_BE">
<meta property="og:locale:alternate" content="nl_BE">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#232a35">
"""

s = open(SRC, encoding="utf-8").read()
s = s.replace('<meta name="claude:viewport-fit-sides" content="cover">\n', "")
s, n = re.subn(r'<link rel="preconnect"[^>]*>\n<link rel="stylesheet" href="https://fonts\.googleapis\.com[^>]*>', FONTS, s)
if n != 1:
    sys.exit("Google Fonts link not found")
i = s.index('<header class="top">')
head, body = s[:i].rstrip(), s[i:]
head = head[: -len("</style>")] if head.endswith("</style>") else sys.exit("unexpected head")
# head = title + fonts + main style
page = (
    '<!doctype html>\n<html lang="fr">\n<head>\n<meta charset="utf-8">\n'
    '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
    '<meta name="description" content="' + DESC + '">\n'
    + OG
    + head + "</style>\n"
    '<style>:root{padding-top:env(safe-area-inset-top);padding-bottom:env(safe-area-inset-bottom)} body{margin:0} img{max-width:100%} [hidden]{display:none!important}</style>\n'
    "</head>\n<body>\n" + body.lstrip("\n") + "\n</body>\n</html>\n"
)
assert "fonts.googleapis" not in page
# Garde le folder déjà en ligne (mis à jour chaque lundi directement dans index.html).
FD = re.compile(r'<script id="folderData" type="application/json">.*?</script>', re.S)
if os.path.exists(OUT):
    live = FD.search(open(OUT, encoding="utf-8").read())
    if live:
        page = FD.sub(lambda m: live.group(0), page, count=1)
open(OUT, "w", encoding="utf-8").write(page)
print("ok", len(page))
