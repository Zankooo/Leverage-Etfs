from datetime import datetime

from izracuni import izracun_dnevnih_sprememb, formatiraj_kes_eur
from leverage_csv_file import calculate_leverage
from ne_pogosto_uporabljene.data_printer import fancy_print
from ne_pogosto_uporabljene.indeksi_zacetek_konec import najdi_indekse_zacetka_in_konca


def kdaj_kupiti_katerega(podatki):
    """
    Ta funkcija dela mesecne investicije prvega v mesecu.
    Naredit pa se da vedno ko pade pod 3 posto enkrat na mesec kupis
    :param podatki:
    :return:
    """
    print("Glavna funkcija laufa!")
    # z dnevnimi spremembami; datum tecaj, sprememba
    osnoven_indeks = izracun_dnevnih_sprememb(podatki)
    # z dnevnimi spremembami; datum, tecaj, sprememba
    leverage_indeks = calculate_leverage(podatki)



    # na indeksu 0 in 1 sta indeksa
    indeksa_zacetka_in_konca = najdi_indekse_zacetka_in_konca(podatki)
    indeks_zacetka = int(indeksa_zacetka_in_konca[0])
    indeks_konca = int(indeksa_zacetka_in_konca[1])

    # all time je prvi dan ki ga pac zberemo za zacetek

    investment_navaden = 0
    investment_leverage = 0
    zacetna_investicija = float(input("Koliko bo zacetka investicija? "))

    print("V kater indeks dam zacetno investicijo? ")
    v_kater_zacetno = int(input("1. Navaden, 2. Leverage? "))
    monthly_investment = float(input("Koliko vsak mesec? "))
    koliko_mora_pasti = float(input("Koliko mora biti prvega v mestu osnoven dol da kupimo leverage? "))
    v_cifri_koliko_mora_pasti = float(1 - (koliko_mora_pasti / 100))# ce je input 3 je pol 0.97

    mesecni_vlozki_vsota = 0

    all_time_high = float(podatki[indeks_zacetka][1])


    # dolocimo v kater indeks damo zacetno investicijo?
    if v_kater_zacetno == 1:
        investment_navaden = zacetna_investicija
    elif v_kater_zacetno == 2:
        investment_leverage = zacetna_investicija
    else:
        print("Napacna cifra")

 # Nastavimo začetni mesec za mesečne vložke
    trenutni_mesec = datetime.strptime(podatki[indeks_zacetka][0], "%Y-%m-%d").month

    # plus ena pri index_zacetka, ker se zacne obrestovat naslednji dan, ker pac mi kupimo po close price ta dan
    for i in range(indeks_zacetka + 1, indeks_konca + 1):
        # navaden indeks
        daily_change_navaden = osnoven_indeks[i][2].replace("%", "")  # Odstrani "%"
        daily_change_cifra_navaden = (float(daily_change_navaden)) / 100  # Pretvori v decimalno vrednost

        daily_change_leverage = leverage_indeks[i][2].replace("%", "")  # Odstrani "%"
        daily_change_cifra_leverage = (float(daily_change_leverage)) / 100

        #torej ce je indeks recimo vec kot 3 posto dol: ker je trenutni tecaj * 0.97
    # vzamemo ath mnozimo z 0.97 recimo, in ce je se vedno vecji, pomeni da je osnoven vec padel
        if float(osnoven_indeks[i][1]) > all_time_high:
            all_time_high = osnoven_indeks[i][1]
            print(f"Nov all time high je: ${all_time_high}")

        date = datetime.strptime(podatki[i][0], "%Y-%m-%d")

        # pogledamo ce ima trenutni dan isti mesec ali ne, ce ne, je nov mesec in gremo v if
        if date.month != trenutni_mesec:

            if float(osnoven_indeks[i][1]) < (all_time_high * v_cifri_koliko_mora_pasti):
                investment_leverage = investment_leverage + monthly_investment
                print(f"Ker je {koliko_mora_pasti}% dol od ath, smo dali {monthly_investment} ta mesec v leverage")
                mesecni_vlozki_vsota = mesecni_vlozki_vsota + monthly_investment
                trenutni_mesec = date.month
            else:
                investment_navaden = investment_navaden + monthly_investment
                print(f"Ta mesec investirali {monthly_investment} v navaden indeks")
                mesecni_vlozki_vsota = mesecni_vlozki_vsota + monthly_investment
                trenutni_mesec = date.month

        # Izračun vrednosti portfelja
        investment_navaden = investment_navaden * (1 + daily_change_cifra_navaden)
        investment_leverage = investment_leverage * (1 + daily_change_cifra_leverage)
        print(f"Portfelj statistics: {i}. oz. datumu {podatki[i][0]}:")
        print(f"Navaden indeks: {formatiraj_kes_eur(investment_navaden)}")
        print(f"Leverage indeks: {formatiraj_kes_eur(investment_leverage)}")
        print("----")

    print("-----------")
    print("REZULTATI:")
    print(f"{podatki[indeks_zacetka][0]} do {podatki[indeks_konca][0]}:")
    print(f"Začetna investicija je bila: {formatiraj_kes_eur(zacetna_investicija)} 📌")
    print(f"Vseh mesečnih investicij je bilo: {formatiraj_kes_eur(mesecni_vlozki_vsota)} 💸")
    print("---")
    print(f"Total contribution (zacetna + mesecne): {formatiraj_kes_eur(zacetna_investicija + mesecni_vlozki_vsota)} 🔢")
    print(f"V navadnem indeksu imamo vse skupaj: {investment_navaden}")
    print(f"V leverage indeksu imamo vse skupaj: {investment_leverage}")
    zasluzili = (investment_navaden + investment_leverage) - zacetna_investicija - monthly_investment
    print(f"Torej zaslužili / izgubili smo: {formatiraj_kes_eur(zasluzili)} 🏆")

def kdaj_kupiti_katerega_ta_dela(podatki):
    """Ta funkcija zgleda dela, ker zgornja pac ne... Preverit ce prav dela
    Funkcija pac kupuje prvega v mesecu, naredit se da vedno ko pade recimo x da kupi, in to samo enkrat v mesecu
    in se prilagodit na vec nacinov in taktik"""
    print("Glavna funkcija laufa!")
    osnoven_indeks = izracun_dnevnih_sprememb(podatki)
    leverage_indeks = calculate_leverage(podatki)

    indeksa_zacetka_in_konca = najdi_indekse_zacetka_in_konca(podatki)
    indeks_zacetka = indeksa_zacetka_in_konca[0]
    indeks_konca = indeksa_zacetka_in_konca[1]

    investment_navaden = 0
    investment_leverage = 0
    zacetna_investicija = float(input("Koliko bo zacetka investicija? "))

    print("V kater indeks dam zacetno investicijo? ")
    v_kater_zacetno = int(input("1. Navaden, 2. Leverage? "))
    monthly_investment = float(input("Koliko vsak mesec? "))
    koliko_mora_pasti = float(input("Koliko mora biti prvega v mestu osnoven dol da kupimo leverage? "))
    v_cifri_koliko_mora_pasti = 1 - (koliko_mora_pasti / 100)

    mesecni_vlozki_vsota = 0
    print("---------")
    # Prisili pretvorbo v float in odstrani nezaželene znake
    try:
        all_time_high = float(str(podatki[indeks_zacetka][1]).replace(",", "").strip())
    except ValueError:
        print(f"Napaka pri pretvorbi podatki[{indeks_zacetka}][1]: {podatki[indeks_zacetka][1]}")
        return

    if v_kater_zacetno == 1:
        investment_navaden = zacetna_investicija
    elif v_kater_zacetno == 2:
        investment_leverage = zacetna_investicija
    else:
        print("Napacna cifra")

    trenutni_mesec = datetime.strptime(podatki[indeks_zacetka][0], "%Y-%m-%d").month

    for i in range(indeks_zacetka + 1, indeks_konca + 1):
        try:
            daily_change_navaden = float(osnoven_indeks[i][2].replace("%", "")) / 100
            daily_change_leverage = float(leverage_indeks[i][2].replace("%", "")) / 100
            current_price = float(str(osnoven_indeks[i][1]).replace(",", "").strip())
        except ValueError:
            print(f"Napaka pri pretvorbi vrednosti na indeksu {i}: {osnoven_indeks[i]}")
            continue

        if current_price > all_time_high:
            all_time_high = current_price
            print(f"Nov all time high je: ${all_time_high}")

        date = datetime.strptime(podatki[i][0], "%Y-%m-%d")

        if date.month != trenutni_mesec:
            if current_price < (all_time_high * v_cifri_koliko_mora_pasti):
                investment_leverage += monthly_investment
                #koliko je dol od ath
                padec_od_ath = ((all_time_high - current_price) / all_time_high) * 100
                print(f"Ker je {koliko_mora_pasti}% dol (dejansko je dol{round(padec_od_ath,2)}) od ATH, smo dali {monthly_investment} ta mesec v leverage,")

            else:
                investment_navaden += monthly_investment
                print(f"Ta mesec investirali {monthly_investment} v navaden indeks")
            mesecni_vlozki_vsota += monthly_investment
            trenutni_mesec = date.month

        investment_navaden *= (1 + daily_change_navaden)
        investment_leverage *= (1 + daily_change_leverage)

        print(f"{i}. {podatki[i][0]} - Navaden: {formatiraj_kes_eur(investment_navaden)} {osnoven_indeks[i][2]}%, Leverage: {formatiraj_kes_eur(investment_leverage)} {leverage_indeks[i][2]}%")

    print("-----------\nREZULTATI:")
    print(f"{podatki[indeks_zacetka][0]} do {podatki[indeks_konca][0]}")
    print(f"Začetna investicija: {formatiraj_kes_eur(zacetna_investicija)} 📌")
    print(f"Vseh mesečnih investicij: {formatiraj_kes_eur(mesecni_vlozki_vsota)} 💸")
    print(f"Total contribution: {formatiraj_kes_eur(zacetna_investicija + mesecni_vlozki_vsota)} 🔢")
    print(f"V navadnem indeksu: {formatiraj_kes_eur(investment_navaden)}, v leverage: {formatiraj_kes_eur(investment_leverage)}")
    zasluzili = (investment_navaden + investment_leverage) - (zacetna_investicija + mesecni_vlozki_vsota)
    print(f"Torej zaslužili / izgubili: {formatiraj_kes_eur(zasluzili)} 🏆")



#TO FUNKCIJO SPROBAT NA NEKEM PRIMERU, NISEM FIX CE CISTO PRAV DELA
def kdaj_kupiti_katerega_ta_dela(podatki):
    """Ta funkcija zgleda dela, ker zgornja pac ne... Preverit ce prav dela
    Funkcija pac kupuje prvega v mesecu, naredit se da vedno ko pade recimo x da kupi, in to samo enkrat v mesecu
    in se prilagodit na vec nacinov in taktik"""
    print("Glavna funkcija laufa!")
    osnoven_indeks = izracun_dnevnih_sprememb(podatki)
    leverage_indeks = calculate_leverage(podatki)

    indeksa_zacetka_in_konca = najdi_indekse_zacetka_in_konca(podatki)
    indeks_zacetka = indeksa_zacetka_in_konca[0]
    indeks_konca = indeksa_zacetka_in_konca[1]

    investment_navaden = 0
    investment_leverage = 0
    zacetna_investicija = float(input("Koliko bo zacetka investicija? "))

    print("V kater indeks dam zacetno investicijo? ")
    v_kater_zacetno = int(input("1. Navaden, 2. Leverage? "))
    monthly_investment = float(input("Koliko vsak mesec? "))
    koliko_mora_pasti = float(input("Koliko mora biti prvega v mestu osnoven dol da kupimo leverage? "))
    v_cifri_koliko_mora_pasti = 1 - (koliko_mora_pasti / 100)

    mesecni_vlozki_navaden_vsota = 0
    mesecni_vlozki_leverage_vsota = 0
    print("---------")
    # Prisili pretvorbo v float in odstrani nezaželene znake
    try:
        all_time_high = float(str(podatki[indeks_zacetka][1]).replace(",", "").strip())
    except ValueError:
        print(f"Napaka pri pretvorbi podatki[{indeks_zacetka}][1]: {podatki[indeks_zacetka][1]}")
        return

    #dolocimo v katerega damo zacetno investicijo
    osnoven_zacetna = False
    if v_kater_zacetno == 1:
        investment_navaden = zacetna_investicija
        osnoven_zacetna = True
    elif v_kater_zacetno == 2:
        investment_leverage = zacetna_investicija
    else:
        print("Napacna cifra")

    #dobimo trenutni mesec
    trenutni_mesec = datetime.strptime(podatki[indeks_zacetka][0], "%Y-%m-%d").month

    for i in range(indeks_zacetka + 1, indeks_konca + 1):
        try:
            daily_change_navaden = float(osnoven_indeks[i][2].replace("%", "")) / 100
            daily_change_leverage = float(leverage_indeks[i][2].replace("%", "")) / 100
            current_price = float(str(osnoven_indeks[i][1]).replace(",", "").strip())
        except ValueError:
            print(f"Napaka pri pretvorbi vrednosti na indeksu {i}: {osnoven_indeks[i]}")
            continue

        if current_price > all_time_high:
            all_time_high = current_price
            print(f"Nov all time high je osnovnega: {osnoven_indeks[i][0]}; ${round(all_time_high,2)}")

        mesec = datetime.strptime(podatki[i][0], "%Y-%m-%d").month

        # TUKAJ KO JE NOV MESEC, SE POL ODLOCIMO KDAJ V KATEREGA INVESTAMO
        if mesec != trenutni_mesec:
            # tuki fiksat ker on investa takoj prvega in pokasera donos tega dneva, more pa ob koncu dneva
            if current_price < (all_time_high * v_cifri_koliko_mora_pasti):
                investment_leverage = investment_leverage + monthly_investment
                mesecni_vlozki_leverage_vsota = mesecni_vlozki_leverage_vsota + monthly_investment
                #koliko je dol od ath
                padec_od_ath = ((all_time_high - current_price) / all_time_high) * 100
                print(f"Ker je osnoven več kot {koliko_mora_pasti}% dol, (dejansko je dol {round(padec_od_ath,2)}%) od ATH, smo dali {monthly_investment} ta mesec v leverage")
                trenutni_mesec = mesec
            else:
                investment_navaden = investment_navaden + monthly_investment
                mesecni_vlozki_navaden_vsota = mesecni_vlozki_navaden_vsota + monthly_investment
                padec_od_ath = ((all_time_high - current_price) / all_time_high) * 100
                print(f"Ker je osnoven manj kot {koliko_mora_pasti}% dol, (dejansko je dol {round(padec_od_ath, 2)}%) od ATH, smo dali {monthly_investment} ta mesec v osnovnega")
                trenutni_mesec = mesec

        # TUKI JE OBRESTOVANJE V VSAKI ITERACIJI
        investment_navaden *= (1 + daily_change_navaden)
        investment_leverage *= (1 + daily_change_leverage)
        # IN IZPIS STANJA
        print(
            f"{podatki[i][0]} - NAVADEN -> {formatiraj_kes_eur(investment_navaden)} (tecaj: {float(osnoven_indeks[i][1]):.2f}), dnevna sprememba: {daily_change_navaden * 100:.2f}% | "
            f"LEVERAGE -> {formatiraj_kes_eur(investment_leverage)} (tecaj: {float(leverage_indeks[i][1]):.2f}), dnevna sprememba: {daily_change_leverage * 100:.2f}%")

    print("-----------\nREZULTATI:")
    print(f"{podatki[indeks_zacetka][0]} do {podatki[indeks_konca][0]}")
    print(f"Začetna investicija: {formatiraj_kes_eur(zacetna_investicija)} 📌")

   #da vemo kateremu pristet zacetno
    if osnoven_zacetna == True:
        print(f"Vseh investicij v osnovnega je bilo: {formatiraj_kes_eur(mesecni_vlozki_navaden_vsota + zacetna_investicija)}")
        print(f"Vseh investicij v leverage je bilo: {formatiraj_kes_eur(mesecni_vlozki_leverage_vsota)}")
    else:
        print(f"Vseh investicij v osnovnega je bilo: {formatiraj_kes_eur(mesecni_vlozki_navaden_vsota)}")
        print(f"Vseh investicij v leverage je bilo: {formatiraj_kes_eur(mesecni_vlozki_leverage_vsota  + zacetna_investicija)}")

    print(f"Total investicij: {formatiraj_kes_eur(zacetna_investicija + mesecni_vlozki_navaden_vsota + mesecni_vlozki_leverage_vsota)} 💸")
    print(f"V Navadnem indeksu imamo: {formatiraj_kes_eur(investment_navaden)}, v Leverage imamo: {formatiraj_kes_eur(investment_leverage)}")
    zasluzili = (investment_navaden + investment_leverage) - (zacetna_investicija + mesecni_vlozki_navaden_vsota + mesecni_vlozki_leverage_vsota)
    print(f"Torej zaslužili / izgubili: {formatiraj_kes_eur(zasluzili)} 🏆")