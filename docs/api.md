# API

Lokalni osnovni naslov backenda je:

```text
http://localhost:8000
```

FastAPI samodejno ustvari interaktivno dokumentacijo:

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- OpenAPI JSON: [http://localhost:8000/openapi.json](http://localhost:8000/openapi.json)

## `GET /`

Preveri, ali backend deluje.

Primer odgovora:

```json
{
  "message": "Backend deluje"
}
```

## Skupno telo POST-zahtev

Oba simulacijska endpointa sprejmeta enako JSON-telo:

```json
{
  "zacetna_investicija": 1000,
  "mesecni_vlozek": 100,
  "indeks": "S&P 500",
  "interval": 15,
  "tip_intervala": "mesecni",
  "language": "en"
}
```

| Polje | Tip | Pomen |
| --- | --- | --- |
| `zacetna_investicija` | integer | Začetni vložek v evrih |
| `mesecni_vlozek` | integer | Redni mesečni vložek v evrih |
| `indeks` | string | `S&P 500`, `Nasdaq 100` ali `Nasdaq Composite` |
| `interval` | integer | Dolžina simulacije v letih; frontend dovoljuje 1–50 |
| `tip_intervala` | string | `letni`: začetek vsako leto; `mesecni`: začetek vsak mesec. Neobvezno, privzeto `mesecni`. |
| `language` | string | Jezik grafov: `sl` ali `en`. Neobvezno, privzeto `sl`; druga vrednost vrne napako 422. |

Začetek je prvi razpoložljivi trgovalni dan izbranega leta oziroma meseca.
Izbira tipa intervala ne spremeni dolžine simulacije v letih ali mesečnih vplačil.
Oba endpointa morata prejeti isti tip intervala, da se primerjave in grafi ujemajo.
Frontend pošlje trenutni jezik v obeh zahtevah. `language` vpliva na prikaz grafov,
ne na izračun, vrednosti ali imena polj v JSON-u.

## `POST /primerjava_vrstic`

Izvede simulacije in vrne povzetek ter razvrstitev 1x, 2x in 3x strategije za vsak zgodovinski interval.

Poenostavljen primer odgovora:

```json
{
  "summary": {
    "zacetna_investicija": 1000.0,
    "vse_mesecne_investicije": 18000.0,
    "skupaj_investirano": 19000.0,
    "wins": {
      "osnoven.csv": { "count": 10, "procent": 20.0 },
      "vzvod-2x.csv": { "count": 25, "procent": 50.0 },
      "vzvod-3x.csv": { "count": 15, "procent": 30.0 }
    },
    "total_compared": 50
  },
  "rows": [
    {
      "datum": "1927-12-30-1942-12-30",
      "best": {
        "file": "vzvod-2x.csv",
        "compare_value": 25000.0,
        "gain": 6000.0,
        "total": 25000.0
      },
      "second": {},
      "third": {},
      "diff_best_second_pct": 12.5,
      "diff_second_third_pct": 8.2
    }
  ]
}
```

Vrednosti v tem primeru so ilustrativne; dejanski odgovor je odvisen od parametrov in zgodovinskih podatkov.

## `POST /html-files`

Pripravi podrobne rezultate, ustvari HTML-graf za vsak interval in vrne seznam grafov.
Prvotne grafe ustvari v zahtevanem jeziku. Vsaka simulacija dobi svoj `simulation_id`.

Primer odgovora:

```json
{
  "simulation_id": "0123456789abcdef0123456789abcdef",
  "language": "en",
  "results": [
    {
      "id": 1,
      "title": "1927-12-30--1942-12-30",
      "filename": "1927-12-30--1942-12-30.html",
      "url": "http://localhost:8000/graf/0123456789abcdef0123456789abcdef/en/1927-12-30--1942-12-30.html",
      "urls": {
        "sl": "http://localhost:8000/graf/0123456789abcdef0123456789abcdef/sl/1927-12-30--1942-12-30.html",
        "en": "http://localhost:8000/graf/0123456789abcdef0123456789abcdef/en/1927-12-30--1942-12-30.html"
      }
    }
  ]
}
```

## `GET /graf/{simulation_id}/{language}/{filename}`

Vrne HTML-graf v izbranem jeziku. Če ta prevod še ne obstaja, ga izriše iz
shranjenega CSV-ja in shrani za naslednje odprtje. Izračuna naložbe ne ponavlja.
Neznana simulacija ali datoteka vrne 404, neveljaven jezik ali ID pa 422.

Frontend uporablja `urls[locale]` kot `src` za `iframe`. Menjava jezika tako
prevede tudi že izračunan graf, pri čemer vnosi in rezultati ostanejo isti.
Deluje tudi, če uporabnik spremeni jezik med čakanjem na prvotni izračun.

Rezultati in parametri so v `rezultati-vsak-interval-vsi-indeksi/{simulation_id}/`,
grafi pa v `mapa-grafi/{simulation_id}/{language}/`. Nova simulacija ne prepiše
prejšnje. Datoteke ostanejo do ročnega čiščenja teh izhodnih map.

Obstoječa statična pot `/grafi/{filename}` ostane na voljo za stare grafe.

## Napake

Če telo zahteve ne ustreza Pydantic modelu, FastAPI običajno vrne status `422 Unprocessable Entity` s podrobnostmi validacije. Napake med samim izračunom trenutno nimajo posebnega aplikacijskega formata in se lahko vrnejo kot splošna strežniška napaka.
