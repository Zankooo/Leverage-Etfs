# Vzvodni ETF primerjalnik 


## Prvo; kaj je ETF?
- To je sklad, ki se tako kot recimo delnica podjetja Apple, trguje na borzi 
- Glavna razlika je, da če kupimo delnico Apple, smo lastniki samo podjetja Apple, v etf skladu so pa mnoge delnice... Sp500 je recimo skupek največjih ameriških podjetij, kjer so podjetja razvrščena po velikosti. Večje kot je podjetje večji procent tega podjetja je v indeksu (etfju). V Nasdaq 100 je sto največjih tehnoloških podjetij...
- Etf isto kupuješ/prodajaš 
- ETF-ji razpršijo tveganje: z eno naložbo kupiš košarico podjetij, ne staviš “all-in” na eno ime. Posamezna delnica lahko na dolgi rok zastane ali pade — tveganje koncentracije je veliko.Zmagovalci se menjajo: nekoč so bili top (Exxon, General Electric, Citigroup, Aig), danes pa (Nvidia, Microsoft, Apple, Google, Amazon, Meta).
- Za dolg rok ima etf boljse razmerje med donosnostjo izgubo in mirnim spanjem -> in vedno se je pobral in prišel spet na vrh! Če se je vedno do sedaj v 98 letni zgodovini sp500 pobral, se bo ob kakšnih padcih v bodoče tudi zagotovo pobral. 


## Kaj je pa ETF z vzvodom (leverage ETF)?
- vzvod si lahko predstavljamo, da je recimo nek etf krat 2 ali krat 3.
- torej sp500 z vzvodom dva, je sp500 2x, to pomeni da je dvakratnik sp500

## Problemi oz. fora vzvoda?
- zdej če to bere nek laik si misli; gremo na glavo. Če je lani sp500 zrastel za 10% je vzvod 2x zrastel za 20% in vzvod 3x 30%. 
- ampak ni tako. Vemo da je vse 'gor dol'. 
    - Primer 1: Imamo prvi dan 100eur investirano in osnoven sp500 zraste 1% -> imamo 101eur. Drugi dan pa pade 1% -> imamo 99,99eur. Torej imamo manj kot smo imeli. Gremo naprej. Tretji dan spet zraste za 1% -> imamo 100,9899eur. Četrti dan pade za 1% -> imamo 99,98eur. In tako naprej... 
    - Primer 2: Imamo prvi dan 100eur investirano in 2x vzvod sp500 zraste 2% -> imamo 102eur. Drugi dan pa pade 2% -> imamo 99,96eur. Torej imamo manj kot smo imeli. Gremo naprej. Tretji dan spet zraste za 2% -> imamo 101,9592eur. Četrti dan pade za 2% -> imamo 99,92eur. In tako naprej...
- vidimo problem ane? Več kot je nihanja gor dol, volatilnost, slabše je za vzvod. Ker se matematično zgublja donos. Zdej si pa predstavljajmo da imamo vzvod delnice Tesle, ki je znana da gre veliko gor dol. Osnovna 3% gor in 3% dol. Vzvod v tem primeru 6% in 6% dol. Koliko hitreje bi izgubljali!

## Ugotovitev
- torej za vzvod je najboljše, da čim manj niha gor dol. Potencialno če bi nekdo garantiral da bo podjetje vsak dan zraste le 0,01%, kupil bi čim večji vzvod tega podjetja in zmagal bi. 
- torej volatilnost uničuje donos. Zato ni fajn kupovat vzvoda individualnih delnic ker individualne delnice še toliko bolj nihajo in donos se drastično izgubi. 
- za vzvod je idealno da je čim manj gor dol in počasna a vztrajno rast. 

## Aplikacija kaj dela?

Primerja donosov 1x, 2x in 3x različic izbranega indeksa (S&P 500, Nasdaq 100 ali Nasdaq Composite) ob vnosu:
- začetne investicije,
- mesečnih vplačil,
- dolžine vlaganja (v letih).

## Kako deluje
1. Uporabnik vnese:
   - začetno investicijo,
   - mesečno investicijo,
   - dolžino investiranja v letih (interval),
   - indeksa (S&P 500 / Nasdaq 100 / Nasdaq Composite).
2. Program nato naredi izračune na vsakem obdobju. Recimo da smo izbrali S&P 500, naredi na navadnem, na 2x in 3x na vsakem obdobju za izbran interval
3. Za vsako celo leto do izbranega intervala izračuna “koliko imamo vse skupaj” ob upoštevanju začetnega in mesečnih vplačil.
4. V vsakem intervalu potem nam program pove kater je bil najboljši. In nam rezultate tudi izpiše 


## Rezultati prikazani v konzoli

```
Datum | NAJBOLJSI (narejen plus/minus, vse skupaj) >> +% >> DRUGI (narejen plus/minus, vse skupaj) >> +% >> TRETJI (narejen plus/minus, vse skupaj)

1927-12-30-1942-12-30 | -7,206.13, 20,793.87 >> +101.04% >> -17,657.02, 10,342.98 >> +76.72% >> -22,147.38, 5,852.62  
1928-01-03-1943-01-04 | -6,819.44, 21,180.56 >> +96.52% >> -17,222.36, 10,777.64 >> +72.56% >> -21,754.20, 6,245.80  
                                                    .
                                                    .
                                                    . 
2009-01-02-2024-01-02 | 431,121.24, 459,121.24 >> +77.99% >> 229,943.81, 257,943.81 >> +168.07% >> 68,221.12, 96,221.12  
2010-01-04-2025-01-06 | 571,790.10, 599,790.10 >> +101.72% >> 269,337.82, 297,337.82 >> +190.8% >> 74,249.64, 102,249.64  

Direktna primerjava med testing/osnoven.csv, testing/vzvod-2x.csv in testing/vzvod-3x.csv  

💰 Začetna investicija: 10000  
📈 Vse mesečne investicije: 18000  
💵 Vse skupaj investirano: 28000  

Procenti so izračunani na podlagi 'koliko imamo vse skupaj'  

✔ testing/osnoven.csv je bil najboljši v 14 primerih (16.67%)  
✔ testing/vzvod-2x.csv je bil najboljši v 12 primerih (14.29%)  
✔ testing/vzvod-3x.csv je bil najboljši v 58 primerih (69.05%)  

🏆 'Najboljši' je tisti z največjo vrednostjo v stolpcu 'koliko imamo vse skupaj'  
```

## Namestitev programa
1. Kloniraj repozitorij:
   - git clone https://github.com/Zankooo/Leverage-Etfs.git
2. Namesti potrebne knjiznice:
   - python3 -m pip install -r requirements.txt (za MacOs)
   - python3 -m pip install -r requirements.txt (Windows)
3. Ustvari in aktiviraj virtualno okolje:
   - python -m venv .venv
   - Windows: .venv\Scripts\activate
   - macOS/Linux: source .venv/bin/activate


## Zagon programa (CLI)
- python main.py

<hr>

## Sekundarna funkcionalnost
Poleg primarne funkcionalnosti, ki je opisana v besedilu zgoraj, program ponuja tudi nekaj drugih funkcionalnosti.
- da pridobis zgodovinske podatke iz interneta in jih iz napisanimi funkcijami preoblikujes v obliko s katero lahko potem delas analize
- navadno obrestovanje 
- obrestno obrestovanje 


### Sp500 (ustvarjen leta 1927)
- https://www.kaggle.com/datasets/paveljurke/s-and-p-500-gspc-historical-data - do danes 

### Nasdaq composite (ustvarjen bil 1971)
- https://www.macrotrends.net/1320/nasdaq-historical-chart -> ampak je le chart
- https://fred.stlouisfed.org/series/NASDAQCOM  -> od leta 1971

### Nasdaq 100 (ustvarjen bil 1985)
- https://fred.stlouisfed.org/series/NASDAQ100 - od leta 1986, eno leto kasneje
