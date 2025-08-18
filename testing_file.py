from datetime import datetime
from dateutil.relativedelta import relativedelta
from csv import reader
from csv import reader
from colorama import Fore, Style


def generiraj_intervale_leto(podatki, dolzina_intervala_let):
    """
    Funkcija generira intervale za izbrano število let
    Da nato lahko naredimo testing na teh datumih 
    :param podatki: List of lists (dogovorjen format, prve 2 vrstice sta naslova)
    :param dolzina_intervala_let: int, dolžina intervala v letih
    :return: list of lists [[zacetni_datum, koncni_datum], ...]
    """
    # Preskoči naslovne vrstice
    podatki = podatki[2:]

    # Pretvori v datetime in poišči prvi datum v vsakem letu
    datumi = [datetime.strptime(row[0], "%Y-%m-%d") for row in podatki]
    prvi_v_letu = {}
    for d in datumi:
        if d.year not in prvi_v_letu:
            prvi_v_letu[d.year] = d

    # Naredi intervale
    intervali = []
    leta = sorted(prvi_v_letu.keys())
    for leto in leta:
        start_date = prvi_v_letu[leto]
        konec_date = start_date + relativedelta(years=dolzina_intervala_let)

        # Poišči prvi datum >= konec_date
        konec = next((d for d in datumi if d >= konec_date), None)
        if konec:
            intervali.append([start_date.strftime("%Y-%m-%d"), konec.strftime("%Y-%m-%d")])

    return intervali

def primerjaj_stolpec(file1, file2, stolpec=5):
    """
    Primerjava dveh csv file rezultatov. En navaden drug leverage
    Face to face
    
    :param file1: ime prve CSV datoteke
    :param file2: ime druge CSV datoteke
    :param stolpec: indeks stolpca za primerjavo (privzeto 5)
    :return: (stevec1, stevec2)
    """
    with open(file1, "r") as f1, open(file2, "r") as f2:
        podatki1 = list(reader(f1))
        podatki2 = list(reader(f2))

    stevec1 = 0
    stevec2 = 0
    print()
    print()
    print("Datum od kdaj do kdaj, koliko smo v plusu oz minusu, koliko imamo vse skupaj")
    print()

    # dodat: Zacetna investicija, vse mesecne investicije, skupaj vse invesiticije

    # preskočimo header (če ga je)
    for i in range(1, min(len(podatki1), len(podatki2))):
        try:
            vrednost1 = float(podatki1[i][stolpec])
            vrednost2 = float(podatki2[i][stolpec])
        except ValueError:
            continue  # preskočimo, če ni številka

        if vrednost1 > vrednost2:
            zmaga_koliko_posto = round(((vrednost1 - vrednost2) / vrednost2) * 100, 2)
            # izpisemo samo; datum, koliko smo v plusu oz minusu, in koliko imamo skupaj
            # to pa zato ker drugace je prevec izpisanega
            print(
            f"\033[95m{podatki1[i][0]}, {float(podatki1[i][4]):,.2f}, {float(podatki1[i][5]):,.2f}\033[0m",
            f"- zmaga za: {zmaga_koliko_posto}%",
            f"\033[94m{podatki2[i][0]}, {float(podatki2[i][4]):,.2f}, {float(podatki2[i][5]):,.2f}\033[0m")
            stevec1 += 1
            print()

        elif vrednost2 > vrednost1:
            zmaga_koliko_posto = round(((vrednost2 - vrednost1) / vrednost1) * 100, 2)
            # izpisemo samo; datum, koliko smo v plusu oz minusu, in koliko imamo skupaj
            # to pa zato ker drugace je prevec izpisanega
            print(
            f"\033[94m{podatki2[i][0]}, {float(podatki2[i][4]):,.2f}, {float(podatki2[i][5]):,.2f}\033[0m "
            f"- zmaga za: {zmaga_koliko_posto}% - "
            f"\033[95m{podatki1[i][0]}, {float(podatki1[i][4]):,.2f}, {float(podatki1[i][5]):,.2f}\033[0m")
            stevec2 += 1
            print()


    print(Fore.MAGENTA + "══════════════════════════════════════════════════════" + Style.RESET_ALL)
    print(Fore.CYAN + f"📊 Direktna primerjava med {file1} in {file2}" + Style.RESET_ALL)
    print(Fore.LIGHTBLACK_EX + "Na levi ➜ boljši v obdobju | Na desni ➜ slabši" + Style.RESET_ALL)
    print()
    print(Fore.YELLOW + f"💰 Začetna investicija: {podatki1[5][1]}" + Style.RESET_ALL)
    print(Fore.YELLOW + f"📈 Mesečne investicije: {podatki1[5][2]}" + Style.RESET_ALL)
    print(Fore.YELLOW + f"💵 Skupno investirano: {podatki1[5][3]}" + Style.RESET_ALL)
    print(Fore.MAGENTA + "══════════════════════════════════════════════════════" + Style.RESET_ALL)

    print()
    print(Fore.LIGHTMAGENTA_EX + f"✔ {file1} je bil boljši v {stevec1} primerih" + Style.RESET_ALL)
    print(Fore.LIGHTBLUE_EX + f"✔ {file2} je bil boljši v {stevec2} primerih" + Style.RESET_ALL)

    print()
    procent_stevec_1 = round((stevec1 / (stevec1 + stevec2)) * 100, 2)
    procent_stevec_2 = round((stevec2 / (stevec1 + stevec2)) * 100, 2)

    print(Fore.GREEN + "🏆 Zmaga tisti, ki ima več na podlagi zadnjega parametra – 'koliko imamo skupaj'" + Style.RESET_ALL)
    print()
    print(Fore.GREEN + f"👉 V {procent_stevec_1}% primerov je bil boljši {file1}" + Style.RESET_ALL)
    print(Fore.GREEN + f"👉 V {procent_stevec_2}% primerov je bil boljši {file2}" + Style.RESET_ALL)
    print(Fore.MAGENTA + "══════════════════════════════════════════════════════" + Style.RESET_ALL)


    return stevec1, stevec2
