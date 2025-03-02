# to je class v katerem bomo izvajali operacije nad csv file
import csv

# nalozimo podatke iz izbrane csv datoteke
def load_csv(filepath):
    """
    Prebere CSV datoteko in vrne podatke kot dvojni array (list of lists).
    """
    with open(filepath, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        array = [row for row in csv_reader]
        print("Csv file naložen!")
        return array

def obrni_csv(podatki):
    """
    Funkcija ki sprejme dvojni list/array, pac podatki
    in obrne vse skupaj; da seveda zacne obracat v tretji vrstici in obrne obicno vse skupaj reverse
    Pri tem prvi dve vrstici ki sta 'naslov' csv filea, obdrzi na istem mestu. Torej zacne kot receno v 3 vrstici obracat
    @:param dvojni array/list
    @return obrnjen array/list
    """
    # obrnemo podatke
    podatki.reverse()
    # prve dva sta 'naslova csv filea'
    # ampak ko smo zdej obrnili sta padla na zadnje in predzadnje mesto
    # damo ju na prve dva mesta in ju zbrisemo na koncu
    zadnji = podatki[len(podatki) - 1]
    predzadnji = podatki[len(podatki) - 2]
    podatki[0] = zadnji
    podatki[1] = predzadnji
    #zbrisemo oba na koncu
    podatki.pop()
    podatki.pop()
    print("Datoteka uspešno obrnjena!")
    return podatki

def ustvari_nov_csv_file(podatki):
    """
    Funkcija ki sprejme dvojni list/array, pac podatki
    in ustvari novo csv datoteko, ki bo imenovana pod kot zelimo"
    @:param dvojni array/list
    """
    ime_novega = input("Kako naj bo ime novega csv file-a? ")
    file_path = f"podatki/{ime_novega}.csv"
    with open(file_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(podatki)
    print(f"Datoteka '{file_path}' je bila uspešno ustvarjena!")

