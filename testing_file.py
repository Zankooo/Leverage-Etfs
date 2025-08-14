from datetime import datetime
from dateutil.relativedelta import relativedelta
from csv import reader
from csv import reader


def generiraj_intervale_15let_leto(podatki):
    """
    Funkcija ki nam generira intervale za vsakih 15 let
    Da nato lahko nardimo testing na teh datumih 
    @param podatki v dogovorjeni obliki
    @return list of list intervali datum od kdaj do kdaj
    """
    # Preskoči naslovne vrstice
    podatki = podatki[2:]

    # Pretvori v datetime in grupiraj po letih
    datumi = [datetime.strptime(row[0], "%Y-%m-%d") for row in podatki]
    prvi_v_letu = {}
    for d in datumi:
        if d.year not in prvi_v_letu:
            prvi_v_letu[d.year] = d

    # Naredi intervale
    intervali = []
    leta = sorted(prvi_v_letu.keys())
    for leto in leta:
        start_date = prvi_v_letu[leto]
        konec_date = start_date + relativedelta(years=15)

        # poišči prvi datum >= konec_date
        konec = next((d for d in datumi if d >= konec_date), None)
        if konec:
            intervali.append([start_date.strftime("%Y-%m-%d"), konec.strftime("%Y-%m-%d")])

    return intervali




def primerjaj_stolpec(file1, file2, stolpec=4):
    """
    Primerja določen stolpec med dvema CSV datotekama in prešteje,
    v koliko primerih ima prvi ali drugi višjo vrednost.
    
    :param file1: ime prve CSV datoteke
    :param file2: ime druge CSV datoteke
    :param stolpec: indeks stolpca za primerjavo (privzeto 4)
    :return: (stevec1, stevec2)
    """
    with open(file1, "r") as f1, open(file2, "r") as f2:
        podatki1 = list(reader(f1))
        podatki2 = list(reader(f2))

    stevec1 = 0
    stevec2 = 0
    print()
    print()
    print("Datum od kdaj do kdaj, Zacetna investicija, vse mesecne investicije, skupaj vse invesiticije, koliko smo v plusu oz minusu, koliko imamo vse skupaj")
    # preskočimo header (če ga je)
    for i in range(1, min(len(podatki1), len(podatki2))):
        try:
            vrednost1 = float(podatki1[i][stolpec])
            vrednost2 = float(podatki2[i][stolpec])
        except ValueError:
            continue  # preskočimo, če ni številka

        if vrednost1 > vrednost2:
            print(f"\033[95m{podatki1[i]}\033[0m", " -- ", f"\033[94m{podatki2[i]}\033[0m")


            stevec1 += 1
        elif vrednost2 > vrednost1:
            print(f"\033[94m{podatki2[i]}\033[0m -- \033[95m{podatki1[i]}\033[0m")
            stevec2 += 1

    print("---------------")
    print(f"Tole je direktna primerjava; {file1} in {file2}. Na levi so tisti ki so bili boljsi v tistem obdobju, na desni pa uni ki so bili slabsi")
    print(f"\033[95m{file1} --> je bil boljsi  v {stevec1} primerih\033[0m")
    print(f"\033[94m{file2} --> je bil boljsi v {stevec2} primerih\033[0m")

    print()
    procent_stevec_1 = round((stevec1 / (stevec1 + stevec2)) * 100, 2)
    procent_stevec_2 = round((stevec2 / (stevec1 + stevec2)) * 100, 2)



    print(f"\033[92mV {procent_stevec_1}% je bil boljsi {file1}, v {procent_stevec_2}% pa je bil boljsi {file2}!\033[0m")


    return stevec1, stevec2
