# Metodologija in omejitve

Projekt primerja simulirane serije S&P 500, Nasdaq 100 in Nasdaq Composite pri vzvodih 1x, 2x in 3x. Serije pripravi iz zgodovinskih cen osnovnih indeksov ter pri izračunu upošteva:

- dnevno sestavljanje donosov in njegov vpliv pri nihajnosti (volatility decay);
- reinvestiranje dividend;
- stroške financiranja vzvoda (funding);
- upravljalske provizije (management fees).

Rezultati predstavljajo modelni izračun, ne zgodovinskih donosov konkretnega ETF-ja.

## Priprava serij in izračun donosa

Vhodni podatki so cene indeksa **brez reinvestiranih dividend**, saj model dividende dodaja posebej. Datumi morajo naraščati, izbrani indeks pa mora ustrezati naloženim podatkom.

Za vsak zaporedni par cen najprej izračunamo donos indeksa:

```text
donos_indeksa = (trenutna_cena − prejšnja_cena) / prejšnja_cena
```

Nato vključimo vzvod, dividende in stroške:

```text
donos_serije = vzvod × (donos_indeksa + dividende_obdobja)
               − (vzvod − 1) × funding_obdobja
               − provizija_obdobja

nova_vrednost = prejšnja_vrednost × (1 + donos_serije)
```

Vsi donosi in stopnje v enačbah so decimalni: `0.02` pomeni 2 %. Če indeks zraste za 0,5 %, je cenovni prispevek pri 2x vzvodu 1 %, pri 3x pa 1,5 %; končni donos vključuje še dividende in stroške.

Prva vrednost serije je enaka prvi vhodni ceni, njen donos pa je `0.0`. Obračun se začne pri naslednjem datumu. Enak postopek velja tudi za 1x, kjer ni stroška financiranja, dividende in upravljalska provizija pa se upoštevajo.

## Dnevno sestavljanje donosov in volatility decay

Vsak naslednji donos se uporabi na že spremenjeni vrednosti. Pozitivna in enako velika negativna odstotna sprememba se zato ne izničita. Primer brez dividend in stroškov:

```text
1x: 100 € × 1,01 × 0,99 = 99,99 €
2x: 100 € × 1,02 × 0,98 = 99,96 €
```

Ta učinek je v simulaciji posledica sestavljanja donosov; ne odštevamo ga kot dodatno provizijo. Končni rezultat je odvisen od poteka dnevnih donosov, zato letni donos 2x ali 3x serije ni preprosto dvakratnik ali trikratnik letnega donosa indeksa.

Več primerov je na strani [Osnove ETF-jev](etf-basics.md).

## Obračun dividend in stroškov

Letne stopnje preračunamo glede na pretekle **koledarske dni** med zaporednima datumoma:

```text
prispevek_obdobja = letna_stopnja × pretekli_dnevi / dni_v_letu
```

Uporabimo 365 oziroma 366 dni v letu. Od petka do ponedeljka tako obračunamo tri dni, tudi če vmes ni trgovalnih podatkov. Ob prehodu leta obdobje razdelimo in seštejemo prispevke z ustreznimi stopnjami ter številom dni za vsako leto.

### Dividende

Letni dividendni donos za izbrani indeks preberemo iz polja `dividende` v datoteki `backend/obcasno_pogosti_fajli/letne_stopnje.json`. Sorazmerni prispevek prištejemo cenovnemu donosu in oboje pomnožimo z vzvodom.

Dividende se tako sproti reinvestirajo. To je enakomeren letni približek, ki ne sledi dejanskim datumom izplačil.

### Glavni strošek

**Financiranje vzvoda (funding)** se obračuna na dodatno izpostavljenost nad lastnim kapitalom. Letno stopnjo preberemo iz polja `funding` v isti datoteki; za posamezno leto je skupna vsem trem indeksom.

```text
funding_obdobja = letna_stopnja_fundinga × pretekli_dnevi / dni_v_letu
strošek_fundinga = (vzvod − 1) × funding_obdobja
```

| Vzvod | Dodatna izpostavljenost | Strošek financiranja |
|---|---|---|
| 1x | Brez dodatne izpostavljenosti | 0 |
| 2x | Enkratnik lastnega kapitala | 1 × funding obdobja |
| 3x | Dvakratnik lastnega kapitala | 2 × funding obdobja |

Strošek odštejemo od donosa serije. Izražen je kot delež njene prejšnje vrednosti.

**Primer:** pri 2x vzvodu in 5 % letni stopnji je strošek za en dan v 365-dnevnem letu `0,05 / 365 ≈ 0,000137`, oziroma **0,0137 %**. Pri vrednosti 10.000 € to pomeni približno **1,37 €**. Pri 3x vzvodu je ob enakih pogojih strošek dvakrat tolikšen.

### Upravljalske provizije

Model uporablja naslednje fiksne letne provizije:

| Indeks | 1x | 2x | 3x | Opomba |
|---|---:|---:|---:|---|
| S&P 500 | 0,07 % (SXR8.DE) | 0,60 % (DBPG.DE) | 0,75 % (3USL.L) | |
| Nasdaq 100 | 0,30 % (SXRV.DE) | 0,60 % (LQQ.PA) | 0,75 % (LQQ3.L) | |
| Nasdaq Composite | 0,30 % | 0,60 % | 0,75 % | Brez referenčnih ETF-jev; predpostavljamo enake stroške kot pri Nasdaq 100. |

Upravljalske provizije so prevzete iz dejanskih etf-jev iz spletne strani https://www.justetf.com/en/

Provizijo izberemo glede na indeks in vzvod, jo sorazmerno preračunamo na koledarske dni ter odštejemo od donosa **enkrat, brez dodatnega množenja z vzvodom**.

Te stopnje so nastavitve simulacije in veljajo za celotno zgodovino. Za Nasdaq Composite model uporablja enake provizije kot za Nasdaq 100; tabela ne predstavlja zgodovine provizij posameznih tržnih produktov.

## Omejitve in razlaga rezultatov

Model vključuje navedene donose in stroške, ne pa vseh okoliščin dejanske naložbe:

- Dividende in funding temeljijo na letnih stopnjah, upravljalske provizije pa so skozi čas fiksne.
- Davki, posredniške provizije, razmik med nakupno in prodajno ceno ter valutne spremembe niso posebej modelirani.
- Odstopanja dejanskega produkta od ciljnega dnevnega vzvoda niso vključena.
- Manjkajoče letne stopnje oziroma vrednosti `null` ustavijo pripravo serije; ne nadomestijo se samodejno z ničlo.
- Pri izračunanem donosu −100 % ali manj se priprava ustavi, ker model ne more nadaljevati s pozitivno vrednostjo.

Donosi se ob pripravi serij ne zaokrožujejo. Pripravljeni stolpec `Daily Return` že vsebuje dividende in navedene stroške, zato jih pri nadaljnjem izračunu naložbe ne odštevamo ponovno. Spremembe nastavitev začnejo veljati v shranjenih podatkih šele po ponovni pripravi serij.

Backtest pokaže rezultat modela v izbranem zgodovinskem obdobju. Zgodovinski rezultat ne zagotavlja prihodnjega donosa; vzvod poveča tako izpostavljenost rasti kot padcem.
