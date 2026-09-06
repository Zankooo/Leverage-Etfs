# Leverage ETFs

Dokumentacija aplikacije za zgodovinsko primerjavo osnovnih in vzvodnih indeksov.

Aplikacija za izbrani indeks in investicijske parametre simulira strategije 1x, 2x in 3x, jih primerja po zgodovinskih intervalih ter prikaže povzetek in grafe.

## Začni tukaj

- [O aplikaciji](overview.md) – kaj aplikacija dela in kako so prikazani rezultati.
- [Namestitev in zagon](installation.md) – zagon backenda, frontenda in dokumentacije.
- [Arhitektura](architecture.md) – pregled komponent in podatkovnega toka.
- [Metodologija in omejitve](methodology.md) – kako nastanejo simulirani podatki in česa rezultat ne upošteva.

## Tehnična dokumentacija

| Področje | Opis |
| --- | --- |
| [Frontend](frontend.md) | Vue 3, routing, stanje in prikaz rezultatov |
| [Backend](backend.md) | FastAPI, izračuni, CSV-datoteke in grafi |
| [API](api.md) | Endpointi, zahteve in odgovori |

## Lokalni naslovi

```text
Frontend        http://localhost:3000
Backend         http://localhost:8000
Dokumentacija   http://127.0.0.1:8001
```

> Projekt je namenjen zgodovinski analizi in izobraževanju. Rezultati niso investicijsko priporočilo in ne napovedujejo prihodnjih donosov.
