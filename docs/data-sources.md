# Viri podatkov

Projekt uporablja zgodovinske podatke treh ameriških indeksov. Spodnje povezave so izhodišča, navedena ob razvoju projekta.

## S&P 500

Indeks ima najdaljšo zgodovino med tremi uporabljenimi nizi.

- [S&P 500 Historical Data – Kaggle](https://www.kaggle.com/datasets/paveljurke/s-and-p-500-gspc-historical-data)

## Nasdaq Composite

- [Nasdaq Historical Chart – Macrotrends](https://www.macrotrends.net/1320/nasdaq-historical-chart)
- [NASDAQCOM – Federal Reserve Economic Data](https://fred.stlouisfed.org/series/NASDAQCOM)

## Nasdaq 100

- [NASDAQ100 – Federal Reserve Economic Data](https://fred.stlouisfed.org/series/NASDAQ100)

## Lokalna organizacija podatkov

```text
backend/
├── podatki_ustvarjeni/   # osnovni indeksi
├── 2x-leverage/          # simulirane dnevne 2x spremembe
└── 3x-leverage/          # simulirane dnevne 3x spremembe
```

Pred zamenjavo ali posodobitvijo podatkov je treba preveriti format datumov, manjkajoče vrednosti, vrstni red zapisov in uporabljeni cenovni stolpec. Različni viri lahko uporabljajo različne definicije cen ali vključujejo različna obdobja.
