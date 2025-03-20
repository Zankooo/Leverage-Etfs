# Leverage etf

## Branchi:
- main -> ki je glaven in to kar dela fix dela
- collection -> ki zbira dobro kodo (primarni namen da ce zaserjem na coding da si povrnem iz brancha collection)
- coding -> kjer se programira

### ---------

## Cilji:
Delat program, da je sam zame in moje analize! Ce bom hotel naknadno za webapp in da lahk o tudi drug folk uporablja pa naredim to, ce bo cas!
- Sprogramirat da ti izracuna uspesno brez napak donose za vsak dan ob danem csv, fileu
- potem da je lahko sintaksa datuma lahko drugačna
- potem pa že s kešom da investiraš (v navadnega ne leverage) ampak pogledat na chatu kko to gre, pac zacet da vsak mesec prvega vrzes notri
- in se s tem igrat da bo dovrseno
- in pol preit na leverage in pogledat na chatu kako iz navadnega naredit leverage, pac a samo 2x das 
- in pol investiranje pri leverage je isto ce prvega investiras v mesecu
- in pol se zacet zafrkavat s kombinacijo
- mogoce tudi na koncu user interface kjer lahko uploadas csv in izberes od katerega leta do katerega
- in kle se lahko zmisljujem kolikor hocem s temi funkcionalnostmi
- JE PA NAJBOLJ POMEMBNO DA IZ UNEGA NAVADNEGA USPESNO NAREEDIM LVERAGE - CHATA PRASAT IN POL V ENEM ZACNEM RECIMO UNE PRIMERE K SO V WORDU


## Andro talk, latest goals:
- naredit oci strategijo da vedno ko je recimo 3% dol prodas in vedno ko je 3% gor kupis. In tako za poljuben posto
- ugotovit kako je leverage narejen pac, kako ga naredit iz osnovnega indeksa
- potem ko bom ta csv naredil -> naredit kak primer ze
- potem sprogramirat da das lahko kes kadarkolli notri ne samo prvega v mesecu
- potem pa zacet uporabljat strategije, rado in reddit in tko. torej vkljucit v projekt

## Kaj je narejeno:
- mi operiramo z indeksom, ki je v csv fileu, ampak preden zacnemo delat izracune, morajo te podatki biti v dogovorjenem formatu, ki smo ga dolocili. Da spravimo podatke v tak format imamo vse opisano v classu **csv_operacije.py** kako to naredit in pravtako so tam funkcije ki nam pomagajo spravit v ta format
- potem pa lahko gremo delat izracune. Razne metode oz. taktike investiranja so napisane v classu **izracuni.py**
    - <u>Prva funkcija</u>: *izracun_dnevnih_sprememb* -> izracuna nam dnevne spremembe daily changes
    - <u>Druga funkcija</u>: *izracun_dobicka_mesecne_investicije_prvega* -> izracuna nam koliko imamo kesa po nekem izbranem obdobju, uposteva tudi mesecne vlozke prvi trgovalni dan v mesecu.
    - <u>Tretja funkcija</u>: *izracun_dobicka_prodaj_kupi* -> funkcija ki izracunava taktiko; gremo vedno prodat ko pade za nek procent in kupimo vedno ko zraste nek procent od 
    - <u>Cetrta funkcija</u>: *izracun leverage

## Problemi:
- leverage se niti priblizno ne ujema z sso(ameriski sp500 2x) recimo. sso = 2x leverage in se ne ujema z mojim izracunom leverage, to najboljse opazimo ce damo neko obdobje in 100eur zacetne in nic mesecnih, procentualno bo cist drugace -> se enkrat cekirat
- ce dam leverage faktor 1 ne dobim isto kot je osnovni, to mi je smeh pac
- unedve funkcije buy sell nisem ziher ce prav delata