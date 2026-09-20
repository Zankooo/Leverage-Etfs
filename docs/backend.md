# Backend

Backend je FastAPI aplikacija, ki bere zgodovinske podatke indeksov, izvaja simulacije za osnovni, 2x in 3x vzvod ter ustvarja rezultate in HTML-grafe.

## Pomembne datoteke

| Datoteka ali mapa | Namen |
| --- | --- |
| `backend/main.py` | FastAPI aplikacija, endpointi in glavni potek |
| `backend/izracuni.py` | Izračuni investicij in priprava CSV-rezultatov |
| `backend/testing_file.py` | Primerjava osnovnega, 2x in 3x rezultata |
| `backend/grafi.py` | Izdelava grafov |
| `backend/obcasno_pogosti_fajli/` | Pomožne funkcije za CSV in konzolni izpis |
| `backend/podatki_ustvarjeni/` | Podatki osnovnih indeksov |
| `backend/2x-leverage/` | Umetno ustvarjeni dnevni 2x donosi |
| `backend/3x-leverage/` | Umetno ustvarjeni dnevni 3x donosi |

## Zagon aplikacije

Backend je treba zagnati iz mape `backend`:

```bash
cd backend
uvicorn main:app --reload --port 8000
```

To je pomembno, ker deli kode uporabljajo relativne poti, na primer `podatki_ustvarjeni/sp-500.csv` in `mapa-grafi`.

## Inicializacija

Ob uvozu `main.py` backend:

1. ustvari FastAPI aplikacijo;
2. določi mape za grafe in rezultate;
3. priklopi mapo grafov na URL `/grafi`;
4. nastavi CORS za frontend na portu `3000`;
5. v pomnilnik naloži osnovne, 2x in 3x podatke treh indeksov.

Podprti indeksi so:

- S&P 500;
- Nasdaq 100;
- Nasdaq Composite.

## Pot izračuna

`POST /primerjava_vrstic` izbere podatke indeksa, izvede simulacijo za vse možne intervale in primerja končne vrednosti strategij 1x, 2x in 3x.

`POST /html-files` ponovno pripravi podrobne rezultate, ustvari HTML-grafe in vrne njihove javne URL-je.

## Statične datoteke

FastAPI objavi mapo `backend/mapa-grafi/`:

```text
backend/mapa-grafi/primer.html
             ↓
http://localhost:8000/grafi/primer.html
```

Frontend ta URL odpre v `iframe`.

## Model vhodnih podatkov

Razred `podatki_iz_frontenda` zahteva štiri polja:

```python
class podatki_iz_frontenda(BaseModel):
    zacetna_investicija: int
    mesecni_vlozek: int
    indeks: str
    interval: int
```

FastAPI in Pydantic preverita prisotnost in osnovni tip teh polj. Dodatne omejitve, kot so dovoljene vrednosti indeksa in interval med 1 ter 50, se trenutno preverjajo predvsem na frontendu.

## Pomembna finančna omejitev

Podatki 2x in 3x ne predstavljajo zgodovine dejanskih vzvodnih ETF-jev. Nastali so z množenjem dnevnih sprememb osnovnega indeksa. Simulacija trenutno ne vključuje vseh stroškov skladov, financiranja, davkov in drugih realnih dejavnikov, zato rezultat ni investicijsko priporočilo.
