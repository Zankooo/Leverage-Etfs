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

    # preskočimo header (če ga je)
    for i in range(1, min(len(podatki1), len(podatki2))):
        try:
            vrednost1 = float(podatki1[i][stolpec])
            vrednost2 = float(podatki2[i][stolpec])
        except ValueError:
            continue  # preskočimo, če ni številka

        if vrednost1 > vrednost2:
            stevec1 += 1
        elif vrednost2 > vrednost1:
            stevec2 += 1

    print(f"{file1} ima večjo vrednost v {stevec1} primerih")
    print(f"{file2} ima večjo vrednost v {stevec2} primerih")

    return stevec1, stevec2
