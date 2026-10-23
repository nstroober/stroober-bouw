#!/usr/bin/env python3
"""Genereert de statische site van Stroober Bouw & Onderhoud.

Pagina's worden opgebouwd uit de templates hieronder, content/site.json (teksten)
en content/projects.json (projecten). Beide worden via /beheer/ bijgewerkt.
Op GitHub draait dit script automatisch bij elke push (zie .github/workflows).
Lokaal: `python3 build.py && python3 -m http.server 4321`.
"""
import datetime
import json
import re
from html import escape
from pathlib import Path

ROOT = Path(__file__).parent
SITE = "https://strooberbouw.nl"
YEAR = datetime.date.today().year
VERSION = datetime.datetime.now().strftime("%Y%m%d%H%M")

S = json.loads((ROOT / "content" / "site.json").read_text(encoding="utf-8"))
PROJECTS = json.loads((ROOT / "content" / "projects.json").read_text(encoding="utf-8"))

C = S["contact"]
PHONE = C["phone"]
PHONE_HREF = "tel:+31" + re.sub(r"\D", "", PHONE).lstrip("0")
EMAIL = C["email"]
ADDRESS = f'{C["street"]}, {C["postcode"]} {C["city"]}'
MAPS = "https://www.google.com/maps/search/?api=1&query=" + ADDRESS.replace(" ", "+").replace(",", "")
DESCRIPTION = "Stroober Bouw & Onderhoud uit Nunspeet. Van kleine verbouwing tot complete renovatie, uitbouw of veranda - wij maken uw woonwensen waar."

ICON = {
    "phone": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.8 2z"/></svg>',
    "mail": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/></svg>',
    "pin": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/></svg>',
    "eye": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 5C6.5 5 2.7 9.2 1.5 12c1.2 2.8 5 7 10.5 7s9.3-4.2 10.5-7C21.3 9.2 17.5 5 12 5zm0 11.5a4.5 4.5 0 1 1 0-9 4.5 4.5 0 0 1 0 9zm0-2.2a2.3 2.3 0 1 0 0-4.6 2.3 2.3 0 0 0 0 4.6z"/></svg>',
    "chat": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M4 3h16a2 2 0 0 1 2 2v11a2 2 0 0 1-2 2h-7l-5 4v-4H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2z"/></svg>',
    "menu": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M3 6h18M3 12h18M3 18h18"/></svg>',
}

NAV = [("/", "Home"), ("/over/", "Over"), ("/projecten/", "Projecten"), ("/contact/", "Contact")]


def paragraphs(text):
    """Tekst met lege regels ertussen -> <p>-blokken; enkele enters -> <br>."""
    return "".join(
        "<p>" + escape(block.strip()).replace("\n", "<br>") + "</p>"
        for block in re.split(r"\n\s*\n", text.strip()) if block.strip()
    )


def img(image, alt, folder="/assets/img/", eager=False, sizes="(max-width: 720px) 100vw, 50vw"):
    """<img> met 800px variant en de uitsnede (x/y/zoom) die in beheer is ingesteld."""
    path = folder + image["src"]
    small = path[:-4] + "-sm.jpg"
    x, y, zoom = image.get("x", 50), image.get("y", 50), image.get("zoom", 1)
    style = f"object-position:{x}% {y}%"
    if zoom and zoom != 1:
        style += f";transform:scale({zoom});transform-origin:{x}% {y}%"
    loading = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    return (f'<img src="{path}" srcset="{small} 800w, {path} 1600w" sizes="{sizes}" '
            f'alt="{escape(alt)}" style="{style}" {loading}>')


def page(path, title, body, description=DESCRIPTION, image="/assets/img/og-image.png", extra_head=""):
    current = "/" + path.strip("/").split("/")[0] + "/" if path != "/" else "/"
    aria = ' aria-current="page"'
    nav = "".join(f'<a href="{href}"{aria if href == current else ""}>{label}</a>' for href, label in NAV)
    footer_nav = "".join(f'<a href="{href}">{label}</a>' for href, label in NAV)
    full_title = title if title.startswith("Stroober") else f"{title} - Stroober Bouw & Onderhoud"
    url = SITE + path
    return f"""<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(full_title)}</title>
<meta name="description" content="{escape(description)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:locale" content="nl_NL">
<meta property="og:site_name" content="Stroober Bouw &amp; Onderhoud">
<meta property="og:title" content="{escape(full_title)}">
<meta property="og:description" content="{escape(description)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}{image}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#00024d">
<link rel="icon" type="image/png" href="/assets/img/favicon.png">
<link rel="preload" href="/assets/fonts/prototype.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/css/style.css?v={VERSION}">
{extra_head}</head>
<body>
<a class="skip" href="#main">Naar inhoud</a>
<header class="site-header">
  <div class="wrap">
    <a class="logo" href="/" aria-label="Stroober Bouw &amp; Onderhoud - home"><img src="/assets/img/logo.png" alt="Stroober Bouw &amp; Onderhoud" width="1240" height="513"></a>
    <button class="nav-toggle" aria-label="Menu" aria-expanded="false" aria-controls="nav">{ICON["menu"]}</button>
    <nav class="nav" id="nav" aria-label="Hoofdmenu">{nav}</nav>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="site-footer">
  <div class="wrap">
    <div class="footer-box">
      <div>
        <img src="/assets/img/logo-stacked.png" alt="" width="908" height="783" loading="lazy">
        <p>&copy; {YEAR} Stroober Bouw &amp; Onderhoud</p>
        <p><a href="{PHONE_HREF}">{escape(PHONE)}</a></p>
        <p><a href="mailto:{EMAIL}">{escape(EMAIL)}</a></p>
        <p>{escape(ADDRESS)}</p>
      </div>
      <nav class="footer-nav" aria-label="Footermenu">{footer_nav}</nav>
    </div>
  </div>
</footer>
<script src="/assets/js/main.js?v={VERSION}" defer></script>
</body>
</html>
"""


def cards(projects):
    return "\n".join(
        f'<a class="card" href="/projecten/{p["slug"]}/">{img(p["images"][0], p["title"], "/assets/img/projecten/")}'
        f'<span class="card-label">{escape(p["title"])}</span></a>'
        for p in projects if p["images"]
    )


def cta():
    return f"""<section class="section"><div class="wrap">
  <div class="cta">
    <div><h2>{escape(S["cta"]["title"])}</h2><p>{escape(S["cta"]["text"])}</p></div>
    <a class="btn" href="/contact/">Neem contact op</a>
  </div>
</div></section>"""


def home():
    H = S["home"]
    services = list(enumerate(H["services"]))
    tabs = "".join(
        f'<button class="tab" role="tab" id="tab-{i}" aria-controls="panel-{i}" aria-selected="{str(i == 0).lower()}">{escape(s["title"])}</button>'
        for i, s in services
    )
    panels = "".join(
        f'<div class="panel" role="tabpanel" id="panel-{i}" aria-labelledby="tab-{i}"{"" if i == 0 else " hidden"}>'
        f'{img(s["image"], s["title"], sizes="100vw")}<div class="panel-text"><p>{escape(s["text"])}</p></div></div>'
        for i, s in services
    )
    steps = "".join(
        f'<li class="step"><span class="step-num">{i}</span><h3>{escape(s["title"])}</h3><p>{escape(s["text"])}</p></li>'
        for i, s in enumerate(H["steps"], 1)
    )
    schema = {
        "@context": "https://schema.org",
        "@type": "HomeAndConstructionBusiness",
        "name": "Stroober Bouw & Onderhoud",
        "url": SITE,
        "logo": SITE + "/assets/img/logo.png",
        "image": SITE + "/assets/img/" + H["heroImage"]["src"],
        "telephone": PHONE_HREF[4:],
        "email": EMAIL,
        "foundingDate": "2019",
        "address": {"@type": "PostalAddress", "streetAddress": C["street"], "postalCode": C["postcode"],
                    "addressLocality": C["city"], "addressCountry": "NL"},
        "areaServed": sorted({C["city"]} | {p["location"] for p in PROJECTS if p["location"] != "Nederland"}),
    }
    body = f"""<section><div class="wrap">
  <div class="hero">
    {img(H["heroImage"], H["heroTitle"], eager=True, sizes="100vw")}
    <div class="hero-card">
      <h1>{escape(H["heroTitle"])}</h1>
      <p>{escape(H["heroText"])}</p>
      <div class="btns"><a class="btn btn-primary" href="/projecten/">Bekijk projecten</a><a class="btn btn-ghost" href="/over/">Lees meer</a></div>
    </div>
  </div>
</div></section>

<section class="section"><div class="wrap intro">
  <div>{paragraphs(H["intro"])}</div>
  <div class="tiles">
    <div class="tile tile-blue">{ICON["eye"]}<span>oog voor detail</span></div>
    <div class="tile tile-turq">{ICON["chat"]}<span>heldere communicatie</span></div>
    <div class="tile tile-navy"><strong>{escape(H["projectsCount"])}</strong><span>afgeronde projecten</span></div>
  </div>
</div></section>

<section class="section" style="padding-top:0"><div class="wrap">
  <h2>Onze diensten</h2>
  <div class="tabs" role="tablist" aria-label="Onze diensten">{tabs}</div>
  {panels}
</div></section>

<section class="section"><div class="wrap steps-grid">
  <div class="sticky">
    <h2>Hoe gaan wij te werk?</h2>
    {paragraphs(H["stepsText"])}
    <a class="btn btn-ghost" href="/over/">Over ons</a>
  </div>
  <ol class="steps">{steps}</ol>
</div></section>

<section class="section" style="padding-top:0"><div class="wrap">
  <div class="section-head"><h2>Recente projecten</h2><a class="btn btn-ghost" href="/projecten/">Alle projecten</a></div>
  <div class="grid">{cards(PROJECTS[:4])}</div>
</div></section>
{cta()}"""
    ld = f'<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>\n'
    return page("/", "Stroober Bouw & Onderhoud", body, extra_head=ld)


def over():
    O = S["over"]
    body = f"""<section class="section"><div class="wrap split">
  <div>
    <h1>{escape(O["title"])}</h1>
    {paragraphs(O["text"])}
  </div>
  <div class="frame">{img(O["image"], "Lennart Stroober", eager=True)}</div>
</div></section>
{cta()}"""
    return page("/over/", "Over", body, description="Stroober Bouw & Onderhoud is in 2019 gestart vanuit een passie voor het bouwersvak. Persoonlijke aanpak, vast aanspreekpunt en kwaliteit boven kwantiteit.")


def projecten():
    body = f"""<section class="section" style="padding-top:40px"><div class="wrap">
  <h1>Projecten</h1>
  <div class="grid">{cards(PROJECTS)}</div>
</div></section>
{cta()}"""
    return page("/projecten/", "Projecten", body, description="Bekijk projecten van Stroober Bouw & Onderhoud: renovaties, uitbouwen, veranda's en tuinhuizen in Nunspeet, Bennekom, Ede en omgeving.")


def contact():
    P = S["contactPage"]
    body = f"""<section class="section"><div class="wrap split contact-split">
  <div>
    <h1>Contact</h1>
    {paragraphs(P["text"])}
    <ul class="contact-list">
      <li>{ICON["phone"]}<a href="{PHONE_HREF}">{escape(PHONE)}</a></li>
      <li>{ICON["mail"]}<a href="mailto:{EMAIL}">{escape(EMAIL)}</a></li>
      <li>{ICON["pin"]}<a href="{MAPS}" target="_blank" rel="noopener">{escape(ADDRESS)}</a></li>
    </ul>
    <form class="contact-form" action="{escape(P["formEndpoint"])}" method="POST">
      <div class="form-row">
        <label>Naam<input type="text" name="naam" autocomplete="name" required></label>
        <label>E-mail<input type="email" name="email" autocomplete="email" required></label>
      </div>
      <label><span>Telefoon <small>(optioneel)</small></span><input type="tel" name="telefoon" autocomplete="tel"></label>
      <label>Bericht<textarea name="bericht" rows="5" required></textarea></label>
      <input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
      <input type="hidden" name="_subject" value="Nieuw bericht via strooberbouw.nl">
      <input type="hidden" name="_template" value="table">
      <button class="btn btn-primary" type="submit">Verstuur bericht</button>
      <p class="form-note">Uw gegevens gebruiken we alleen om contact met u op te nemen.</p>
      <p class="form-status" role="status" hidden></p>
    </form>
  </div>
  <div class="frame">{img(P["image"], "Stroober bedrijfsbus op de bouwplaats", eager=True)}</div>
</div></section>"""
    return page("/contact/", "Contact", body, description=f"Neem contact op met Stroober Bouw & Onderhoud in {C['city']}. Bel {PHONE} of mail {EMAIL}.")


def project(i, p):
    prev_p, next_p = PROJECTS[i - 1], PROJECTS[(i + 1) % len(PROJECTS)]
    base = "/assets/img/projecten/"
    title = p["title"]
    gallery = "".join(
        f'<button type="button" data-full="{base}{im["src"]}" aria-label="Foto {n} vergroten">'
        f'{img(im, f"{title} - foto {n}", base, sizes="(max-width: 720px) 100vw, 33vw")}</button>'
        for n, im in enumerate(p["images"], 1)
    )
    meta = "".join(
        f'<div><dt>{label}</dt><dd>{escape(p[key])}</dd></div>'
        for key, label in (("location", "Locatie"), ("type", "Project type")) if p.get(key)
    )
    nav = ""
    if len(PROJECTS) > 1:
        nav = f"""<nav class="pager" aria-label="Andere projecten">
    <a href="/projecten/{prev_p["slug"]}/">&larr; {escape(prev_p["title"])}</a>
    <a href="/projecten/{next_p["slug"]}/">{escape(next_p["title"])} &rarr;</a>
  </nav>"""
    body = f"""<section style="padding-top:8px"><div class="wrap">
  <div class="project-hero">{img(p["images"][0], title, base, eager=True, sizes="100vw")}<h1>{escape(title)}</h1></div>
  <div class="project-body">
    <dl class="meta">{meta}</dl>
    <div class="project-text">{paragraphs(p["text"])}</div>
  </div>
  <div class="gallery">{gallery}</div>
  {nav}
</div></section>
<div class="lightbox" hidden role="dialog" aria-modal="true" aria-label="Foto">
  <button class="lb-close" aria-label="Sluiten">&times;</button>
  <button class="lb-prev" aria-label="Vorige foto">&lsaquo;</button>
  <img src="" alt="">
  <button class="lb-next" aria-label="Volgende foto">&rsaquo;</button>
</div>
{cta()}"""
    text = " ".join(p["text"].split())
    desc = text if len(text) <= 155 else text[:155].rsplit(" ", 1)[0] + "..."
    return page(f"/projecten/{p['slug']}/", title, body, description=desc, image=base + p["images"][0]["src"])


def not_found():
    body = """<section class="section"><div class="wrap" style="min-height:40vh">
  <h1>Pagina niet gevonden</h1>
  <p>Deze pagina bestaat niet (meer). Bekijk onze projecten of ga terug naar de homepage.</p>
  <div class="btns"><a class="btn btn-primary" href="/">Naar home</a><a class="btn btn-ghost" href="/projecten/">Projecten</a></div>
</div></section>"""
    return page("/404", "Pagina niet gevonden", body).replace(
        '<link rel="canonical" href="https://strooberbouw.nl/404">\n', '<meta name="robots" content="noindex">\n')


def write(rel, html):
    out = ROOT / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")


if __name__ == "__main__":
    PROJECTS = [p for p in PROJECTS if p.get("images")]
    write("index.html", home())
    write("over/index.html", over())
    write("projecten/index.html", projecten())
    write("contact/index.html", contact())
    for i, p in enumerate(PROJECTS):
        write(f"projecten/{p['slug']}/index.html", project(i, p))
    write("404.html", not_found())

    urls = ["/", "/over/", "/projecten/", "/contact/"] + [f"/projecten/{p['slug']}/" for p in PROJECTS]
    today = datetime.date.today().isoformat()
    sitemap = "".join(f"<url><loc>{SITE}{u}</loc><lastmod>{today}</lastmod></url>\n" for u in urls)
    write("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{sitemap}</urlset>\n')
    write("robots.txt", f"User-agent: *\nAllow: /\nDisallow: /beheer/\n\nSitemap: {SITE}/sitemap.xml\n")
    print(f"Gebouwd: {len(urls)} pagina's + 404")
