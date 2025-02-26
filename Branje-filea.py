import csv
import pandas as pd
podatki = []


"""
FUNKCIJA; Prebere .csv file in ga shrani v variable "podatki"
To je v bistvu dvojni array
Ta program je narejen za nasdaq.csv, ker so prve tri vrstice ne upostevajo v loopu pol, pac sintaksa je od nasdaq.csv
"""
with open('podatki/nasdaq.csv', 'r', encoding='utf-8') as file:
    csv_reader = csv.reader(file)
    podatki = [row for row in csv_reader]  # Shranjevanje vsake vrstice v seznam


"""
FUNKCIJA; Navaden print
Naprinta nam dvojni array kot je v originalu
"""
def navaden_print():
    print(podatki)

"""
FUNKCIJA; Print v svoji vrstici
dvojni array je to, in on vsak array v njemu naprinta v svoji vrstici
"""
def print_vsak_v_svoji_vrstici():
    for line in podatki:
        print(line)

"""
FUNKCIJA; Print v svoji vrstici
dvojni array je to, in on vsak array v njemu naprinta v svoji vrstici
"""
def print_vsak_v_svoji_vrsticii(podatki):
    for line in podatki:
        print(line)


def calculate_daily_changes(podatki):
    """
    Sprejme dvojni array s podatki o NASDAQ indeksu in vrne array z dodatnim stolpcem
    'Daily Change (%)', ki prikazuje dnevno spremembo v odstotkih.

    - Preverja, ali so podatki veljavni float-i.
    - Izračuna dnevno spremembo.
    - Hkrati izpiše vsako vrstico in opozori na neveljavne vrednosti.
    - Dodan znak '%' na koncu spremembe.
    - Zaokroženo na dve decimalki.
    - Če je sprememba pozitivna, doda znak '+'.
    """

    # Funkcija za preverjanje, ali je vrednost veljaven float
    def is_float(value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    # Dodamo nov stolpec v glavo
    result = [podatki[0]]
    print(result[0])  # Izpišemo glavo

    # Prvo vrstico dodamo brez spremembe
    result.append(podatki[1] + ['Daily Change (%)'])
    print(result[1])  # Izpišemo prvo vrstico

    # Izračunamo spremembo za vsak naslednji dan
    for i in range(2, len(podatki)):
        # Preverimo, ali sta obe vrednosti veljavna float-a
        if is_float(podatki[i - 1][1]) and is_float(podatki[i][1]):
            previous_value = float(podatki[i - 1][1])
            current_value = float(podatki[i][1])
            daily_change = ((current_value - previous_value) / previous_value) * 100

            # Dodamo znak '+' za pozitivne spremembe
            change_str = f"{'+' if daily_change > 0 else ''}{round(daily_change, 2)}%"

            result.append(podatki[i] + [change_str])
            print(result[-1])  # Izpišemo trenutno vrstico
        else:
            result.append(podatki[i] + ['Invalid'])
            print(f"⚠️  Warning: Invalid data at line {i + 1}: {podatki[i]}")

    return result


calculate_daily_changes(podatki)