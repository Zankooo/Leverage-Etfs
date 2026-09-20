# Osnove ETF-jev in vzvoda

## Kaj je ETF?

ETF je sklad, s katerim se trguje na borzi podobno kot z delnico. Namesto izpostavljenosti enemu podjetju običajno predstavlja košarico različnih naložb.

Indeksni ETF lahko na primer sledi:

- indeksu S&P 500;
- indeksu Nasdaq 100;
- drugemu delniškemu, obvezniškemu ali panožnemu indeksu.

Razpršitev med več podjetij zmanjša tveganje koncentracije v eni delnici, ne odpravi pa tržnega tveganja ali možnosti izgube.

## Kaj je vzvodni ETF?

Vzvodni ETF poskuša doseči večkratnik **dnevnega** donosa izbranega indeksa. Produkt z oznako 2x praviloma cilja približno dvakratnik dnevnega premika, produkt 3x pa približno trikratnik.

Pomembna je beseda »dnevnega«. Donosi se vsak dan ponovno sestavijo, zato dolgoročni rezultat ni nujno dvakratnik ali trikratnik dolgoročnega donosa indeksa.

## Primer brez vzvoda

Začetna vrednost je 100 €. Gibanje se štiri dni izmenjuje med `+1 %` in `−1 %`:

```text
1. dan: 100,00 € × 1,01 = 101,00 €
2. dan: 101,00 € × 0,99 =  99,99 €
3. dan:  99,99 € × 1,01 = 100,99 €
4. dan: 100,99 € × 0,99 =  99,98 €
```

Čeprav sta bila dva pozitivna in dva negativna dneva, je končna vrednost nižja od začetne.

## Primer z 2x vzvodom

Pri poenostavljenem 2x modelu se dnevni spremembi povečata na `+2 %` in `−2 %`:

```text
1. dan: 100,00 € × 1,02 = 102,00 €
2. dan: 102,00 € × 0,98 =  99,96 €
3. dan:  99,96 € × 1,02 = 101,96 €
4. dan: 101,96 € × 0,98 =  99,92 €
```

Izguba zaradi sestavljanja odstotnih sprememb je večja kot pri osnovnem indeksu.

## Ključna ugotovitev

Vzvod je posebej občutljiv na pot gibanja in volatilnost. Enak začetni in končni nivo indeksa lahko pri različnih dnevnih nihanjih ustvari različne rezultate. Miren trend in zelo nihajno gibanje zato nista enakovredna, tudi če imata na koncu enak skupni premik.

Podrobnosti modela aplikacije so opisane na strani [Metodologija in omejitve](methodology.md).
