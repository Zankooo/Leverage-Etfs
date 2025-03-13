import re

import pandas as pd

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


def calculate_annual_returns(podatki):
    """
    Ne vem kako ta funkcija dela ampak dela!
    Funkcija ki sprejme podatke, list of lists
    In izracuna donos za vsako leto.
    :param list of lists podatki indeksa
    :return: list of lists donosov za vsako leto
    """
    # Začnemo obdelavo podatkov od tretje vrstice
    podatki = podatki[2:]

    # Če je vhodni podatki list of lists, ga pretvorimo v DataFrame
    if isinstance(podatki, list):
        podatki = pd.DataFrame(podatki, columns=["Date", "Close"])

    # Preverimo, ali je podatki DataFrame
    if not isinstance(podatki, pd.DataFrame):
        raise TypeError(f"Vhodni podatki morajo biti pandas DataFrame, prejet: {type(podatki)}")

    # Pretvorimo stolpec 'Date' v datetime format
    podatki["Date"] = pd.to_datetime(podatki["Date"], errors='coerce')

    # Odstranimo morebitne neveljavne vrstice
    podatki = podatki.dropna()

    # Pretvorimo 'Close' v numerični format
    podatki["Close"] = pd.to_numeric(podatki["Close"], errors='coerce')

    # Izluščimo leto
    podatki["Year"] = podatki["Date"].dt.year

    # Priprava praznega seznama za rezultate
    annual_returns = [["Leto", "Prvi-dan", "Zadnji-dan", "Donos(%)"]]
    unique_years = sorted(podatki["Year"].unique())

    for year in unique_years:
        yearly_data = podatki[podatki["Year"] == year]
        first_price = float(yearly_data.iloc[0]["Close"])
        last_price = float(yearly_data.iloc[-1]["Close"])
        return_pct = float(((last_price / first_price) - 1) * 100)
        annual_returns.append([int(year), first_price, last_price, round(return_pct,2)])
    return annual_returns






