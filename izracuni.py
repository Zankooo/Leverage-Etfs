from datetime import datetime
from datetime import *
import re

from csv_operacije import *


def calculate_daily_changes(podatki):
    """
    Sprejme dvojni array s podatki o indeksu in vrne array z dodatnim stolpcem; "daily change"
    Prva vrstica v csv file je ime indeksa in od kdaj do kdaj je
    Druga vrstica v csv file so poimenovanje podatkov
    Tretja so pa ze podatki, prvi(na indeksu 0) je datum drugi(na indeksu 1) je pa vrednost
    """
    # vzamemo datum iz tretje vrstice in ce ni v iso modelu klicemo funkcijo in spremenimo v iso model
    date_string = podatki[2][0]
    if not re.match(r"\d{4}-\d{2}-\d{2}", date_string):
        podatki = convert_dates(podatki)

    # prvo datum spremenimo datum in pol podatke da so od najstarejsega k najlmaljsemu
    #vzamemo iz tretje vrstice in zadnje in ce je iz tretje vecji datum klicemo funkcijo
    datum1_string = podatki[2][0]
    datum2_string = podatki[len(podatki)-1][0]
    date1 = datetime.strptime(datum1_string, "%Y-%m-%d")
    date2 = datetime.strptime(datum2_string, "%Y-%m-%d")
    if date1 > date2:
        podatki = obrni_csv(podatki)


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
        elif is_float(current_value):
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

def calculate_return(podatki):
    """
    Sprejme seznam seznamov [[datum, tečaj]] in omogoča začetno investicijo + mesečne vložke.
    Izračuna končno vrednost investicije glede na spremembo S&P 500 indeksa.
    :param podatki: Seznam seznamov [[datum, vrednost SP500]]
    :return: int končna vrednost investicije
    """
    podatki_daily_changes = calculate_daily_changes(podatki)

    initial_investment = int(input("Vpisi začetno investicijo: "))
    monthly_investment = int(input("Vpisi mesečni vložek: "))  # Nov vnos za mesečno investicijo
    investment = initial_investment
    mesecni_vlozki_vsota = 0
    print("Izberi začetni dan investiranja (indeks vrstice, npr. 2)")
    zacetek = int(input("Začetek (katera vrstica): "))
    konec = int(input("Konec (katera vrstica): "))
    # Nastavimo začetni mesec za mesečne vložke
    current_month = datetime.strptime(podatki[zacetek][0], "%Y-%m-%d").month
    for i in range(zacetek, konec + 1):
        if podatki_daily_changes[i][2] == "Holidays":
            continue  # Preskoči dneve, ko borza ne deluje

        daily_change = podatki_daily_changes[i][2].replace("%", "")  # Odstrani "%"
        daily_change_cifra = round(float(daily_change), 2) / 100  # Pretvori v decimalno vrednost
        # Pridobimo mesec trenutnega datuma
        date = datetime.strptime(podatki[i][0], "%Y-%m-%d")
        # Če je nov mesec, dodamo mesečni vložek
        if date.month != current_month:
            investment = investment + monthly_investment
            mesecni_vlozki_vsota = mesecni_vlozki_vsota + monthly_investment
            current_month = date.month  # Posodobimo trenutni mesec
        # Izračun vrednosti portfelja
        investment = investment * (1 + daily_change_cifra)
        print(f"Vrednost pri vrstici {i} oz. datumu {podatki[i][0]}: {investment:.2f} EUR ({daily_change}%)")

    print("-----------")
    print(f"Začetna investicija je bila: {initial_investment} EUR in vseh mesečnih investicij: {mesecni_vlozki_vsota}EUR, skupaj: {initial_investment + mesecni_vlozki_vsota}EUR")

    print(f"Od {podatki[zacetek][0]} do {podatki[konec][0]} imamo vse skupaj z donosom/izgubo: {investment:.2f} EUR")

    zasluzili = round(investment - initial_investment - mesecni_vlozki_vsota, 2)

    print(f"Torej zaslužili / izgubili smo: {zasluzili}EUR")

    return round(investment, 2)

#----------- POMOZNE FUNKCIJE KI JIH KLIČEMO ZNOTRAJ DRUGIH FUNKCIJ-----------

def is_float(value):
    """Notranja funkcija; Preveri, ali je podana vrednost veljaven float."""
    try:
        float(value)
        return True
    except ValueError:
        return False

