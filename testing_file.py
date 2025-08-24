from datetime import datetime
from dateutil.relativedelta import relativedelta
from csv import reader
from csv import reader
from colorama import Fore, Style
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

def primerjaj_dva_indeksa(file1, file2, stolpec=5):
    """
    Primerjava dveh csv file rezultatov. En navaden drug leverage
    Face to face
    """
    
    with open(file1, "r") as f1, open(file2, "r") as f2:
        podatki1 = list(reader(f1))
        podatki2 = list(reader(f2))

    stevec1 = 0
    stevec2 = 0
    print()
    print()
    print("Datum | BOLJŠI (narejen plus/minus, vse skupaj) | razlika | SLABŠI (narejen plus/minus, vse skupaj) ")
    print()

    # preskočimo header (če ga je)
    for i in range(1, min(len(podatki1), len(podatki2))):
        try:
            vrednost1 = float(podatki1[i][stolpec])
            vrednost2 = float(podatki2[i][stolpec])
        except ValueError:
            continue  # preskočimo, če ni številka

        datum = podatki1[i][0]  # ob predpostavki, da imata oba fajla isti datum v 0. stolpcu

        if vrednost1 > vrednost2:
            zmaga_koliko_posto = round(((vrednost1 - vrednost2) / vrednost2) * 100, 2)
            print(
                f"{Fore.YELLOW}{datum}{Style.RESET_ALL} | "
                f"{Fore.MAGENTA}{float(podatki1[i][4]):,.2f}, {float(podatki1[i][5]):,.2f}{Style.RESET_ALL} "
                f">> {Fore.GREEN}+{zmaga_koliko_posto}%{Style.RESET_ALL} >> "
                f"{Fore.BLUE}{float(podatki2[i][4]):,.2f}, {float(podatki2[i][5]):,.2f}{Style.RESET_ALL}")
            stevec1 += 1

        elif vrednost2 > vrednost1:
            zmaga_koliko_posto = round(((vrednost2 - vrednost1) / vrednost1) * 100, 2)
            print(
                f"{Fore.YELLOW}{datum}{Style.RESET_ALL} | "
                f"{Fore.BLUE}{float(podatki2[i][4]):,.2f}, {float(podatki2[i][5]):,.2f}{Style.RESET_ALL} "
                f">> {Fore.GREEN}+{zmaga_koliko_posto}%{Style.RESET_ALL} >> "
                f"{Fore.MAGENTA}{float(podatki1[i][4]):,.2f}, {float(podatki1[i][5]):,.2f}{Style.RESET_ALL}")
            stevec2 += 1

    # povzetek
    print(Fore.MAGENTA + "══════════════════════════════════════════════════════" + Style.RESET_ALL)
    print(Fore.CYAN + f"📊 Direktna primerjava med {file1} in {file2}" + Style.RESET_ALL)
    print()
    print(Fore.CYAN + f"💰 Začetna investicija {podatki1[10][1]} , vse mesečne investicije {podatki1[2][2]}, vse skupaj investirano: {podatki1[10][3]}")
    print()
    print(Fore.CYAN + f"Procenti so izracunani na podlagi 'koliko imamo vse skupaj'")
    print()

    procent_stevec_1 = round((stevec1 / (stevec1 + stevec2 or 1)) * 100, 2)
    procent_stevec_2 = round((stevec2 / (stevec1 + stevec2 or 1)) * 100, 2)

    print(Fore.LIGHTMAGENTA_EX + f"✔ {file1} je bil boljši v {stevec1} primerih ({procent_stevec_1}%)" + Style.RESET_ALL)
    print(Fore.LIGHTBLUE_EX + f"✔ {file2} je bil boljši v {stevec2} primerih ({procent_stevec_2}%)" + Style.RESET_ALL)

    print()
    

    print(Fore.GREEN + "🏆 Najboljši je tisti, ki z največjo vrednostjo v stoplcu 'koliko imamo skupaj' " + Style.RESET_ALL)
    print()
    
    print(Fore.MAGENTA + "══════════════════════════════════════════════════════" + Style.RESET_ALL)

    return stevec1, stevec2







from csv import reader

from csv import reader

def primerjaj_tri_indekse(file1, file2, file3, stolpec=5):
    # --- ANSI RGB helper ---
    def rgb(r, g, b): return f"\033[38;2;{r};{g};{b}m"
    RESET = "\033[0m"

    # Barve (RGB)
    DATE_COLOR = rgb(226, 226, 226)   # datumi (svetlo siva)
    CYAN = rgb(23, 190, 207)
    GREEN = rgb(0, 200, 83)

    FILE1_COLOR = rgb(166, 130, 255)  # file1
    FILE2_COLOR = rgb(85, 193, 255)   # file2
    FILE3_COLOR = rgb(255, 183, 3)    # file3

    # Preberi vse tri datoteke
    with open(file1, "r") as f1, open(file2, "r") as f2, open(file3, "r") as f3:
        podatki1 = list(reader(f1))
        podatki2 = list(reader(f2))
        podatki3 = list(reader(f3))

    wins = {file1: 0, file2: 0, file3: 0}
    ties = 0

    print()
    print("Datum | NAJBOLJSI (narejen plus/minus, vse skupaj)  >>  +%  >>  DRUGI (narejen plus/minus, vse skupaj)  >>  +%  >>  TRETJI (narejen plus/minus, vse skupaj)")
    print()

    rows = min(len(podatki1), len(podatki2), len(podatki3))
    for i in range(1, rows):
        try:
            v1 = float(podatki1[i][stolpec])
            v2 = float(podatki2[i][stolpec])
            v3 = float(podatki3[i][stolpec])

            f1_gain, f1_tot = float(podatki1[i][4]), float(podatki1[i][5])
            f2_gain, f2_tot = float(podatki2[i][4]), float(podatki2[i][5])
            f3_gain, f3_tot = float(podatki3[i][4]), float(podatki3[i][5])
        except (ValueError, IndexError):
            continue

        datum = podatki1[i][0]

        # Priprava za razvrščanje: (naziv, vrednost, obarvan izpis, vrednost)
        candidates = [
            (file1, v1, f"{FILE1_COLOR}{f1_gain:,.2f}, {f1_tot:,.2f}{RESET}", v1),
            (file2, v2, f"{FILE2_COLOR}{f2_gain:,.2f}, {f2_tot:,.2f}{RESET}", v2),
            (file3, v3, f"{FILE3_COLOR}{f3_gain:,.2f}, {f3_tot:,.2f}{RESET}", v3),
        ]

        if v1 == v2 == v3:
            ties += 1
            print(f"{DATE_COLOR}{datum}{RESET} | Vse tri enake (tie)")
            continue

        ordered = sorted(candidates, key=lambda x: x[3], reverse=True)
        (best_name, best_val, best_str, _), (sec_name, sec_val, sec_str, _), (third_name, third_val, third_str, _) = ordered

        def pct_diff(a, b):
            try:
                return f"+{round((a - b) / b * 100, 2)}%"
            except ZeroDivisionError:
                return "+inf%"

        diff_best_sec = pct_diff(best_val, sec_val)
        diff_sec_third = pct_diff(sec_val, third_val)

        print(
            f"{DATE_COLOR}{datum}{RESET} | "
            f"{best_str}  >>  {GREEN}{diff_best_sec}{RESET}  >>  "
            f"{sec_str}  >>  {GREEN}{diff_sec_third}{RESET}  >>  "
            f"{third_str}"
        )

        wins[best_name] += 1

    total_compared = sum(wins.values())

    print(FILE1_COLOR + "══════════════════════════════════════════════════════" + RESET)
    print(CYAN + f"📊 Direktna primerjava med {file1}, {file2} in {file3}" + RESET)
    print()
    print(CYAN + f"💰 Začetna investicija: {podatki1[2][1]}" + RESET)
    print(CYAN + f"📈 Vse mesečne investicije: {podatki1[2][2]}" + RESET)
    print(CYAN + f"💵 Vse skupaj investirano: {podatki1[2][3]}" + RESET)
    print()
    print(CYAN + f"Procenti so izracunani na podlagi 'koliko imamo vse skupaj'" + RESET)
    print()

    for fname, color in [(file1, FILE1_COLOR), (file2, FILE2_COLOR), (file3, FILE3_COLOR)]:
        w = wins[fname]
        pct = round((w / (total_compared or 1)) * 100, 2)
        print(color + f"✔ {fname} je bil najboljši v {w} primerih ({pct}%)" + RESET)

    if ties:
        print(DATE_COLOR + f"⚖ Neodločeno (vsi enaki): {ties}" + RESET)

    print()
    print(GREEN + "🏆 'Najboljši' je tisti z največjo vrednostjo v stolpcu 'koliko imamo vse skupaj'" + RESET)
    print(FILE1_COLOR + "══════════════════════════════════════════════════════" + RESET)

    return wins[file1], wins[file2], wins[file3], ties

