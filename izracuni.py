import re
from csv_operacije import *


def calculate_daily_changes(podatki):
    """
    Sprejme dvojni array s podatki o indeksu in vrne array z dodatnim stolpcem; "daily change"
    Prva vrstica v csv file je ime indeksa in od kdaj do kdaj je
    Druga vrstica v csv file so poimenovanje podatkov
    Tretja so pa ze podatki, prvi(na indeksu 0) je datum drugi(na indeksu 1) je pa vrednost
    Ta funkcija naredi to:
    - moras ji dati file

    """
    # Dodamo stolpec 'Daily Change (%)' prvo vrstico
    result = [podatki[0]]
    # Inicializacija prve vrstice brez spremembe
    result.append(podatki[1] + ["Daily Change (%)"])  # Prvi dan ni spremembe
    # Drugi dan nastavim na '0%', ker pac je prvi dan
    result.append(podatki[2] + ['0%'])
    # Izračun spremembe za vsak naslednji dan
    for i in range(3, len(podatki)):
        trenutni_tecaj = float(podatki[i][1])
        dan_prej_tecaj = float(podatki[i - 1][1])
        daily_change = ((trenutni_tecaj - dan_prej_tecaj) / dan_prej_tecaj) * 100
        sprememba_procentualno = f"{'+' if daily_change > 0 else ''}{round(daily_change, 2)}%"
        result.append(podatki[i] + [sprememba_procentualno])
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
        daily_change = podatki_daily_changes[i][2].replace("%", "")  # Odstrani "%"
        daily_change_cifra = round(float(daily_change), 2) / 100  # Pretvori v decimalno vrednost
        # Pridobimo mesec trenutnega datuma
        date = datetime.strptime(podatki[i][0], "%Y-%m-%d")
        stevec_mesecev = 1
        # Če je nov mesec, dodamo mesečni vložek
        if date.month != current_month:
            investment = investment + monthly_investment
            print(f"Mesecna investicija investirana: {monthly_investment}eur")
            mesecni_vlozki_vsota = mesecni_vlozki_vsota + monthly_investment
            current_month = date.month
            stevec_mesecev = stevec_mesecev + 1# Posodobimo trenutni mesec
        # Izračun vrednosti portfelja
        investment = investment * (1 + daily_change_cifra)
        print(f"Vrednost pri vrstici {i} oz. datumu {podatki[i][0]}: {investment:.2f} EUR ({daily_change}%)")
    print("-----------")
    print(f"Začetna investicija je bila: {initial_investment}EUR,")
    print(f"Vseh mesečnih investicij je bilo: {mesecni_vlozki_vsota}EUR,")
    print(f"Celotne investicije skupaj je torej bilo: {initial_investment + mesecni_vlozki_vsota}EUR")
    print("-----------")
    print(f"Od {podatki[zacetek][0]} do {podatki[konec][0]} imamo vse skupaj z donosom/izgubo: {investment:.2f} EUR")
    zasluzili = round(investment - initial_investment - mesecni_vlozki_vsota, 2)
    print(f"Torej zaslužili / izgubili smo: {zasluzili}EUR")
    procentualno_zasluzek = (zasluzili / (initial_investment + mesecni_vlozki_vsota)) * 100
    procentualno_zasluzek = round(procentualno_zasluzek,2)
    print(f"Procentualno: {procentualno_zasluzek}%")
    # procentualno je izracunano ->  (donos/cela investicija)*100

    return round(investment, 2)

#----------- POMOZNE FUNKCIJE KI JIH KLIČEMO ZNOTRAJ DRUGIH FUNKCIJ-----------

def is_float(value):
    """Notranja funkcija; Preveri, ali je podana vrednost veljaven float."""
    try:
        float(value)
        return True
    except ValueError:
        return False

