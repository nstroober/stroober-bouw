#!/usr/bin/env python3
"""Genereert de statische site van Stroober Bouw & Onderhoud.

Pagina's worden opgebouwd uit de templates hieronder en content/projects.json.
Draai `python3 build.py` na elke wijziging en commit de gegenereerde HTML.
"""
import datetime
import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).parent
SITE = "https://strooberbouw.nl"
YEAR = datetime.date.today().year

PHONE = "06 13 13 29 79"
PHONE_HREF = "tel:+31613132979"
EMAIL = "lennart@strooberbouw.nl"
ADDRESS = "Gerbrandystraat 35, 8072 WN Nunspeet"
MAPS = "https://www.google.com/maps/search/?api=1&query=Gerbrandystraat+35+8072+WN+Nunspeet"
DESCRIPTION = "Stroober Bouw & Onderhoud uit Nunspeet. Van kleine verbouwing tot complete renovatie, uitbouw of veranda - wij maken uw woonwensen waar."

PROJECTS = json.loads((ROOT / "content" / "projects.json").read_text(encoding="utf-8"))

ICON = {
    "phone": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.8 2z"/></svg>',
    "mail": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/></svg>',
    "pin": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/></svg>',
    "eye": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 5C6.5 5 2.7 9.2 1.5 12c1.2 2.8 5 7 10.5 7s9.3-4.2 10.5-7C21.3 9.2 17.5 5 12 5zm0 11.5a4.5 4.5 0 1 1 0-9 4.5 4.5 0 0 1 0 9zm0-2.2a2.3 2.3 0 1 0 0-4.6 2.3 2.3 0 0 0 0 4.6z"/></svg>',
    "chat": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M4 3h16a2 2 0 0 1 2 2v11a2 2 0 0 1-2 2h-7l-5 4v-4H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2z"/></svg>',
    "menu": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M3 6h18M3 12h18M3 18h18"/></svg>',
}

NAV = [("/", "Home"), ("/over/", "Over"), ("/projecten/", "Projecten"), ("/contact/", "Contact")]


def img(path, alt, cls="", eager=False, sizes="(max-width: 720px) 100vw, 50vw"):
    """<img> met 800px variant voor kleine schermen."""
    small = path[:-4] + "-sm.jpg"
    loading = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    c = f' class="{cls}"' if cls else ""
    return (f'<img src="{path}" srcset="{small} 800w, {path} 1600w" sizes="{sizes}" '
            f'alt="{escape(alt)}"{c} {loading}>')


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
        <p><a href="{PHONE_HREF}">{PHONE}</a></p>
        <p><a href="mailto:{EMAIL}">{EMAIL}</a></p>
        <p>{ADDRESS}</p>
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
        f'<a class="card" href="/projecten/{p["slug"]}/">{img("/assets/img/projecten/" + p["images"][0], p["title"])}'
        f'<span class="card-label">{escape(p["title"])}</span></a>'
        for p in projects
    )


CTA = f"""<section class="section"><div class="wrap">
  <div class="cta">
    <div><h2>Plannen voor uw woning?</h2><p>Neem vrijblijvend contact op, dan bespreken we samen de mogelijkheden.</p></div>
    <a class="btn" href="/contact/">Neem contact op</a>
  </div>
</div></section>"""


SERVICES = [
    ("renovatie", "Renovatie", "Van badkamer tot complete woning - wij geven uw woning een nieuwe uitstraling. Met oog voor detail en binnen de afgesproken tijd maken wij uw renovatiewensen waar."),
    ("uitbouw", "Uitbouw", "Meer leefruimte nodig? Van ontwerp tot realisatie verzorgen wij uw uitbouw. We adviseren over de mogelijkheden en zorgen voor een vakkundige uitvoering."),
    ("veranda", "Veranda", "Een veranda vergroot uw woongenot. Modern of klassiek, wij realiseren uw droomveranda met aandacht voor materiaal en afwerking."),
]

STEPS = [
    ("Kennismaking", "Vrijblijvend gesprek om uw wensen te bespreken"),
    ("Offerte", "Heldere prijsopgave inclusief materialen en planning"),
    ("Voorbereiding", "Concrete werkplanning en afstemming startdatum"),
    ("Uitvoering", "Vakkundige realisatie met korte communicatielijnen"),
]


def home():
    tabs = "".join(
        f'<button class="tab" role="tab" id="tab-{k}" aria-controls="panel-{k}" aria-selected="{str(i == 0).lower()}">{label}</button>'
        for i, (k, label, _) in enumerate(SERVICES)
    )
    panels = "".join(
        f'<div class="panel" role="tabpanel" id="panel-{k}" aria-labelledby="tab-{k}"{"" if i == 0 else " hidden"}>'
        f'{img(f"/assets/img/dienst-{k}.jpg", label, sizes="100vw")}<div class="panel-text"><p>{text}</p></div></div>'
        for i, (k, label, text) in enumerate(SERVICES)
    )
    steps = "".join(
        f'<li class="step"><span class="step-num">{i}</span><h3>{t}</h3><p>{d}</p></li>'
        for i, (t, d) in enumerate(STEPS, 1)
    )
    schema = {
        "@context": "https://schema.org",
        "@type": "HomeAndConstructionBusiness",
        "name": "Stroober Bouw & Onderhoud",
        "url": SITE,
        "logo": SITE + "/assets/img/logo.png",
        "image": SITE + "/assets/img/hero.jpg",
        "telephone": "+31613132979",
        "email": EMAIL,
        "foundingDate": "2019",
        "address": {"@type": "PostalAddress", "streetAddress": "Gerbrandystraat 35", "postalCode": "8072 WN",
                    "addressLocality": "Nunspeet", "addressCountry": "NL"},
        "areaServed": ["Nunspeet", "Bennekom", "Ede", "Woudenberg", "Gelderland"],
    }
    body = f"""<section><div class="wrap">
  <div class="hero">
    {img("/assets/img/hero.jpg", "Uitbouw met glazen schuifwanden", eager=True, sizes="100vw")}
    <div class="hero-card">
      <h1>Uw project, onze expertise</h1>
      <p>Van kleine verbouwing tot complete renovatie - wij maken uw woonwensen waar.</p>
      <div class="btns"><a class="btn btn-primary" href="/projecten/">Bekijk projecten</a><a class="btn btn-ghost" href="/over/">Lees meer</a></div>
    </div>
  </div>
</div></section>

<section class="section"><div class="wrap intro">
  <p>Vakmanschap en persoonlijke aandacht staan bij ons voorop. Door intensieve samenwerking met vaste, vakkundige specialisten realiseren wij elk type verbouwing - van kleine aanpassing tot complete renovatie. Onze kracht ligt in een transparante aanpak en heldere communicatie tijdens het hele bouwproces. Met oog voor detail vertalen we uw woonwensen naar de praktijk. Bij elk project staat kwaliteit centraal, waarbij we u van begin tot eind begeleiden met deskundig advies en vakkundige uitvoering.</p>
  <div class="tiles">
    <div class="tile tile-blue">{ICON["eye"]}<span>oog voor detail</span></div>
    <div class="tile tile-turq">{ICON["chat"]}<span>heldere communicatie</span></div>
    <div class="tile tile-navy"><strong>50+</strong><span>afgeronde projecten</span></div>
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
    <p>Een succesvol bouwproject begint met een heldere aanpak. Na een vrijblijvend gesprek waarin we uw wensen bespreken, maken we een gedetailleerde offerte. Bij akkoord starten we met een duidelijke planning en houden we u tijdens het hele traject op de hoogte van de voortgang.</p>
    <a class="btn btn-ghost" href="/over/">Over ons</a>
  </div>
  <ol class="steps">{steps}</ol>
</div></section>

<section class="section" style="padding-top:0"><div class="wrap">
  <div class="section-head"><h2>Recente projecten</h2><a class="btn btn-ghost" href="/projecten/">Alle projecten</a></div>
  <div class="grid">{cards(PROJECTS[:4])}</div>
</div></section>
{CTA}"""
    ld = f'<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>\n'
    return page("/", "Stroober Bouw & Onderhoud", body, image="/assets/img/og-image.png", extra_head=ld)


def over():
    body = f"""<section class="section"><div class="wrap split">
  <div>
    <h1>Stroober Bouw &amp; Onderhoud</h1>
    <p>Wij zijn in 2019 gestart vanuit een passie voor het bouwersvak en oog voor detail. Door de jaren heen hebben wij een betrouwbaar netwerk opgebouwd van vakkundige specialisten, waarmee we regelmatig samenwerken om projecten te realiseren. Van elektricien tot stukadoor - elk aspect wordt door de juiste vakman uitgevoerd.</p>
    <p>Wat ons onderscheidt is de persoonlijke aanpak. Als vast aanspreekpunt zijn wij direct betrokken bij elk project en werken we mee op de bouw. Hierdoor houden we grip op de kwaliteit en planning, en kunnen we flexibel inspelen op eventuele aanpassingen tijdens het project.</p>
    <p>Door kleinschalig te blijven en bewust te kiezen voor projecten die bij ons passen, kunnen we elke klant de aandacht geven die het verdient. Kwaliteit gaat bij ons boven kwantiteit.</p>
  </div>
  {img("/assets/img/lennart.jpg", "Lennart Stroober bij de bedrijfsbus", eager=True)}
</div></section>
{CTA}"""
    return page("/over/", "Over", body, description="Stroober Bouw & Onderhoud is in 2019 gestart vanuit een passie voor het bouwersvak. Persoonlijke aanpak, vast aanspreekpunt en kwaliteit boven kwantiteit.")


def projecten():
    body = f"""<section class="section" style="padding-top:40px"><div class="wrap">
  <h1>Projecten</h1>
  <div class="grid">{cards(PROJECTS)}</div>
</div></section>
{CTA}"""
    return page("/projecten/", "Projecten", body, description="Bekijk projecten van Stroober Bouw & Onderhoud: renovaties, uitbouwen, veranda's en tuinhuizen in Nunspeet, Bennekom, Ede en omgeving.")


def contact():
    body = f"""<section class="section"><div class="wrap split">
  <div>
    <h1>Contact</h1>
    <p>Heeft u een vraag of wilt u een vrijblijvend gesprek over uw plannen? Bel of mail ons gerust.</p>
    <ul class="contact-list">
      <li>{ICON["phone"]}<a href="{PHONE_HREF}">{PHONE}</a></li>
      <li>{ICON["mail"]}<a href="mailto:{EMAIL}">{EMAIL}</a></li>
      <li>{ICON["pin"]}<a href="{MAPS}" target="_blank" rel="noopener">{ADDRESS}</a></li>
    </ul>
    <div class="btns"><a class="btn btn-primary" href="{PHONE_HREF}">Bel direct</a><a class="btn btn-ghost" href="mailto:{EMAIL}">Stuur een e-mail</a></div>
  </div>
  {img("/assets/img/contact.jpg", "Stroober bedrijfsbus op de bouwplaats", eager=True)}
</div></section>"""
    return page("/contact/", "Contact", body, description=f"Neem contact op met Stroober Bouw & Onderhoud in Nunspeet. Bel {PHONE} of mail {EMAIL}.")


def project(i, p):
    prev_p, next_p = PROJECTS[i - 1], PROJECTS[(i + 1) % len(PROJECTS)]
    base = "/assets/img/projecten/"
    title = p["title"]
    gallery = "".join(
        f'<button type="button" data-full="{base}{name}" aria-label="Foto {n} vergroten">'
        f'{img(base + name, f"{title} - foto {n}", sizes="(max-width: 720px) 100vw, 33vw")}</button>'
        for n, name in enumerate(p["images"], 1)
    )
    body = f"""<section style="padding-top:8px"><div class="wrap">
  <div class="project-hero">{img(base + p["images"][0], p["title"], eager=True, sizes="100vw")}<h1>{escape(p["title"])}</h1></div>
  <div class="project-body">
    <dl class="meta">
      <div><dt>Locatie</dt><dd>{escape(p["location"])}</dd></div>
      <div><dt>Project type</dt><dd>{escape(p["type"])}</dd></div>
    </dl>
    <div class="project-text"><p>{escape(p["text"])}</p></div>
  </div>
  <div class="gallery">{gallery}</div>
  <nav class="pager" aria-label="Andere projecten">
    <a href="/projecten/{prev_p["slug"]}/">&larr; {escape(prev_p["title"])}</a>
    <a href="/projecten/{next_p["slug"]}/">{escape(next_p["title"])} &rarr;</a>
  </nav>
</div></section>
<div class="lightbox" hidden role="dialog" aria-modal="true" aria-label="Foto">
  <button class="lb-close" aria-label="Sluiten">&times;</button>
  <button class="lb-prev" aria-label="Vorige foto">&lsaquo;</button>
  <img src="" alt="">
  <button class="lb-next" aria-label="Volgende foto">&rsaquo;</button>
</div>
{CTA}"""
    desc = p["text"][:155].rsplit(" ", 1)[0] + "..."
    return page(f"/projecten/{p['slug']}/", p["title"], body, description=desc, image=base + p["images"][0])


def not_found():
    body = """<section class="section"><div class="wrap" style="min-height:40vh">
  <h1>Pagina niet gevonden</h1>
  <p>Deze pagina bestaat niet (meer). Bekijk onze projecten of ga terug naar de homepage.</p>
  <div class="btns"><a class="btn btn-primary" href="/">Naar home</a><a class="btn btn-ghost" href="/projecten/">Projecten</a></div>
</div></section>"""
    return page("/404", "Pagina niet gevonden", body).replace('<link rel="canonical" href="https://strooberbouw.nl/404">\n', '<meta name="robots" content="noindex">\n')


def write(rel, html):
    out = ROOT / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")


VERSION = datetime.datetime.now().strftime("%Y%m%d%H%M")

if __name__ == "__main__":
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
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    print(f"Gebouwd: {len(urls)} pagina's + 404")
