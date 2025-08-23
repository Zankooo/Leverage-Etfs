import re
import os
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


def izracun_letnih_donosov(podatki):
    """
    Ne vem kako ta funkcija dela ampak dela!
    Funkcija ki sprejme podatke, list of lists
    In izracuna donos za Vsako leto. -> to funkcijo nikjer ne uporabim ampak je za vsak slucaj kle ce me kdaj zanima
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


# ----------------------------------------------------------------
def izracun_dca_metoda(podatki, output_file="rezultati_investicije.csv"):
    """
    Funkcija izracuna koliko imamo kesa po izbranem obdobju. Damo notri nek csv z nekimi podatki. 
    1x 2x 3x kere kol podatke, le da imajo pravilno obliko
    Torej: izberemo začetno investicijo + mesečne vložke(prvega v mesecu oz na zacetku meseca, se obracunajo).
    Izračuna končno vrednost investicije glede na vsakodnevno spremembo indeksa.
    :param podatki: List of lists dogovorjen format
    :return: int končna vrednost investicije
    :return; ustvari še csv file z rezultati za vsak dan
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
    #datum_zacetka = input("Začetek investiranja datum: ")
    #datum_konca = input("Konec investiranja datum: ")
    # za namen testiranja da ne rabim skos pisat notr
    datum_zacetka = "2015-10-22"
    datum_konca = "2016-03-31"

    # Nastavimo začetni mesec za mesečne vložke
    current_month = datetime.strptime(datum_zacetka, "%Y-%m-%d").month

    # to rabimo da lahko pozenemo loop cez vse dneve
    vrstica_zacetka = (next(i for i, row in enumerate(podatki) if row[0] == datum_zacetka))
    vrstica_konca = (next(i for i, row in enumerate(podatki) if row[0] == datum_konca))

    results = []
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
        
        results.append([podatki[i][0], round(investment, 2), daily_change + "%"])


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
    

    with open(output_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["date", "A"])
        writer.writerows(results)

    print(f"Rezultati so zapisani v {output_file}")
    return round(investment, 2)

# -------------------------- spremenjena funkcija dca za testing
# --------------------------------------------

# ta funkcija tocno zracuna isto k kot funkcija 'izracun dca metoda' le da vse tri 1x in 2x in 3x naredi
# in jih da v locen csv!!
import csv
from datetime import datetime

def izracun_dca_metoda_prilagojena_da_naredi_csv(
    podatki1, podatki2, podatki3,  # morajo biti isti indeks: osnovni, 2x, 3x
    initial_investment: float,
    monthly_investment: float,
    datum_zacetka: str = "2009-02-19",
    datum_konca: str   = "2016-03-31",
    output_file: str   = "rezultati_investicije.csv",
):
    """
    DCA simulacija za 3 serije z ISTO začetno investicijo in ISTIM mesečnim vložkom.
    Mesečni vložek se doda ob prvem razpoložljivem dnevu NOVEGA meseca (po podatkih serije 1).
    Zapiše CSV: date, A, B, C in vrne končne vrednosti (A, B, C).
    Zahteva: izracun_dnevnih_sprememb(podatkiX) -> ...[i][2] = '±x.xx%'.
    """

    # dnevne spremembe (nizi s percenti)
    spremembe1 = izracun_dnevnih_sprememb(podatki1)
    spremembe2 = izracun_dnevnih_sprememb(podatki2)
    spremembe3 = izracun_dnevnih_sprememb(podatki3)

    # poiščemo indekse intervala v vseh treh
    s1 = next(i for i, row in enumerate(podatki1) if row[0] == datum_zacetka)
    e1 = next(i for i, row in enumerate(podatki1) if row[0] == datum_konca)
    s2 = next(i for i, row in enumerate(podatki2) if row[0] == datum_zacetka)
    e2 = next(i for i, row in enumerate(podatki2) if row[0] == datum_konca)
    s3 = next(i for i, row in enumerate(podatki3) if row[0] == datum_zacetka)
    e3 = next(i for i, row in enumerate(podatki3) if row[0] == datum_konca)

    len1 = e1 - s1 + 1
    len2 = e2 - s2 + 1
    len3 = e3 - s3 + 1
    if not (len1 == len2 == len3):
        raise ValueError(f"Intervali serij se ne ujemajo (len1={len1}, len2={len2}, len3={len3}).")

    # začetno stanje (enako za vse tri)
    inv1 = float(initial_investment)
    inv2 = float(initial_investment)
    inv3 = float(initial_investment)

    # števci mesečnih vložkov (na serijo)
    vsota_mesecnih_vlozkov = 0.0
    st_vplacil = 0

    current_month = datetime.strptime(datum_zacetka, "%Y-%m-%d").month
    results = []

    for k in range(len1):
        i1, i2, i3 = s1 + k, s2 + k, s3 + k
        date_str = podatki1[i1][0]

        # poravnava datumov
        if podatki2[i2][0] != date_str or podatki3[i3][0] != date_str:
            raise ValueError(f"Datumi se ne ujemajo pri k={k}: {date_str} vs {podatki2[i2][0]} / {podatki3[i3][0]}")

        date_obj = datetime.strptime(date_str, "%Y-%m-%d")

        # ob prehodu v nov mesec dodamo mesečni vložek vsem trem (vplačilo šteje ENKRAT na serijo)
        if date_obj.month != current_month:
            inv1 += monthly_investment
            inv2 += monthly_investment
            inv3 += monthly_investment
            vsota_mesecnih_vlozkov += monthly_investment
            st_vplacil += 1
            current_month = date_obj.month

        # % → decimal
        ch1 = round(float(spremembe1[i1][2].replace("%", "")), 2) / 100.0
        ch2 = round(float(spremembe2[i2][2].replace("%", "")), 2) / 100.0
        ch3 = round(float(spremembe3[i3][2].replace("%", "")), 2) / 100.0

        inv1 *= (1.0 + ch1)
        inv2 *= (1.0 + ch2)
        inv3 *= (1.0 + ch3)

        results.append([date_str, round(inv1, 2), round(inv2, 2), round(inv3, 2)])

    # zapis CSV
    with open(output_file, mode="w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["date", "A", "B", "C"])
        w.writerows(results)

    # izpis povzetka (na serijo)
    
    print(f"Začetna investicija (na serijo): {initial_investment:.2f} EUR")
    print(f"Vsota mesečnih vložkov (na serijo): {vsota_mesecnih_vlozkov:.2f} EUR  (št. vplačil: {st_vplacil})")

    return round(inv1, 2), round(inv2, 2), round(inv3, 2)



























# TA METODA JE FIXERICA KER SE JO KLICE V FOR LOOPU - POTREBNA ZA KONZOLA PRIMERJAVO!
def metoda_dca_za_testing_prilagojena(podatki, initial_investment, monthly_investment, datum_zacetka, datum_konca, ime_novega_filea):
    """
    Funkcija ista kot una zgoraj le da prejmemo kot parametri in ne izpisujemo vsega
    prilagojena je da delamo testing na njen
    testing pa delamo tako da ji damo razlicne datum zacetka in datum konca...
    te datum zacetka pa konca pa dobim iz funkcije "generiraj_intervale_15let_leto"
    @param podakti v dogovorjeni obliki
    @param zacetna investicija
    @param mesecne investicije
    @param datum zacetka
    @param datum konca
    @param ime novega fajla
    @return nic -> v bistvu v nov csv file izpise rezultate
    """
    # ta funkcija je misljena da se jo klice v mainu v for loopu toliko koliko je intervalov in da se ji podaja razlicne datume pridobljena iz intervali letni
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
   
    # od tukaj naprej je pa pisanje v file
    # da bi v csv file pisal ane..
    # od kdaj do kdaj, zacetna investicija, vse mesecne investicije, total contribution, zasluzili in koliko imamo
    vrstica = [datum_zacetka + "-" + datum_konca, initial_investment, mesecni_vlozki_vsota, initial_investment + mesecni_vlozki_vsota, zasluzili, investment]
    
    ime_novega_filea = ime_novega_filea + ".csv"
    pot = f"testing/{ime_novega_filea}"

    # Ustvari mapo testing, če ne obstaja
    os.makedirs("testing", exist_ok=True)

    # Če datoteka obstaja, dodaj v obstoječo, drugače ustvari novo
    mode = "a" if os.path.exists(pot) else "w"

    with open(pot, mode=mode, newline="") as f:
        writer = csv.writer(f)
        
        if mode == "w":  # pišemo header samo če ustvarjamo novo datoteko
            writer.writerow([ime_novega_filea])
            writer.writerow([
                "Datum od kdaj do kdaj",
                "Zacetna investicija",
                "vse mesecne investicije",
                "skupaj vse investicije",
                "koliko smo v plusu oz minusu",
                "koliko imamo vse skupaj"
            ])
        
        writer.writerow(vrstica)
    
    return 0


 # ------------------------------------------------------

