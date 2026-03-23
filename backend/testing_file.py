from datetime import datetime
from dateutil.relativedelta import relativedelta
from csv import reader
from colorama import Fore, Style

def generiraj_intervale_leto(podatki, dolzina_intervala_let):
    """
    Funkcija generira intervale za izbrano število let
    Da nato lahko naredimo testing na teh datumih 
    :param podatki: List of lists (dogovorjen format, prve 2 vrstice sta naslova): 
    Nasdaq-composite, 1971-2025
    Date, Close-price
    1971-02-05,100.000
    1971-02-08,100.840
    1971-02-09,100.760
    :param dolzina_intervala_let: int, dolžina intervala v letih
    :return: list of lists [[zacetni_datum, koncni_datum], ...]: 
    [
    ['1962-01-02', '1967-01-03']
    ['1963-01-02', '1968-01-02']
    ['1964-01-02', '1969-01-02']
    ['1965-01-04', '1970-01-05']
    ['1966-01-03', '1971-01-04']
    ['1967-01-03', '1972-01-03']
    ['1968-01-02', '1973-01-02']
    ['1969-01-02', '1974-01-02']
    ['1970-01-02', '1975-01-02']
    ['1971-01-04', '1976-01-05']
    ['1972-01-03', '1977-01-03']
    ]
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




def primerjaj_tri_indekse(file1, file2, file3, stolpec=5):
    """
    Tak format csvja more bit
    vzvod-3x.csv
    "Datum od kdaj do kdaj,Zacetna investicija,vse mesecne investicije,skupaj vse investicije,koliko smo v plusu oz minusu,koliko imamo vse skupaj"
    "1927-12-30-2022-12-30,1000,114000,115000,1400258538.15,1400373538.148123"
    "1928-01-03-2023-01-03,1000,114000,115000,1383427739.07,1383542739.0715628"

    :param file1: csv osnoven
    :param file2: csv 2x leverage
    :param file3: csv 3x leverage

    :return: nic pametnega ne returna le izpise kater je bil boljsi v katerem intervalu in primerjava
    """
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

    # EU format helper: 12345.67 -> 12.345,67
    def fmt_eu(x, decimals=2):
        try:
            val = float(x)
        except (TypeError, ValueError):
            return str(x)
        s = f"{val:,.{decimals}f}"  # 12,345.67
        return s.replace(",", "X").replace(".", ",").replace("X", ".")

    # EU percent helper s predznakom: +12,34% ali -5,67%
    def fmt_pct_eu(x, decimals=2):
        try:
            val = float(x)
        except (TypeError, ValueError):
            return str(x)
        sign = "+" if val >= 0 else "-"
        return f"{sign}{fmt_eu(abs(val), decimals)}%"

    # Preberi vse tri datoteke
    with open(file1, "r") as f1, open(file2, "r") as f2, open(file3, "r") as f3:
        podatki1 = list(reader(f1))
        podatki2 = list(reader(f2))
        podatki3 = list(reader(f3))

    wins = {file1: 0, file2: 0, file3: 0}
    ties = 0

    print()
    print("Datum | NAJBOLJŠI (narejen plus/minus, vse skupaj)  >>  +%  >>  DRUGI (narejen plus/minus, vse skupaj)  >>  +%  >>  TRETJI (narejen plus/minus, vse skupaj)")
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

        # Obarvani EU izpisi (gain, total)
        c1_str = f"{FILE1_COLOR}{fmt_eu(f1_gain,2)}, {fmt_eu(f1_tot,2)}{RESET}"
        c2_str = f"{FILE2_COLOR}{fmt_eu(f2_gain,2)}, {fmt_eu(f2_tot,2)}{RESET}"
        c3_str = f"{FILE3_COLOR}{fmt_eu(f3_gain,2)}, {fmt_eu(f3_tot,2)}{RESET}"

        candidates = [
            (file1, v1, c1_str, v1),
            (file2, v2, c2_str, v2),
            (file3, v3, c3_str, v3),
        ]

        if v1 == v2 == v3:
            ties += 1
            print(f"{DATE_COLOR}{datum}{RESET} | Vse tri enake (tie)")
            continue

        ordered = sorted(candidates, key=lambda x: x[3], reverse=True)
        (best_name, best_val, best_str, _), (sec_name, sec_val, sec_str, _), (third_name, third_val, third_str, _) = ordered

        def pct_diff(a, b):
            try:
                return fmt_pct_eu((a - b) / b * 100, 2)
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

    # Povzetek: preberi in formatiraj v EU (če ni številka, izpiši surovo)
    def safe_fmt(val):
        try:
            return fmt_eu(float(val), 2)
        except (TypeError, ValueError):
            return str(val)

    print(CYAN + f"💰 Začetna investicija: {safe_fmt(podatki1[2][1])}$" + RESET)
    print(CYAN + f"📈 Vse mesečne investicije: {safe_fmt(podatki1[2][2])}$" + RESET)
    print(CYAN + f"💵 Vse skupaj investirano: {safe_fmt(podatki1[2][3])}$" + RESET)
    print()
    print(CYAN + f"Procenti so izračunani na podlagi 'koliko imamo vse skupaj'" + RESET)
    print()
    print(GREEN + "🏆 'Najboljši' je tisti z največjo vrednostjo v stolpcu 'koliko imamo vse skupaj'" + RESET)
    print()

    for fname, color in [(file1, FILE1_COLOR), (file2, FILE2_COLOR), (file3, FILE3_COLOR)]:
        w = wins[fname]
        pct = (w / (total_compared or 1)) * 100
        # EU integer za število primerov, EU percent za odstotek
        w_eu = fmt_eu(w, 0)
        pct_eu = fmt_eu(pct, 2)
        print(color + f"✔ {fname} je bil najboljši v {w_eu} primerih ({pct_eu}%)" + RESET)

    if ties:
        ties_eu = fmt_eu(ties, 0)
        print(DATE_COLOR + f"⚖ Neodločeno (vsi enaki): {ties_eu}" + RESET)

    print()
    print(FILE1_COLOR + "══════════════════════════════════════════════════════" + RESET)

    return wins[file1], wins[file2], wins[file3], ties

