# Stroober Bouw & Onderhoud

Website van [strooberbouw.nl](https://strooberbouw.nl), statische HTML gehost op GitHub Pages (voorheen Framer).

## Structuur

- `content/projects.json`: alle projecten (titel, locatie, type, tekst, foto's)
- `build.py`: genereert alle pagina's (`index.html`, `over/`, `projecten/`, `contact/`, `404.html`, `sitemap.xml`)
- `assets/`: CSS, JS, fonts (lokaal gehost) en afbeeldingen
- `compress-images.py`: TinyPNG compressie (key in `.env` als `TINYPNG_API_KEY`)

## Project toevoegen

1. Foto's klaarzetten (verkleint naar 1600px + 800px variant en comprimeert via TinyPNG):
   ```
   python3 compress-images.py ~/Downloads/foto1.jpg mijn-project-1.jpg
   python3 compress-images.py ~/Downloads/foto2.jpg mijn-project-2.jpg
   ```
2. Project toevoegen bovenaan `content/projects.json` (eerste foto = omslagfoto; de bovenste 4 staan op de homepage).
3. `python3 build.py`
4. Commit en push: GitHub Pages publiceert automatisch.

Lokaal bekijken: `python3 -m http.server 4321` en open http://localhost:4321

## Hosting / DNS

- Domein en DNS: Hostnet. E-mail: Microsoft 365 (MX-record niet aanpassen).
- GitHub Pages: A-records `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`, `www` CNAME naar `nstroober.github.io`.
