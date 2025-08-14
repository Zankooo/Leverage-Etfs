import re

import pandas as pd

from obcasno_pogosti_fajli.csv_operacije import *
# karkoli tukaj delamo oz kero kol funkcijo klicemo moramo imeti
# dogovorjen format podatkov oz csv.ja

def izracun_dnevnih_sprememb(podatki):
    """
    Funkcija, ki izracuna dnevne spremembe indeksa
    :param list of lists (dogovorjen format)
    :return list of lists tak kot je bil podan in mu doda dnevne spremembe "daily changes"
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
        sprememba_procentualno = f"{'+' if daily_change > 0 else ''}{daily_change}%"
        result.append(podatki[i] + [sprememba_procentualno])
    return result

def izracun_dca_metoda(podatki):
    """
    Funkcija izracuna koliko imamo kesa po izbranem obdobju
    Torej: izberemo začetno investicijo + mesečne vložke(prvega v mesecu oz na zacetku meseca, se obracunajo).
    Izračuna končno vrednost investicije glede na vsakodnevno spremembo indeksa.
    :param podatki: List of lists dogovorjen format
    :return: int končna vrednost investicije
    """
    #kle je fora ker tist dan ko mi kupimo se uposta tudi koliko je ta dan zrastlo
    # ampak tega verjetno ne bi smel upostevat, idk
   # pogledat tudi za mesecne investicije kdaj dejansko se kupjo
    podatki_daily_changes = izracun_dnevnih_sprememb(podatki)

    initial_investment = int(input("Vpisi začetno investicijo: "))
    monthly_investment = int(input("Vpisi mesečni vložek: "))  # Nov vnos za mesečno investicijo
    investment = initial_investment
    mesecni_vlozki_vsota = 0

# PROBLEM JE KER CE PRIMERJAS Z GOOGLE GRAFOM NISO CIST CIST ISTI DONOSI IN ZDEJ GRUNTAM KJE JE PROBLEM
# zdej je okej sem testiral ampak mi ni jasno kako je lahko okej ce v for loopu ze prvi dan vzamemo, idk ampak je zlo prou
    datum_zacetka = input("Začetek investiranja datum: ")
    datum_konca = input("Konec investiranja datum: ")

    # Nastavimo začetni mesec za mesečne vložke
    current_month = datetime.strptime(datum_zacetka, "%Y-%m-%d").month

    # to rabimo da lahko pozenemo loop cez vse dneve
    vrstica_zacetka = (next(i for i, row in enumerate(podatki) if row[0] == datum_zacetka))
    vrstica_konca = (next(i for i, row in enumerate(podatki) if row[0] == datum_konca))

    # od kere do kere vrstice gre? -> pac mi smatramo da kupimo ob close ob zaprtju, po tisti ceni
    for i in range(vrstica_zacetka, vrstica_konca + 1):
        # odstranimo %, da pac lahko delamo z podatkom ane
        daily_change = podatki_daily_changes[i][2].replace("%", "")
        # Pretvori v decimalno vrednost
        daily_change_cifra = round(float(daily_change), 2) / 100

        # Pridobimo mesec trenutnega datuma, da lahko upalimo mesecno investicijo ce je nov mesec
        date = datetime.strptime(podatki[i][0], "%Y-%m-%d")

        # Če je nov mesec, dodamo mesečni vložek
        if date.month != current_month:
            investment = investment + monthly_investment
            print(f"Mesecna investicija investirana: {monthly_investment}eur")
            mesecni_vlozki_vsota = mesecni_vlozki_vsota + monthly_investment
            current_month = date.month

        # Izračun vrednosti portfelja
        investment = investment * (1 + daily_change_cifra)
        print(f"Vrednost pri vrstici {i}. oz. datumu {podatki[i][0]}: {investment:.2f} EUR ({daily_change}%)")

    print("-----------")
    print(f"Od {datum_zacetka} do {datum_konca}:")
    print(f"Začetna investicija je bila: {initial_investment}EUR 💵,")
    print(f"Vseh mesečnih investicij je bilo skupaj: {mesecni_vlozki_vsota}EUR 💸,")
    print("-----------")
    print(f"Total contribution(zacentna + mesecne): {initial_investment + mesecni_vlozki_vsota}EUR 🔢,")
    zasluzili = round(investment - initial_investment - mesecni_vlozki_vsota, 2)
    print(f"Torej zaslužili / izgubili smo: {zasluzili}EUR")
    print(f"Imamo vse skupaj: {investment:.2f} EUR 💰✈️🌍")

    # to prikazemo samo ce imamo brez mescecnih. Edini namen je dokaz/prikazati, da pac ce potegnemo na google grafu da pac res dela funkcija
    if mesecni_vlozki_vsota == 0:
        procentualno_zasluzek = (zasluzili / initial_investment) * 100
        procentualno_zasluzek = round(procentualno_zasluzek, 2)
        print(f"Procentualno: {procentualno_zasluzek}%. Lahko preveris na google stock grafu da je zelo zelo podobno")
    # procentualno je izracunano ->  (donos/cela investicija)*100
    # tukaj ce so mesecne investicije je malo drugace in treba nekako fiksat
    return round(investment, 2)


def izracun_letnih_donosov(podatki):
    """
    Ne vem kako ta funkcija dela ampak dela!
    Funkcija ki sprejme podatke, list of lists
    In izracuna donos za Vsako leto.
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
        return_str = f"{round(return_pct, 2):+.2f}%"
        annual_returns.append([int(year), round(first_price, 2), round(last_price, 2), return_str])


    return annual_returns

#----------- POMOZNE FUNKCIJE KI JIH KLIČEMO ZNOTRAJ DRUGIH FUNKCIJ-----------

def is_float(value):
    """Notranja funkcija; Preveri, ali je podana vrednost veljaven float."""
    try:
        float(value)
        return True
    except ValueError:
        return False



# -------------------------- spremenjena funkcija dca za testing
# --------------------------------------------

def metoda_dca_za_testing_prilagojena(podatki, initial_investment, monthly_investment, datum_zacetka, datum_konca):
    """
    Funkcija ista kot una zgoraj le da prejmemo kot parametri 
    in ne izpisujemo vsega
    prilagojena je da delamo testing na njen
    testing pa delamo tako da ji damo razlicne datum zacetka in datum konca...
    te datum zacetka pa konca pa dobim iz funkcije "generiraj_intervale_15let_leto"
    """
    #kle je fora ker tist dan ko mi kupimo se uposta tudi koliko je ta dan zrastlo
    # ampak tega verjetno ne bi smel upostevat, idk
   # pogledat tudi za mesecne investicije kdaj dejansko se kupjo

    podatki_daily_changes = izracun_dnevnih_sprememb(podatki)

     # Nov vnos za mesečno investicijo
    investment = initial_investment
    mesecni_vlozki_vsota = 0

# PROBLEM JE KER CE PRIMERJAS Z GOOGLE GRAFOM NISO CIST CIST ISTI DONOSI IN ZDEJ GRUNTAM KJE JE PROBLEM
# zdej je okej sem testiral ampak mi ni jasno kako je lahko okej ce v for loopu ze prvi dan vzamemo, idk ampak je zlo prou
    

    # Nastavimo začetni mesec za mesečne vložke
    current_month = datetime.strptime(datum_zacetka, "%Y-%m-%d").month

    # to rabimo da lahko pozenemo loop cez vse dneve
    vrstica_zacetka = (next(i for i, row in enumerate(podatki) if row[0] == datum_zacetka))
    vrstica_konca = (next(i for i, row in enumerate(podatki) if row[0] == datum_konca))

    # od kere do kere vrstice gre? -> pac mi smatramo da kupimo ob close ob zaprtju, po tisti ceni
    for i in range(vrstica_zacetka, vrstica_konca + 1):
        # odstranimo %, da pac lahko delamo z podatkom ane
        daily_change = podatki_daily_changes[i][2].replace("%", "")
        # Pretvori v decimalno vrednost
        daily_change_cifra = round(float(daily_change), 2) / 100

        # Pridobimo mesec trenutnega datuma, da lahko upalimo mesecno investicijo ce je nov mesec
        date = datetime.strptime(podatki[i][0], "%Y-%m-%d")

        # Če je nov mesec, dodamo mesečni vložek
        if date.month != current_month:
            investment = investment + monthly_investment
            mesecni_vlozki_vsota = mesecni_vlozki_vsota + monthly_investment
            current_month = date.month

        # Izračun vrednosti portfelja
        investment = investment * (1 + daily_change_cifra)
        

    
    zasluzili = round(investment - initial_investment - mesecni_vlozki_vsota, 2)
   

    
    # da bi v csv file pisal ane..
    # od kdaj do kdaj, zacetna investicija, vse mesecne investicije, total contribution, zasluzili in koliko imamo
    vrstica = [datum_zacetka + "-" + datum_konca, initial_investment, mesecni_vlozki_vsota, initial_investment+mesecni_vlozki_vsota, zasluzili, investment]
    
    poimenovanje = input("Kako poimenujem file v katerega dam rezultate: ")
    
    with open(f"testing/{poimenovanje}.csv", mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(vrstica)
    

    return 0
