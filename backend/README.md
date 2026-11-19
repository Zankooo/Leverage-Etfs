
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

`/html-files` izračuna rezultate in nariše grafe v poslanem jeziku. Vrne en URL
za vsak HTML-graf, ki ga obstoječa statična pot `/grafi/` prikaže v brskalniku.
Kasnejša menjava jezika na frontendu ne spreminja grafov; za drug jezik je
potreben nov klik na Izračunaj. Podrobnosti in primeri JSON-a so v `docs/api.md`.
