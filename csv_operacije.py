# to je class v katerem bomo izvajali operacije nad csv file
import csv
from datetime import datetime

#TO FUNKCIJO VEDNO KLICEMO KER PAC NALOZI PODATKE
def load_csv(filepath):
    """
    Prebere CSV datoteko in vrne podatke kot dvojni array (list of lists).
    """
    with open(filepath, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        array = [row for row in csv_reader]
        print("Csv file naložen!")
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
# AMPAK CE JE BIL HOLIDAYS TEGA DATUMA SPLOH NE SME BIT NOTRI, TOREJ MOREMO FA FUKNT VEN

# TOREJ:
#TE FUNKCIJE PA KLIČEMO LE ČE PODATKI NISO V NAŠEM DOGOVORJENEM FORMATU,
# IN ZADNJO FUNKCIJO KLICEMO DA NAM USTVARI FILE IZ OBDELANEGA CSVJA KI JE PRIPRAVLJEN ZA ANALIZE

def obrni_csv(podatki):
    """
    Funkcija, ki sprejme dvojni seznam/array (CSV podatke),
    in obrne vrstni red vseh vrstic od tretje vrstice naprej.
    Prvi dve vrstici ('naslovna' dela CSV-ja) ostaneta nespremenjeni.
    @param podatki: seznam seznamov (CSV podatki)
    @return: obrnjen seznam seznamov
    """
    prva_vrstica = podatki[0]
    druga_vrstica = podatki[1]
    # Obrnemo vrstni red od tretje vrstice naprej
    obrnjeni_podatki = list(reversed(podatki[2:]))
    print("Podatke smo obrnili, saj datumi niso bili od najstarejšega k najmlajšemu, sedaj pa so.")
    return [prva_vrstica, druga_vrstica] + obrnjeni_podatki

def spremeni_format_datumov(podatki):
    """
    Sprejme list of lists, kjer je prvi stolpec datum v formatu MM/DD/YYYY.
    Pretvori datume od tretje vrstice naprej v format YYYY-MM-DD.
    Vrne posodobljen list of lists.
    """

    for i in range(2, len(podatki)):  # Spremenimo datume od tretje vrstice naprej
        podatki[i][0] = datetime.strptime(podatki[i][0], "%m/%d/%Y").strftime("%Y-%m-%d")
    print("Datumi niso bili v iso formatu sedaj pa smo jih pretvorili.")
    return podatki  # Vrne posodobljene podatke


# NAPISAT SE FUNKCIJO DA ZMECE VEN VSE VRSTICE KJER SO HOLIDAYSI IN NI TECAJA
def izbaci_ven_holidayse(podatki):
    """
    Odstrani vrstice, ki vsebujejo samo datum (tj. en element v seznamu) basicaly holidays izbaci ven
    :param podatki: List of lists
    :return list of lists brez vrstic holidaysov
    """
    i = 0
    while i < len(podatki):  # Iteriramo po seznamu
        if len(podatki[i]) > 1 and podatki[i][1] == "":  # Če drugi stolpec vsebuje "", izbrišemo vrstico
            del podatki[i]  # Odstranimo vrstico
        else:
            i += 1  # Premaknemo se na naslednji element samo, če ni bilo brisanja
    return podatki  # Vrnemo urejeni seznam

# ta funkcija je zadnja ker pac ustvari podatke
def ustvari_nov_csv_file(podatki):
    """
    Funkcija ki sprejme dvojni list/array, pac podatki
    in ustvari iz nje novo csv datoteko, ki bo imenovana pod kot zelimo"
    @:param dvojni array/list
    """
    ime_novega = input("Kako naj bo ime novega csv file-a? ")
    file_path = f"podatki_obdelani/{ime_novega}.csv"
    with open(file_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(podatki)
    print(f"Datoteka '{file_path}' je bila uspešno ustvarjena!")

