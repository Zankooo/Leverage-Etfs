from datetime import datetime

from izracuni import izracun_dnevnih_sprememb, formatiraj_kes
from leverage_csv_file import calculate_leverage
from ne_pogosto_uporabljene.data_printer import fancy_print
from ne_pogosto_uporabljene.indeksi_zacetek_konec import najdi_indekse_zacetka_in_konca


def kdaj_kupiti_katerega(podatki):
    print("Glavna funkcija laufa!")
    # z dnevnimi spremembami; datum tecaj, sprememba
    osnoven_indeks = izracun_dnevnih_sprememb(podatki)
    # z dnevnimi spremembami; datum, tecaj, sprememba
    leverage = calculate_leverage(podatki)



    # na indeksu 0 in 1 sta indeksa
    indeksa_zacetka_in_konca = najdi_indekse_zacetka_in_konca(podatki)
    indeks_zacetka = indeksa_zacetka_in_konca[0]
    indeks_konca = indeksa_zacetka_in_konca[1]

    # all time je prvi dan ki ga pac zberemo za zacetek

    investment_navaden = 0
    zacetna_investicija = float(input("Koliko bo zacetka investicija?"))
    monthly_investment = float(input("Koliko vsak mesec?"))

    mesecni_vlozki_vsota = 0
    all_time_high = podatki[indeks_zacetka][1]

 # Nastavimo začetni mesec za mesečne vložke
    trenutni_mesec = datetime.strptime(podatki[indeks_zacetka][0], "%Y-%m-%d").month

    # plus ena pri index_zacetka, ker se zacne obrestovat naslednji dan, ker pac mi kupimo po close price ta dan
    for i in range(indeks_zacetka + 1, indeks_konca + 1):
        daily_change = osnoven_indeks[i][2].replace("%", "")  # Odstrani "%"
        daily_change_cifra = (float(daily_change)) / 100  # Pretvori v decimalno vrednost

        # trenutni dan
        date = datetime.strptime(podatki[i][0], "%Y-%m-%d")

        # pogledamo ce ima trenutni dan isti mesec ali ne, ce ne, je nov mesec in gremo v if
        if date.month != trenutni_mesec:

            # kupimo ta dan na koncu dneva, ob close pac -> recimo prvega v mesecu ob close ceni
            investment_navaden = investment_navaden + monthly_investment
            print(f"Mesecna investicija investirana: {monthly_investment}eur")
            mesecni_vlozki_vsota = mesecni_vlozki_vsota + monthly_investment
            trenutni_mesec = date.month

        # Izračun vrednosti portfelja
        investment = investment_navaden * (1 + daily_change_cifra)
        print(f"Vrednost pri vrstici {i}. oz. datumu {podatki[i][0]}: {investment:.2f} EUR ({daily_change}%)")


    print("-----------")
    print("REZULTATI:")
    print(f"{podatki[indeks_zacetka][0]} do {podatki[indeks_konca][0]}:")
    print(f"Začetna investicija je bila: {formatiraj_kes(zacetna_investicija)} 📌")
    print(f"Vseh mesečnih investicij je bilo: {formatiraj_kes(mesecni_vlozki_vsota)} 💸")
    print("---")
    print(f"Total contribution (zacetna + mesecne): {formatiraj_kes(zacetna_investicija + mesecni_vlozki_vsota)} 🔢")
    zasluzili = investment_navaden - zacetna_investicija - mesecni_vlozki_vsota
    print(f"Torej zaslužili / izgubili smo: {formatiraj_kes(zasluzili)} 🏆")
    print(f"Imamo vse skupaj: {formatiraj_kes(investment_navaden)} EUR 💰✈️🌍")

