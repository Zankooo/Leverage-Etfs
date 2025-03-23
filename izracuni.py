import pandas as pd
from csv_operacije import *
from ne_pogosto_uporabljene.indeksi_zacetek_konec import najdi_indekse_zacetka_in_konca


# karkoli tukaj delamo oz kero kol funkcijo klicemo moramo imeti
# dogovorjen format podatkov oz csv.ja!

def izracun_dnevnih_sprememb(podatki):
    """
    Funkcija, ki izracuna dnevne spremembe indeksa
    :param list of lists (dogovorjen format)
    :return list of lists tak kot je bil podan in mu doda dnevne spremembe "daily changes"
    """
    # Dodamo stolpec 'Daily Change (%)' prvo vrstico
    result = [podatki[0]]
    # Inicializacija prve vrstice brez spremembe
    result.append(podatki[1] + ["Change (%)"])  # Prvi dan ni spremembe
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

def izracun_dobicka_dca(podatki):
    """
    Funkcija izracuna koliko imamo kesa po izbranem obdobju
    Torej: izberemo začetno investicijo + mesečne vložke(prvega v mesecu oz na zacetku meseca, se obracunajo).
    Izračuna končno vrednost investicije glede na vsakodnevno spremembo indeksa.
    :param podatki: List of lists dogovorjen format, kerkoli indeks seveda
    :return: int končna vrednost investicije
    """
   # TA FUNKCIJA DEJANSKO DELA ZELO DOBR
    podatki_daily_changes = izracun_dnevnih_sprememb(podatki)

    initial_investment = int(input("Vpisi začetno investicijo: "))
    monthly_investment = int(input("Vpisi mesečni vložek: "))  # Nov vnos za mesečno investicijo
    investment = initial_investment
    mesecni_vlozki_vsota = 0

    # klicemo funkcijo da dobimo indeksa zacetka in konca
    indeksa_zacetka_in_konca = najdi_indekse_zacetka_in_konca(podatki)
    index_zacetka = indeksa_zacetka_in_konca[0]
    index_konca = indeksa_zacetka_in_konca[1]

    # Nastavimo začetni mesec za mesečne vložke
    current_month = datetime.strptime(podatki[index_zacetka][0], "%Y-%m-%d").month
    # plus ena pri index_zacetka, ker se zacne obrestovat naslednji dan, ker pac mi kupimo po close price ta dan
    for i in range(index_zacetka + 1, index_konca + 1):
        daily_change = podatki_daily_changes[i][2].replace("%", "")  # Odstrani "%"
        daily_change_cifra = (float(daily_change)) / 100  # Pretvori v decimalno vrednost
        # Pridobimo mesec trenutnega datuma
        date = datetime.strptime(podatki[i][0], "%Y-%m-%d")
        # Če je nov mesec, dodamo mesečni vložek
        if date.month != current_month:
            # kupimo ta dan na koncu dneva, ob close pac -> recimo prvega v mesecu ob close ceni
            investment = investment + monthly_investment
            print(f"Mesecna investicija investirana: {monthly_investment}eur")
            mesecni_vlozki_vsota = mesecni_vlozki_vsota + monthly_investment
            current_month = date.month
        # Izračun vrednosti portfelja
        investment = investment * (1 + daily_change_cifra)
        print(f"Vrednost pri vrstici {i}. oz. datumu {podatki[i][0]}: {investment:.2f} EUR ({daily_change}%)")
    print("-----------")
    print("REZULTATI:")
    print(f"{podatki[index_zacetka][0]} do {podatki[index_konca][0]}:")
    print(f"Začetna investicija je bila: {formatiraj_kes_eur(initial_investment)} 📌")
    print(f"Vseh mesečnih investicij je bilo: {formatiraj_kes_eur(mesecni_vlozki_vsota)} 💸")
    print("---")
    print(f"Total contribution (zacetna + mesecne): {formatiraj_kes_eur(initial_investment + mesecni_vlozki_vsota)} 🔢")
    zasluzili = investment - initial_investment - mesecni_vlozki_vsota
    print(f"Torej zaslužili / izgubili smo: {formatiraj_kes_eur(zasluzili)} 🏆")
    print(f"Imamo vse skupaj: {formatiraj_kes_eur(investment)} EUR 💰✈️🌍")
    # to prikazemo samo ce imamo brez mescecnih. Edini namen je dokaz/prikazati, da pac ce potegnemo na google grafu da pac res dela funkcija
    if mesecni_vlozki_vsota == 0:
        procentualno_zasluzek = (zasluzili / initial_investment) * 100
        procentualno_zasluzek = round(procentualno_zasluzek, 2)
        print(f"Procentualno: {procentualno_zasluzek}%. Lahko preveris na Google stock grafu, da je zelo zelo podobno")
    # procentualno je izracunano ->  (donos/cela investicija)*100
    # tukaj ce so mesecne investicije je malo drugace in treba nekako fiksat
    return round(investment, 2)


#----------- POMOZNE FUNKCIJE; TEH DVEH FUNKCIJ ČIST NE RAZUMEM IN NE VEM CE PRAV DELATA-----------
def izracun_dobicka_prodaj_kupi(podatki):
    #STESTIRAL IN KAO DELA, SE ENKRAT STESTIRAT Z ANDROTOM, NAPISAT PODATKE NA LIST IN STESTIRAT
    # ugotavljat zakaj se splaca kdaj in kdaj ne, ker je veliko taktike tukaj
    podatki_daily_changes = izracun_dnevnih_sprememb(podatki)

    initial_investment = int(input("Vpisi začetno investicijo: "))
    investment = initial_investment

    # dobimo datume
    indeksa_zacetka_in_konca = najdi_indekse_zacetka_in_konca(podatki)
    index_zacetka = indeksa_zacetka_in_konca[0]
    index_konca = indeksa_zacetka_in_konca[1]

    input_koliko_more_padet_da_prodas = float(input("Koliko mora padet da prodas? (%): "))
    input_koliko_mora_potem_spet_zrasti = float(input("Koliko mora potem spet zrasti od vrednosti, kjer si prodal, da spet nazaj kupis? (%): "))
    # pretvorba v format za izracunanje, recimo ce je 1, to je 0,99
    koliko_more_padet = 1 - (input_koliko_more_padet_da_prodas / 100)
    # # pretvorba v format za izracunanje, recimo ce je 2, to je 1,02
    koliko_mora_potem_zrast = 1 + (input_koliko_mora_potem_spet_zrasti / 100)
    # ta metoda dela tako da kupis ko zraste od tok kokr si prodal, in ne od all time low
    # naredit se eno funkcijo ki od all time low
    ne_investiran_denar = 0
    invested = True
    prodal_pri = None
    tecaj_od_katerega_more_padet_da_prodamo = float(podatki[index_zacetka][1])
    print("--------------------------------")
    for i in range(index_zacetka + 1, index_konca + 1):
        trenutni_tecaj = float(podatki[i][1])
        if invested and trenutni_tecaj > tecaj_od_katerega_more_padet_da_prodamo:
            tecaj_od_katerega_more_padet_da_prodamo = trenutni_tecaj
            print(f"Nov all time high je {tecaj_od_katerega_more_padet_da_prodamo} od te vrednosti more pasti {input_koliko_more_padet_da_prodas}% da prodamo")
        # recimo ce damo da max pade 3, je to trenutni tecaj mora biti manjsi kot all time high * 0,97
        if invested and trenutni_tecaj <= tecaj_od_katerega_more_padet_da_prodamo * koliko_more_padet:
            print(f"Prodal pri {podatki[i]}, zrasti mora {input_koliko_mora_potem_spet_zrasti}% da spet kupimo")
            print(f"In to na vsaj: {trenutni_tecaj * koliko_mora_potem_zrast}eur")
            prodal_pri = trenutni_tecaj
            dnevna_sprememba = float(podatki_daily_changes[i][2].replace("%", "")) / 100
            investment = investment * (1 + dnevna_sprememba)
            ne_investiran_denar = investment
            print(f"imamo toliko denarja {ne_investiran_denar}eur")
            investment = 0
            invested = False
        # recimo ce smo prodali pri 80 in damo; da mora zrasti 3% torej ko je trenutni vecji ali enak 82,4
        elif not invested and trenutni_tecaj >= prodal_pri * koliko_mora_potem_zrast:
            print(f"Kupil pri {podatki[i]}")
            investment = ne_investiran_denar
            ne_investiran_denar = 0
            invested = True
            tecaj_od_katerega_more_padet_da_prodamo = trenutni_tecaj

        elif invested and (trenutni_tecaj > tecaj_od_katerega_more_padet_da_prodamo * koliko_more_padet):
            dnevna_sprememba = float(podatki_daily_changes[i][2].replace("%", "")) / 100
            # tuki prej delil z 100 ampak je ze deljeno z sto v zgornji vrstici.
            # preverit na listu papirja ce deluje
            investment = investment * (1 + dnevna_sprememba)

            print(f"Investirano imamo pri {podatki[i]}in toliko je vredno: {investment}eur")
        elif not invested:
            print(f"Nimamo investirano pri {podatki[i]}")

    print("--------------------------------")
    print(f"Zacetna investicija je bila {formatiraj_kes_eur(initial_investment)}")
    print("Zasluzili smo tok eur:")
    zasluzili = investment if invested else ne_investiran_denar
    print(formatiraj_kes_eur(zasluzili))
    return zasluzili

def izracun_dobicka_prodaj_kupi_low(podatki):
    #STESTIRAL IN KAO DELA, SE ENKRAT STESTIRAT Z ANDROTOM, NAPISAT PODATKE NA LIST IN STESTIRAT
    # ugotavljat zakaj se splaca kdaj in kdaj ne, ker je veliko taktike tukaj
    podatki_daily_changes = izracun_dnevnih_sprememb(podatki)

    initial_investment = int(input("Vpisi začetno investicijo: "))
    investment = initial_investment

    # dobimo datume
    indeksa_zacetka_in_konca = najdi_indekse_zacetka_in_konca(podatki)
    index_zacetka = indeksa_zacetka_in_konca[0]
    index_konca = indeksa_zacetka_in_konca[1]

    input_koliko_more_padet_da_prodas = float(input("Koliko mora padet da prodas? (%): "))
    input_koliko_mora_potem_spet_zrasti = float(input("Koliko mora potem spet zrasti od vrednosti, kjer si prodal, da spet nazaj kupis? (%): "))
    # pretvorba v format za izracunanje, recimo ce je 1, to je 0,99
    koliko_more_padet = 1 - (input_koliko_more_padet_da_prodas / 100)
    # # pretvorba v format za izracunanje, recimo ce je 2, to je 1,02
    koliko_mora_potem_zrast = 1 + (input_koliko_mora_potem_spet_zrasti / 100)
    # ta metoda dela tako da kupis ko zraste od tok kokr si prodal, in ne od all time low
    # naredit se eno funkcijo ki od all time low
    ne_investiran_denar = 0
    invested = True
    tecaj_od_katerega_mora_zrasti = float
    tecaj_od_katerega_more_padet_da_prodamo = float(podatki[index_zacetka][1])
    print("--------------------------------")
    for i in range(index_zacetka + 1, index_konca + 1):
        trenutni_tecaj = float(podatki[i][1])

        if invested and trenutni_tecaj > tecaj_od_katerega_more_padet_da_prodamo:
            tecaj_od_katerega_more_padet_da_prodamo = trenutni_tecaj
            print(f"Od te vrednosti mora sedaj pasti {tecaj_od_katerega_more_padet_da_prodamo}. Od te vrednosti more pasti {input_koliko_more_padet_da_prodas}% da prodamo, torej {tecaj_od_katerega_more_padet_da_prodamo * koliko_more_padet}eur")

        # recimo ce damo da max pade 3, je to trenutni tecaj mora biti manjsi kot all time high * 0,97
        if invested and trenutni_tecaj <= tecaj_od_katerega_more_padet_da_prodamo * koliko_more_padet:
            print(f"Prodal pri {podatki[i]}, zrasti mora {input_koliko_mora_potem_spet_zrasti}% da spet kupimo")
            print(f"In to na vsaj: {trenutni_tecaj * koliko_mora_potem_zrast}eur")
            tecaj_od_katerega_mora_zrasti = trenutni_tecaj
            dnevna_sprememba = float(podatki_daily_changes[i][2].replace("%", "")) / 100
            investment = investment * (1 + dnevna_sprememba)
            ne_investiran_denar = investment
            print(f"Imamo toliko denarja {ne_investiran_denar}eur")
            investment = 0
            invested = False

        # recimo ce smo prodali pri 80 in damo; da mora zrasti 3% torej ko je trenutni vecji ali enak 82,4
        elif not invested and trenutni_tecaj >= (float(tecaj_od_katerega_mora_zrasti) * float(koliko_mora_potem_zrast)):
            print(f"Kupil pri {podatki[i]}")
            investment = ne_investiran_denar
            ne_investiran_denar = 0
            invested = True
            tecaj_od_katerega_more_padet_da_prodamo = trenutni_tecaj

        elif invested and (trenutni_tecaj > tecaj_od_katerega_more_padet_da_prodamo * koliko_more_padet):
            dnevna_sprememba = float(podatki_daily_changes[i][2].replace("%", "")) / 100
            # tuki prej delil z 100 ampak je ze deljeno z sto v zgornji vrstici.
            # preverit na listu papirja ce deluje
            investment = investment * (1 + dnevna_sprememba)
            print(f"Investirano imamo pri {podatki[i]}in toliko je vredno: {investment}eur")

        elif not invested:
            print(f"Nimamo investirano pri {podatki[i]}")
            tecaj_od_katerega_mora_zrasti = podatki[i][1]
            #print(f"Nov all time low je {tecaj_od_katerega_mora_zrasti}. Od te vrednosti mora zrasti {input_koliko_mora_potem_spet_zrasti}% da kupimo, torej {tecaj_od_katerega_mora_zrasti * koliko_mora_potem_zrast}eur")

    print("--------------------------------")
    print(f"Zacetna investicija je bila {formatiraj_kes_eur(initial_investment)}")
    print("Zasluzili smo tok eur:")
    zasluzili = investment if invested else ne_investiran_denar
    print(formatiraj_kes_eur(zasluzili))
    return zasluzili




#----------- POMOZNE FUNKCIJE KI JIH KLIČEMO ZNOTRAJ DRUGIH FUNKCIJ-----------

def is_float(value):
    """Notranja funkcija; Preveri, ali je podana vrednost veljaven float."""
    try:
        float(value)
        return True
    except ValueError:
        return False

def formatiraj_kes_eur(vrednost):
    return f"{vrednost:,.2f} €".replace(",", "X").replace(".", ",").replace("X", ".")

def formatiraj_kes_dolar(vrednost):
    return f"${vrednost:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")




#----------- FUNKCIJE KI NISO TAKTIKE OZ SO ZA ZRAVEN MALO ZA FORO-----------
def izracun_letnih_donosov_indeksa(podatki):
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
        annual_returns.append([int(year), round(first_price,2), round(last_price,2), round(return_pct,2)])
    return annual_returns




