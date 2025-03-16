# to je class v katerem bomo izvajali operacije od csv file
import csv
from datetime import datetime

#TO FUNKCIJO VEDNO KLICEMO KER PAC NALOZI PODATKE
def load_csv(filepath):
    """
    Prebere CSV datoteko in vrne podatke kot dvojni array (list of lists).
    """
    print("--------------------------------")
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
    :param podatki: List of lists
    :return list of lists brez vrstic holidaysov
    """
    print("--------------------------------")
    print("Funkcija ki izbaci ven holidayse laufa")
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


# ta funkcija je zadnja ker pac ustvari podatke
def ustvari_nov_csv_file(podatki):
    """
    Funkcija ki sprejme dvojni list/array, pac podatki
    in ustvari iz nje novo csv datoteko, ki bo imenovana pod kot zelimo"
    @:param dvojni array/list
    """
    print("--------------------------------")
    print("Funkcija ki ustvari nov csv file laufa!")
    ime_novega = input("Kako naj bo ime novega csv file-a? ")
    file_path = f"podatki_obdelani/{ime_novega}.csv"
    with open(file_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(podatki)
    print(f"Datoteka '{file_path}' je bila uspešno ustvarjena! ✅")
    print(f"Dodana je bila v directory: 'podatki_obdelani'")

