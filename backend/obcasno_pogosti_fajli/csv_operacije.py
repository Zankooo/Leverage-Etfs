"""Branje in urejanje CSV-jev ter priprava serij z vzvodom.

Vse operacije so zbrane tukaj. Običajni potek pri ročni pripravi:
    podatki = load_csv(pot)
    rezultat = naredi_leverage_iz_osnovnega(podatki)
    ustvari_nov_csv_file(rezultat)

Pred izračunom po potrebi uredi datume, vrstni red in stolpce s pomočnimi
funkcijami spodaj. Letne stopnje so v letne_stopnje.json v isti mapi.
"""

import csv
import json
from calendar import isleap
from datetime import date, datetime
from math import isfinite
from pathlib import Path


POT_LETNE_STOPNJE = Path(__file__).resolve().with_name("letne_stopnje.json")

#TO FUNKCIJO VEDNO KLICEMO KER PAC NALOZI PODATKE
def load_csv(filepath):
    """
    Prebere CSV datoteko in vrne podatke kot dvojni array (list of lists).
    """
    print()
    with open(filepath, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        array = [row for row in csv_reader]
        print(f"Csv file '{filepath}' naložen! ✅")
        return array

#----------------------------------------------------------------------------------------------------------------
#DOGOVORJEN FORMAT V CSV-JA S KATERIM DELAMO ANALIZE NATO; PO VRSTICAH:
# 1. IME INDEKSA, LETO ZAČETEK-LETO KONEC
# 2. DATUM, CLOSE-PRICE
# 3. [DATUM-NAJMLAJSI], [CLOSE-PRICE]
# N. [DATUM-NAJSTAREJSI], [CLOSE-PRICE]

#PRIMER
# 1. NASDAQ 100, 1986-2025
# 2. Date,Close-Price
# 3. 1986-01-02,131.250
# ...
# N. 1999-05-26,2053.040

# OPOMBA; CE JE HOLIDAY BIL NA DAN, NESME BIT DATUM IN PRAZEN TECAJ
# AMPAK CE JE BIL HOLIDAYS TEGA DATUMA SPLOH NE SME BIT NOTRI, TOREJ MOREMO GA FUKNT VEN

# TOREJ:
# TE FUNKCIJE V TEMU CLASSU PA IMAMO DA CSV SPRAVIMO V DOGOVORJENO OBLIKO,
# IN ZADNJO FUNKCIJO KLICEMO DA NAM USTVARI FILE IZ OBDELANEGA CSVJA KI JE POTEM PRIPRAVLJEN ZA ANALIZE

# AMPAK VEDNO PA DAJMO V PRVO VRSTICO NASLOV IN OD KDAJ DO KDAJ
# DRUGA VRSTICA PA IMENA PODATKOV
# TO TAKOJ NA ZACETKU, TUDI PREDEN GREMO UREJAT CSV FILE DA BO SPREMAN ZA ANALIZE

def obrni_csv(podatki):
    """
    Funkcija, ki sprejme dvojni seznam/array (CSV podatke),
    in obrne vrstni red vseh vrstic od tretje vrstice naprej.
    Prvi dve vrstici ('naslovna' dela CSV-ja) ostaneta nespremenjeni.
    @param podatki: seznam seznamov (CSV podatki)
    @return: obrnjen seznam seznamov
    """
    print("--------------------------------")
    print("Funkcija ki obraca csv podatke laufa")
    prva_vrstica = podatki[0]
    druga_vrstica = podatki[1]
    # Obrnemo vrstni red od tretje vrstice naprej
    obrnjeni_podatki = list(reversed(podatki[2:]))
    print("Podatke smo obrnili ✅")
    return [prva_vrstica, druga_vrstica] + obrnjeni_podatki

def spremeni_format_datumov(podatki):
    """
    Sprejme list of lists, kjer je prvi stolpec datum v formatu MM/DD/YYYY.
    Pretvori datume od tretje vrstice naprej v format YYYY-MM-DD.
    Vrne posodobljen list of lists.
    """
    print("--------------------------------")
    print("Funkcija spremenu format datumov laufa!")
    for i in range(2, len(podatki)):  # Spremenimo datume od tretje vrstice naprej
        podatki[i][0] = datetime.strptime(podatki[i][0], "%m/%d/%Y").strftime("%Y-%m-%d")
    print("Uspesno smo pretvorili v pravi format! ✅")
    return podatki  # Vrne posodobljene podatke


# NAPISAT SE FUNKCIJO DA ZMECE VEN VSE VRSTICE KJER SO HOLIDAYSI IN NI TECAJA
def izbaci_ven_holidayse(podatki):
    """
    Odstrani vrstice, ki vsebujejo samo datum (tj. en element v seznamu) basicaly holidays izbaci ven
    To funkcijo dejmo klicat ko ze klicemo funkcijo za izbris nepotrebnih stolpev
    :param podatki: List of lists
    :return list of lists brez vrstic holidaysov
    """
    print("--------------------------------")
    print("Funkcija izbaci_ven_holidayse() laufa")
    i = 0
    while i < len(podatki):  # Iteriramo po seznamu
        if len(podatki[i]) > 1 and podatki[i][1] == "":  # Če drugi stolpec vsebuje "", izbrišemo vrstico
            del podatki[i]  # Odstranimo vrstico
        else:
            i += 1  # Premaknemo se na naslednji element samo, če ni bilo brisanja
    print("Uspesno smo izbacili ven holidayse! ✅")
    return podatki  # Vrnemo urejeni seznam

def izbrisi_nezelene_stoplce(podatki):
    """
    Funkcija ki izbrise zelene 'stolpce', oziroma bolj pravilno povedano; na katerih mestih elemente v listih
    :param podatki:
    :return:
    Primer:
    input:
    podatki = [
    [1, 2, 3, 4],
    [1, 2, 3, 4],
    ]
    odstranit hocemo 2 3
    output:
    podatki = [
    [1, 4],
    [1, 4],
    ]
    """
    print("--------------------------------")
    print("Funkcija, ki izbrise zelene stolpce laufa!")

    # tukaj dobimo v list stolpce ki jih hocemo izbrisat
    stolpec_za_zbrisat = []
    prvi_vnos = True
    while True:
        try:
            if prvi_vnos:
                izbrisati_kero = int(input("Katero vrstico hočeš izbrisati? "))
                prvi_vnos = False
            else:
                izbrisati_kero = int(input("Se katero? (Vnesi številko ali -1 za konec) "))

            if izbrisati_kero == -1:
                break
            stolpec_za_zbrisat.append(izbrisati_kero)
        except ValueError:
            print("Prosim, vnesi veljavno številko.")
    print(f"Izbrisati želiš te 'stolpce': {stolpec_za_zbrisat}")
    # tukaj jih pretvorimo v indekse, torej vsako - 1
    for i in range(0,len(stolpec_za_zbrisat)):
        stolpec_za_zbrisat[i] = stolpec_za_zbrisat[i] - 1
    # kle pa te stolpce oziroma elemente zbrisemo
    filtrirani_podatki = [
        [element for i, element in enumerate(vrstica) if i not in stolpec_za_zbrisat]
        for vrstica in podatki
    ]

    print(f"'Stolpci' {stolpec_za_zbrisat} uspesno zbrisani..✅")
    return filtrirani_podatki


def naredi_leverage_iz_osnovnih_podatkov(podatki):
    """
    Iz osnovnih cen ustvari serijo z vzvodom, dividendami in fundingom.

    PREJME SAMO PODATKE
        Seznam vrstic osnovnega CSV-ja (brez reinvestiranih dividend):
            [
                ["SP-500", "2024-2025"],
                ["Date", "Close"],
                ["2024-01-05", "100"],
                ["2024-01-08", "101"],
            ]
        Prva vrstica je samo opis; iz nje ne prepoznavamo indeksa.
        Datumi morajo naraščati, cene morajo biti pozitivne.
        Funkcija vhodnega seznama ne spreminja.

    DRUGI PODATKI
        Indeks izbereš z input(): 1 = S&P 500, 2 = Nasdaq 100,
        3 = Nasdaq Composite. Nato izbereš še vzvod (1, 2 ali 3).
        Letne stopnje sama prebere iz letne_stopnje.json v isti mapi.
        Funding je skupen, dividend yield pa izbere glede na indeks.
        Stopnje so že decimalke: 0.05 pomeni 5 %; ne delimo še enkrat s 100.
        Manjkajoče leto ali null sproži ValueError z navedbo leta in podatka.

    ALGORITEM
        1. Prvi datum: vrednost = prva osnovna cena, dnevni donos = 0.0.
        2. Za vsako naslednjo vrstico:
           a) donos_indeksa = (trenutna_cena - prejsnja_cena) / prejsnja_cena
           b) Preštej koledarske dni od prejšnjega do trenutnega datuma.
              Petek → ponedeljek pomeni 3 dni. Interval [prejšnji, trenutni)
              ob novem letu razdeli: 31. 12. → 2. 1. je en dan starega leta
              in en dan novega leta. Za vsak del vzemi stopnji njegovega leta.
           c) Prispevek vsakega dela = letna stopnja * dnevi / (365 ali 366).
              Seštej prispevke dividend in posebej prispevke fundinga.
           d) dnevni_donos = vzvod * (donos_indeksa + dividende_obdobja)
                             - (vzvod - 1) * funding_obdobja
           e) nova_vrednost = prejsnja_vrednost_serije * (1 + dnevni_donos)
           f) Shrani datum, novo vrednost in KONČNI dnevni donos.
        3. Vrni seznam za zapis v CSV; funkcija sama ne piše datoteke.

        Dividende so enakomerno razporejen letni približek in se reinvestirajo.
        Funding se obračuna na dodatno izpostavljenost: 0 pri 1x, 1 pri 2x,
        2 pri 3x. Model uporablja koledarsko osnovo 365/366 za obe stopnji.
        Donosov in vrednosti ne zaokrožujemo. Pri izgubi 100 % ali več se
        računanje ustavi, ker model ne more nadaljevati s pozitivno serijo.

    VRNE
        Nov seznam, ki ohrani prvo opisno vrstico in ji doda oznako vzvoda:
            [
                ["SP-500 2x", "2024-2025"],
                ["Date", "Close", "Daily Return"],
                ["2024-01-05", 100.0, 0.0],
                ...
            ]
        Tretji stolpec že vsebuje vzvod, dividende in funding.
        0.02 pomeni 2 % donosa. DCA ga lahko prebere s float(vrstica[2]),
        brez ponovnega izračuna sprememb iz cen in brez deljenja s 100.
    """


    """
    še management fee ki je nevem 0,8% na leto al kok in morda spread še. 
    """


    # Preverimo, da imamo opis, glavo in vsaj eno ceno.
    if len(podatki) < 3 or not podatki[0]:
        raise ValueError("Potrebujemo opis indeksa, glavo in vsaj eno vrstico s ceno.")

    # Iz CSV-vrstic pripravimo datume in številčne cene ter preverimo njihov vrstni red.
    vrstice = []
    for st_vrstice, vrstica in enumerate(podatki[2:], start=3):
        try:
            datum = datetime.strptime(str(vrstica[0]), "%Y-%m-%d").date()
            cena = float(vrstica[1])
        except (IndexError, TypeError, ValueError) as exc:
            raise ValueError(f"Neveljaven datum ali cena v vrstici {st_vrstice}.") from exc
        if not isfinite(cena) or cena <= 0:
            raise ValueError(f"Cena v vrstici {st_vrstice} mora biti pozitivna in končna.")
        if vrstice and datum <= vrstice[-1][0]:
            raise ValueError(f"Datumi morajo strogo naraščati; preveri vrstico {st_vrstice}.")
        vrstice.append((datum, cena))

    # Uporabnik izbere indeks; ta izbira določa dividend yield iz JSON-a.
    indeksi = {"1": "sp_500", "2": "nasdaq_100", "3": "nasdaq_comp"}
    izbira = input("Izberi indeks (1 = S&P 500, 2 = Nasdaq 100, 3 = Nasdaq Composite): ").strip()
    if izbira not in indeksi:
        raise ValueError("Indeks izberi s številko 1, 2 ali 3.")
    indeks = indeksi[izbira]

    # Uporabnik izbere, ali želi serijo 1x, 2x ali 3x.
    try:
        vzvod = int(input("Vnesi vzvod (1, 2 ali 3): "))
    except ValueError as exc:
        raise ValueError("Vzvod mora biti 1, 2 ali 3.") from exc
    if vzvod not in (1, 2, 3):
        raise ValueError("Vzvod mora biti 1, 2 ali 3.")

    # JSON preberemo enkrat, ne za vsak trgovalni dan posebej.
    with POT_LETNE_STOPNJE.open(encoding="utf-8") as f:
        leta = json.load(f)["leta"]

    # Posamezni letni stopnji preverimo in pripravimo samo enkrat na klic.
    stopnje_po_letih = {}

    def stopnji_za_leto(leto):
        if leto not in stopnje_po_letih:
            zapis = leta.get(str(leto))
            if not isinstance(zapis, dict):
                raise ValueError(f"V letne_stopnje.json manjka leto {leto}.")
            # Funding je skupen, dividende pa vzamemo samo za izbrani indeks.
            funding = zapis.get("funding")
            dividende = zapis.get("dividende", {}).get(indeks)
            if funding is None:
                raise ValueError(f"V letne_stopnje.json manjka funding za leto {leto}.")
            if dividende is None:
                raise ValueError(f"V letne_stopnje.json manjka dividend yield za {indeks}, leto {leto}.")
            try:
                funding, dividende = float(funding), float(dividende)
            except (TypeError, ValueError) as exc:
                raise ValueError(f"Letni stopnji za {leto} morata biti številki.") from exc
            if not isfinite(funding) or not isfinite(dividende) or dividende < 0:
                raise ValueError(f"Neveljavni letni stopnji za {indeks}, leto {leto}.")
            stopnje_po_letih[leto] = funding, dividende
        return stopnje_po_letih[leto]

    # Pripravimo nov rezultat; prvi datum ima začetno vrednost in donos 0.
    opis = list(podatki[0])
    opis[0] = f"{opis[0]} {vzvod}x"
    prejsnji_datum, prejsnja_cena = vrstice[0]
    vrednost = prejsnja_cena
    rezultat = [opis, ["Date", "Close", "Daily Return"],
                [prejsnji_datum.isoformat(), vrednost, 0.0]]

    # Od drugega trgovalnega dne naprej izračunamo spremembo osnovne cene.
    for datum, cena in vrstice[1:]:
        donos_indeksa = (cena - prejsnja_cena) / prejsnja_cena
        funding_obdobja = 0.0
        dividende_obdobja = 0.0
        zacetek_dela = prejsnji_datum
        # Obdobje čez novo leto razdelimo, da vsak del dobi stopnji svojega leta.
        while zacetek_dela < datum:
            leto = zacetek_dela.year
            konec_dela = datum if datum.year == leto else date(leto + 1, 1, 1)
            funding, dividende = stopnji_za_leto(leto)
            # Upoštevamo vse pretekle koledarske dni, tudi vikende, ter 365/366 dni v letu.
            delez_leta = (konec_dela - zacetek_dela).days / (366 if isleap(leto) else 365)
            funding_obdobja += funding * delez_leta
            dividende_obdobja += dividende * delez_leta
            zacetek_dela = konec_dela

        # Donos in dividende pomnožimo z vzvodom; funding odštejemo za izposojeni del.
        dnevni_donos = vzvod * (donos_indeksa + dividende_obdobja) - (vzvod - 1) * funding_obdobja
        if not isfinite(dnevni_donos) or dnevni_donos <= -1:
            raise ValueError(f"Serije ni mogoče nadaljevati: donos na {datum} je {dnevni_donos}.")
        # Končni donos uporabimo na prejšnji vrednosti pripravljene serije.
        vrednost *= 1 + dnevni_donos
        if not isfinite(vrednost) or vrednost <= 0:
            raise ValueError(f"Vrednost serije na {datum} ni več pozitivno končno število.")
        # Shranimo tudi končni dnevni donos, da ga DCA lahko neposredno prebere.
        rezultat.append([datum.isoformat(), vrednost, dnevni_donos])
        prejsnji_datum, prejsnja_cena = datum, cena

    # Vrnemo podatke; zapis v CSV opravi ustvari_nov_csv_file().
    return rezultat


# ta funkcija je zadnja ker pac ustvari podatke
def ustvari_nov_csv_file(podatki):
    """
    Funkcija ki sprejme list of list /array, pac podatki
    in ustvari iz nje novo csv datoteko, ki bo imenovana pod kot zelimo"
    @:param dvojni array/list
    """
    print("--------------------------------")
    print("Funkcija ki ustvari nov csv file laufa!")
    ime_novega = input("Kako naj bo ime novega csv file-a? ")
    # Izhodna mapa je vedno v backendu, ne glede na mapo zagona skripte.
    output_dir = Path(__file__).resolve().parents[1] / "podatki_ustvarjeni"
    output_dir.mkdir(parents=True, exist_ok=True)
    file_path = output_dir / f"{ime_novega}.csv"
    with open(file_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(podatki)
    print(f"Datoteka '{file_path}' je bila uspešno ustvarjena! ✅")
    print(f"Dodana je bila v directory: 'podatki_ustvarjeni'")
