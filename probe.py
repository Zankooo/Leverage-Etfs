from data_printer import *

def obdrzi_le_datum_in_tecaj(podatki):
    """
    Funkcija ki izbrise zelene stolpce, oziroma bolj pravilno povedano, na katerih mestih elemente v listih
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
    print(f"Podatki brez teh stolpcev:{stolpec_za_zbrisat}")
    print(filtrirani_podatki)
    print("Uspesno izbrisano! ✅")
    return filtrirani_podatki




