# Stroober Bouw & Onderhoud

Website van [strooberbouw.nl](https://strooberbouw.nl): statische site op GitHub Pages (voorheen Framer), met een eigen beheeromgeving voor de klant.

## Beheer (voor de klant)

Op **strooberbouw.nl/beheer/** kan met een wachtwoord:

- projecten toevoegen, bewerken, verwijderen en de volgorde aanpassen (bovenste 4 staan op de homepage)
- foto's uploaden (worden automatisch verkleind en via TinyPNG gecomprimeerd)
- per foto de uitsnede kiezen door te slepen en te zoomen
- alle teksten, dienstfoto's en contactgegevens aanpassen

*Opslaan & publiceren* maakt één commit op `main`; de GitHub Action bouwt de site en zet hem binnen ±2 minuten live.

**Wachtwoord instellen/wijzigen:** maak een fine-grained personal access token (alleen repo `stroober-bouw`, recht *Contents: Read and write*) en vul die in via "Wachtwoord instellen" op /beheer/. Het token wordt AES-versleuteld met het wachtwoord opgeslagen in `content/admin.json`.

## Structuur

- `content/site.json`: teksten, contactgegevens en sitefoto's (met uitsnede x/y/zoom)
- `content/projects.json`: projecten
- `build.py`: genereert alle pagina's uit de content (de HTML staat niet in git)
- `beheer/index.html`: de beheeromgeving
- `compress-images.py`: TinyPNG-compressie van nieuwe foto's (bijgehouden in `assets/img/.tinypng.json`)
- `.github/workflows/deploy.yml`: comprimeren, bouwen en publiceren bij elke push

## Lokaal

```
python3 build.py && python3 -m http.server 4321
```

Open http://localhost:4321. TinyPNG lokaal draaien: `TINYPNG_API_KEY` in `.env`, dan `python3 compress-images.py`.

## Contactformulier

Verstuurt via [FormSubmit](https://formsubmit.co) naar het e-mailadres in `content/site.json` (`contactPage.formEndpoint`). Het eerste bericht levert een activatiemail op die één keer bevestigd moet worden.

## Hosting / DNS

- Domein en DNS: Hostnet. E-mail: Microsoft 365 (MX-record niet aanpassen).
- GitHub Pages: A-records `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`, `www` CNAME naar `nstroober.github.io`.
