from datetime import datetime

def calculate_daily_changes(podatki):
    """
    Sprejme dvojni array s podatki o NASDAQ indeksu in vrne array z dodatnim stolpcem; "daily change"
    Prva vrstica je ime indeksa in od kdaj do kdaj
    Druga vrstica so poimenovanje podatkov
    Tretja so pa ze podatki, prvi je datum drugi pa vrednost
    """
    def is_float(value):
        """Notranja funkcija; Preveri, ali je podana vrednost veljaven float."""
        try:
            float(value)
            return True
        except ValueError:
            return False
    # Dodamo stolpec 'Daily Change (%)' prvo vrstico
    result = [podatki[0]]
    # Inicializacija prve vrstice brez spremembe
    result.append(podatki[1] + ["Daily Change (%)"])  # Prvi dan ni spremembe
    # Drugi dan nastavim na '0%', ker ni spremembe
    result.append(podatki[2] + ['0%'])
    # Izračun spremembe za vsak naslednji dan
    for i in range(3, len(podatki)):
        current_value = podatki[i][1]
        previous_value = podatki[i - 1][1]  # Ena vrstica nazaj

        # Če je trenutna vrednost prazna, napišemo "holidays"
        if current_value == '':
            result.append(podatki[i] + ['Holidays'])
            # nadaljujemo loop - continue, ker ni nic za racunat pac
            continue

        # Če je trenutna vrednost veljaven float
        if is_float(current_value):
            current_value = float(current_value)
            #ugotovit moramo prejšno vrednost, oz ker dan nazadnje je pa bil trgovalni dan
            # v skoraj večini primerov je bil prejšni dan trgovalni-ima tecaj, razen ko je bil 11/9
            # zato sem kodo tako napisal
            if previous_value == '':
                #loopamo nazaj da ugotovimo ker dan je pa tazadnji ki ima tecaj
                vrstica = i - 1
                while vrstica >= 0:
                    #tisti ki ni prazen torej
                    if podatki[vrstica][1]!= '':
                        previous_value = float(podatki[vrstica][1])
                        break
                    else:
                        vrstica = vrstica - 1

            # tukaj pa zracunamo torej spremembo in jo zapisemo v vrstico v kateri smo trenutno
            previous_value = float(previous_value)
            daily_change = ((current_value - previous_value) / previous_value) * 100
            change_str = f"{'+' if daily_change > 0 else ''}{round(daily_change, 2)}%"
            result.append(podatki[i] + [change_str])

    return result

def convert_dates(podatki):
    """
    Sprejme list of lists, kjer je prvi stolpec datum v formatu MM/DD/YYYY.
    Pretvori datume od tretje vrstice naprej v format YYYY-MM-DD.
    Vrne posodobljen seznam.
    """
    for i in range(2, len(podatki)):  # Spremenimo datume od tretje vrstice naprej
        podatki[i][0] = datetime.strptime(podatki[i][0], "%m/%d/%Y").strftime("%Y-%m-%d")
    return podatki  # Vrne posodobljene podatke


def calculate_return(data, initial_investment=1000):
    """
    Sprejme seznam seznamov [[datum, tecaj]] in začetno investicijo.
    Izračuna končno vrednost investicije glede na spremembo SP500 indeksa.

    :param data: Seznam seznamov [[datum, vrednost SP500]]
    :param initial_investment: Začetni kapital (privzeto 1000 enot)
    :return: Končna vrednost investicije
    """

    # Vrednost SP500 na prvi dan
    first_price = float(data[2][1])

    # Vrednost SP500 na zadnji dan
    last_price = float(data[-1][1])

    # Donos na osnovi rasti indeksa
    final_value = initial_investment * (last_price / first_price)
    if final_value > 1000:
        final_value_formatirano = f"{final_value:,.2f} eur"
        print(final_value_formatirano)
    print(f"{round(final_value,2)} eur")

    return round(final_value,2)  # Zaokrožimo na 2 decimalni mesti