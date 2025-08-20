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
    Primerjava treh CSV rezultatov (npr. 1x, 2x, 3x).
    Za vsak datum najde najboljšega po `stolpec` (privzeto 5 = 'koliko imamo vse skupaj'),
    izpiše redosled BEST >> SECOND >> THIRD z % razlikama,
    in na koncu povzame, kolikokrat je zmagal kateri file.
    """

    # Preberi vse tri datoteke
    with open(file1, "r") as f1, open(file2, "r") as f2, open(file3, "r") as f3:
        podatki1 = list(reader(f1))
        podatki2 = list(reader(f2))
        podatki3 = list(reader(f3))

    # Števci zmag
    wins = {file1: 0, file2: 0, file3: 0}
    ties = 0

    print()
    print("Datum | NAJBOLJSI (narejen plus/minus, vse skupaj)  >>  +%  >>  DRUGI (narejen plus/minus, vse skupaj)  >>  +%  >>  TRETJI (narejen plus/minus, vse skupaj)")
    print()

    # Preskočimo header (vrstica 0)
    rows = min(len(podatki1), len(podatki2), len(podatki3))
    for i in range(1, rows):
        try:
            # vrednosti po katerih odločamo (stolpec = 'skupaj vse skupaj')
            v1 = float(podatki1[i][stolpec])
            v2 = float(podatki2[i][stolpec])
            v3 = float(podatki3[i][stolpec])

            # za lep prikaz vzamemo tudi stolpce 4 in 5 (gain, together)
            f1_gain, f1_tot = float(podatki1[i][4]), float(podatki1[i][5])
            f2_gain, f2_tot = float(podatki2[i][4]), float(podatki2[i][5])
            f3_gain, f3_tot = float(podatki3[i][4]), float(podatki3[i][5])

        except (ValueError, IndexError):
            continue

        datum = podatki1[i][0]

        # Priprava za razvrščanje: (naziv, vrednost, barvni_izpis, gain, tot)
        candidates = [
            (file1, v1, f"{Fore.MAGENTA}{f1_gain:,.2f}, {f1_tot:,.2f}{Style.RESET_ALL}", v1),
            (file2, v2, f"{Fore.BLUE}{f2_gain:,.2f}, {f2_tot:,.2f}{Style.RESET_ALL}", v2),
            (file3, v3, f"{Fore.RED}{f3_gain:,.2f}, {f3_tot:,.2f}{Style.RESET_ALL}", v3),
        ]

        # Preveri neodločene (vsi enaki)
        if v1 == v2 == v3:
            ties += 1
            print(f"{Fore.YELLOW}{datum}{Style.RESET_ALL} | "
                  f"{Fore.WHITE}Vse tri enake (tie){Style.RESET_ALL}")
            continue

        # Razvrsti po vrednosti (desc)
        ordered = sorted(candidates, key=lambda x: x[3], reverse=True)
        (best_name, best_val, best_str, _), (sec_name, sec_val, sec_str, _), (third_name, third_val, third_str, _) = ordered

        # % razlika BEST proti SECOND in SECOND proti THIRD
        # (če je imenovalec 0, izpišemo 'inf')
        def pct_diff(a, b):
            try:
                return f"+{round((a - b) / b * 100, 2)}%"
            except ZeroDivisionError:
                return "+inf%"

        diff_best_sec = pct_diff(best_val, sec_val)
        diff_sec_third = pct_diff(sec_val, third_val)

        # Izpis vrstice (barve: datum = rumen; best/sec/third ohranijo lastne barve)
        print(
            f"{Fore.YELLOW}{datum}{Style.RESET_ALL} | "
            f"{best_str}  >>  {Fore.GREEN}{diff_best_sec}{Style.RESET_ALL}  >>  "
            f"{sec_str}  >>  {Fore.GREEN}{diff_sec_third}{Style.RESET_ALL}  >>  "
            f"{third_str}")

        # Zmaga pripada 'best_name'
        wins[best_name] += 1

    # Povzetek
    total_compared = sum(wins.values())
    print(Fore.MAGENTA + "══════════════════════════════════════════════════════" + Style.RESET_ALL)
    print(Fore.CYAN + f"📊 Direktna primerjava med {file1}, {file2} in {file3}" + Style.RESET_ALL)
    print()
    print(Fore.CYAN + f"Procenti so izracunani na podlagi 'koliko imamo vse skupaj'")
    print()
    for fname, color in [(file1, Fore.LIGHTMAGENTA_EX), (file2, Fore.BLUE), (file3, Fore.RED)]:
        w = wins[fname]
        pct = round((w / (total_compared or 1)) * 100, 2)
        print(color + f"✔ {fname} je bil najboljši v {w} primerih ({pct}%)" + Style.RESET_ALL)

    if ties:
        print(Fore.YELLOW + f"⚖ Neodločeno (vsi enaki): {ties}" + Style.RESET_ALL)

    print()
    print(Fore.GREEN + "🏆 'Najboljši' je tisti z največjo vrednostjo v stolpcu 'koliko imamo vse skupaj'" + Style.RESET_ALL)
    print(Fore.MAGENTA + "══════════════════════════════════════════════════════" + Style.RESET_ALL)

    return wins[file1], wins[file2], wins[file3], ties
