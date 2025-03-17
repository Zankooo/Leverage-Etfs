podatki = [
    ['SP500', '1927-2020'],
    ['Date', 'Close-Price'],
    ['1927-12-30', '17.660000'],
    ['1928-01-03', '17.760000'],
    ['1928-01-04', '17.719999'],
    ['1928-01-05', '17.549999'],
    ['1928-01-06', '17.660000'],
]


datum_zacetka = input("Vpisi datum zacetka (format: yyy-mm-dd): ")

index_zacetka = None
index_konca = None
od_tukaj_naprej = None
# Inicializiraj to spremenljivko izven zanke
for i in range(0, len(podatki)):
    if podatki[i][0] == datum_zacetka:
        print(f"Nasli smo datum, nahaja se na indeksu {i}")
        index_zacetka = i # Nastavi index zacetka
        od_tukaj_naprej = i  # Nastavi od-tukaj-naprej
        break  # Lahko prekinemo zanko, ker smo našli začetek

if od_tukaj_naprej == None:
    print("Datum zacetka ni najden, oz. je napravilno vpisan!")

datum_konca = input("Vpisi datum konca (format: yyy-mm-dd): ")

if od_tukaj_naprej is not None:  # Preverimo, ali smo našli datum začetka
    for i in range(od_tukaj_naprej, len(podatki)):
        if podatki[i][0] == datum_konca:
            index_konca = i
            print(f"Nasli smo datum, nahaja se na indeksu {i}")
            break  # Prekinemo, ko najdemo datum konca

if index_konca == None:
    print("Datum konca ni najden, oz. je napravilno vpisan!")
