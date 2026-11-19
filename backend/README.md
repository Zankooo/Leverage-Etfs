
# Navodila za namestitev in delovanje
## MacOS
Ustvari okolje:
```bash
python3 -m venv .venv
```
Aktiviraj okolje:
```bash
source .venv/bin/activate
```

Instaliraj knjiznice:
```bash
python -m pip install -r requirements.txt
```
Zaženi:
```bash
uvicorn main:app --reload
```

## Windows

Ustvari okolje:
```bash
python -m venv .venv
```
Aktiviraj okolje:
```bash
.venv\Scripts\activate
```

Instaliraj knjiznice:
```bash
python -m pip install -r requirements.txt
```
Zaženi:
```bash
uvicorn main:app --reload
```

## Jeziki grafov

Obe POST-zahtevi sprejemata `language: "sl"` ali `language: "en"`; če polje
manjka, se uporabi slovenščina. Prevodi grafov in nastavitev orodne vrstice
Plotly so v `prevodi_grafov.py`. Jezik ne spreminja številčnih izračunov.

`/html-files` shrani rezultate v lastno mapo simulacije in vrne povezavi za oba
jezika. `GET /graf/{simulation_id}/{language}/{filename}` drugi jezik po potrebi
izriše iz istega CSV-ja. Podrobnosti in primeri JSON-a so v `docs/api.md`.

## Preverjanje

V mapi `backend` namesti testne odvisnosti in zaženi teste:

```bash
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
```

Testi preverijo oba jezika, enake številčne podatke, privzeti jezik, validacijo,
ločene simulacije, uporabo shranjenih grafov in prenos jezika v vzporedni izris.
