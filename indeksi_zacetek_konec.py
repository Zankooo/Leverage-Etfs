def najdi_indekse_zacetka_in_konca(podatki):
    """Funkcija ki sprejema kot user input datum zacetka in konca in najde na katerem indeksu oz vrstici se nahajata
    :param podatki: list of lists, dogovorjen format
    :return list z dvema elementoma: index zacetka in index konca. Glede na vpisan datum
    """
    datum_zacetka = input("Vpisi datum zacetka (format: yyyy-mm-dd): ")
    index_zacetka = None
    index_konca = None
    od_tukaj_naprej = None

    # Najdemo za začetni datum indeks
    for i in range(0, len(podatki)):
        if podatki[i][0] == datum_zacetka:
            print(f"Nasli smo datum zacetka, nahaja se na indeksu {i} oz. vrstici {i+1}")
            index_zacetka = i  # Nastavi index začetka
            od_tukaj_naprej = i  # Nastavi od-tukaj-naprej
            break  # Lahko prekinemo zanko, ker smo našli začetek

    if od_tukaj_naprej is None:
        print("Datum začetka ni najden, oz. je napačno vpisan!")
        return [-1, -1]

    datum_konca = input("Vpisi datum konca (format: yyyy-mm-dd): ")

    # Najdemo za končni datum indeks
    for i in range(od_tukaj_naprej, len(podatki)):
        if podatki[i][0] == datum_konca:
            index_konca = i
            print(f"Nasli smo datum konca, nahaja se na indeksu {i} oz. vrstici {i+1}")
            break  # Prekinemo, ko najdemo datum konca

    if index_konca is None:
        print("Datum konca ni najden, oz. je napačno vpisan!")
        return [-1, -1]

    return [index_zacetka, index_konca]