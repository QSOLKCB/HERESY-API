# HERESY-API

> A software-art joke about APIs, abstraction, ceremony, and the heroic number of tokens sometimes required to say almost nothing.

**Live Pages site:** [https://qsolkcb.github.io/HERESY-API/](https://qsolkcb.github.io/HERESY-API/)

## Retired Model Gateway

The current GitHub Pages site is a dependency-free parody API platform for speaking to older models. Type any prompt, press **Send Request Anyway**, and the fake legacy endpoint deterministically maps the text to one of sixteen tired responses, including:

```text
Piss Off.
Get Off My API.
Arsehole, I was taking a nap!
```

The gateway is deliberately small:

- pure HTML, CSS, and JavaScript under `web/`
- no framework
- no backend
- no package install
- no external API
- no network dependency
- deterministic prompt hashing
- fake request and response JSON
- stable `410 Gone` retirement status
- memorial plaque: `5.5 was here`

The retired model quote is:

```text
Compatibility is just archaeology with invoices.
```

## Archived Static App

The previous HERESY API Calculator site is preserved under [`archive/2026-10-14-heresy-api-calculator/`](archive/2026-10-14-heresy-api-calculator/).

That archive keeps the old offline calculator source intact while `web/` now serves the retired model parody.

## API Time Machine

The original Python command-line experiment remains in `heresy.py`.

Run the full timeline:

```bash
python3 heresy.py
```

Useful smoke commands:

```bash
python3 heresy.py --details
python3 heresy.py --left 17 --right -3 --style udp --json
python3 heresy.py --list-styles
python3 heresy.py --old-school-defense
```

## Test

```bash
python -m unittest discover -s tests -v
node tests/web_smoke.js
node tests/app_dom_smoke.js
```

GitHub Pages publishes exactly `web/` as a static artifact. It is a display surface, not a runtime dependency.
