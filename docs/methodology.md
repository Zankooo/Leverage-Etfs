# Metodologija in omejitve

Ta stran opisuje, kako projekt pripravi vzvodne podatke in katere omejitve je treba upoštevati pri razlagi rezultatov.

## Simulirani 2x in 3x podatki

Projekt ne uporablja celotne zgodovine dejanskih vzvodnih ETF-jev. Ti produkti nimajo tako dolge zgodovine kot osnovni indeksi, zato aplikacija iz dnevnih sprememb osnovnega indeksa pripravi sintetični različici:

```text
dnevna sprememba 1x × 2 → dnevna sprememba 2x
dnevna sprememba 1x × 3 → dnevna sprememba 3x
```

Če se osnovni indeks v enem dnevu premakne za `+0,5 %`, je simulirana sprememba 2x `+1,0 %`, sprememba 3x pa `+1,5 %`. Enak princip velja pri padcu.

To je poenostavljen model dnevnega vzvoda, ne rekonstrukcija konkretnega tržnega produkta.

## Volatility decay

Pozitivna in enako velika negativna odstotna sprememba se ne izničita:

```text
100 € × 1,01 × 0,99 = 99,99 €
```

Pri 2x vzvodu je učinek večji:

```text
100 € × 1,02 × 0,98 = 99,96 €
```

Ker se donosi sestavljajo dnevno, visoka nihajnost lahko sčasoma zmanjša rezultat vzvodne strategije. Letnega donosa 2x ali 3x produkta zato ni pravilno oceniti samo z množenjem letnega donosa osnovnega indeksa.

Več primerov je na strani [Osnove ETF-jev](etf-basics.md).

## Stroški, ki niso vključeni

Trenutna simulacija ne modelira vseh dejavnikov dejanske naložbe, med drugim:

- upravljavskih stroškov ETF-ja;
- stroškov financiranja vzvoda;
- odstopanja od ciljnega dnevnega donosa;
- trgovalnih stroškov in razmika med nakupno ter prodajno ceno;
- davkov;
- razlik med indeksom in dejanskim skladom.

Ti stroški so pri vzvodnih produktih posebej pomembni in lahko dolgoročno bistveno vplivajo na rezultat.

## Razlaga rezultatov

Backtest pokaže, kako bi se poenostavljena strategija obnesla v izbranih zgodovinskih obdobjih. Ne dokazuje, da se bo enak rezultat ponovil v prihodnosti. Zgodovinska rast indeksa ni zagotovilo prihodnje rasti, vzvod pa poveča tako potencialne dobičke kot izgube.
