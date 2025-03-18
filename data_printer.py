import pandas as pd


def print_original(podatki):
    """Izpiše podatke v originalni obliki."""
    print("Izpis v originalni obliki: 📝")

    print(podatki)
    print("\nKonec izpisa\n")

def print_vsak_v_svoji_vrstici(podatki):
    """Funkcija sprinta vsak line v svoji vrstici
    @:param dvojni array
    """
    print("Izpis vsak list v svoji vrstici: 📝")

    for i in range(0, len(podatki)):
        print(podatki[i])
        print("\nKonec izpisa\n")



def fancy_print(podatki):
    """Funkcija lepo izpiše podatke v obliki tabele, pri čemer prva vrstica nima separatorjev '|'.
    @:param podatki: seznam seznamov (list of lists)
    """
    print("Fancy izpis_: 📝")

    # Največje število stolpcev v katerikoli vrstici
    max_columns = max(len(vrstica) for vrstica in podatki)

    # Razširitev vseh vrstic na enako dolžino (dodamo prazne vrednosti, kjer manjkajo stolpci)
    normalized_podatki = [vrstica + [""] * (max_columns - len(vrstica)) for vrstica in podatki]

    # Izračun širine stolpcev glede na najdaljši element v posameznem stolpcu
    max_lengths = [max(len(str(row[i])) for row in normalized_podatki) for i in range(max_columns)]

    # Oblikovanje niza za izpis vrstice (z "|")
    format_str = " | ".join("{:^" + str(width) + "}" for width in max_lengths)

    # Prvo vrstico izpišemo brez separatorja "|"
    print(" ".join("{:^{width}}".format(item, width=max_lengths[i]) for i, item in enumerate(normalized_podatki[0])))

    # Nato izpišemo preostale vrstice v obliki tabele
    for vrstica in normalized_podatki[1:]:
        # Dodajanje "$" pred vrednosti v stolpcih, ki vsebujejo številčne vrednosti
        formatted_row = [
            f"${str(item)}" if str(item).replace('.', '', 1).isdigit() else str(item)
            for item in vrstica
        ]
        print(format_str.format(*map(str, formatted_row)))

    print("\nKonec izpisa\n")




