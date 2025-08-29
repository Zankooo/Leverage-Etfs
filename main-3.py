# ti dolocis v katerega prvo investiras
# dolocis koliko mora biti dol osnvoen da kupis 2x ali 3x
# dolocis interval
# in ti spet on izracuna za vsa leta oz intervale

# to bo funkcija ki bo izracunala vse skupaj
# 15 let recimo. ce je osnoven 5% dol kupimo tistega v mesecu 2x, ce 10% kupimo 3x
# to bomo probali kakko bo ker je fact da je fajn kupovat ko je dol cim vecji leverage
from obcasno_pogosti_fajli.csv_operacije import *
from testing_file import *
from izracuni import *
from rich.progress import Progress
import csv
from datetime import datetime
import os
from csv import reader as csv_reader

sp_500 = load_csv('podatki_ustvarjeni/sp-500.csv')
sp_500_2x = load_csv('2x-leverage/sp-500-2x.csv')
sp_500_3x = load_csv('3x-leverage/sp-500-3x.csv')


# -------------------------------------------------------------------------------------
def to_float(x):
    if isinstance(x, (int, float)):
        return float(x)
    s = str(x).replace(",", "").replace(" ", "")
    if s.endswith("%"):
        s = s[:-1]
    return float(s)

# -------------------------------------------------------------------------------------

def investicija(podatki1, podatki2, podatki3, datum_zacetka, datum_konca, 
                zacetna_investicija, mesecna_investicija, koliko_da_kupis_2x, 
                koliko_da_kupis_3x, output_csv_path):
    
    koliko_da_kupis_2x = koliko_da_kupis_2x / 100
    koliko_da_kupis_3x = koliko_da_kupis_3x / 100

    podatki1_daily_changes = izracun_dnevnih_sprememb(podatki1)
    podatki2_daily_changes = izracun_dnevnih_sprememb(podatki2)
    podatki3_daily_changes = izracun_dnevnih_sprememb(podatki3)

   
    vrstica_zacetka = next(i for i, row in enumerate(podatki1) if row[0] == datum_zacetka)
    vrstica_konca   = next(i for i, row in enumerate(podatki1) if row[0] == datum_konca)

    investicija1 = float(zacetna_investicija)
    investicija2 = 0.0
    investicija3 = 0.0

    investirano_v_1x = 0.0
    investirano_v_2x = 0.0
    investirano_v_3x = 0.0

    all_time_high = to_float(podatki1[vrstica_zacetka][1])
    current_month = datetime.strptime(datum_zacetka, "%Y-%m-%d").month

    for i in range(vrstica_zacetka, vrstica_konca + 1):

        cena1 = to_float(podatki1[i][1])
        daily_change_podatki1 = to_float(podatki1_daily_changes[i][2]) / 100.0
        daily_change_podatki2 = to_float(podatki2_daily_changes[i][2]) / 100.0
        daily_change_podatki3 = to_float(podatki3_daily_changes[i][2]) / 100.0

        date = datetime.strptime(podatki1[i][0], "%Y-%m-%d")

        if date.month != current_month:
            if cena1 < (all_time_high * (1.0 - koliko_da_kupis_3x)):
                investicija3 += mesecna_investicija
                investirano_v_3x += mesecna_investicija
            elif cena1 < (all_time_high * (1.0 - koliko_da_kupis_2x)):
                investicija2 += mesecna_investicija
                investirano_v_2x += mesecna_investicija
            else:
                investicija1 += mesecna_investicija
                investirano_v_1x += mesecna_investicija
            current_month = date.month

        if cena1 > all_time_high:
            all_time_high = cena1

        investicija1 *= (1.0 + daily_change_podatki1)
        investicija2 *= (1.0 + daily_change_podatki2)
        investicija3 *= (1.0 + daily_change_podatki3)

    skupno = investicija1 + investicija2 + investicija3
    skupaj_mesecno = investirano_v_1x + investirano_v_2x + investirano_v_3x

    print("----------------")
    print("Datum zacetka:", datum_zacetka, "| Datum konca:", datum_konca)
    print("Končna vrednost skupaj:", round(skupno, 2), "eur")
    print("Skupaj mesečnih vložkov:", round(skupaj_mesecno, 2), "eur")
    print(f"Razbitje mesečnih vložkov -> 1x: {investirano_v_1x}eur | 2x: {investirano_v_2x}eur | 3x: {investirano_v_3x}eur")

    # --- zapis v CSV (3 vrstice po tvojem vzorcu) ---
    
    # --- zapis v CSV ---
    file_exists = os.path.exists(output_csv_path)

    row1 = [
        f"SP500 osnoven more padet {koliko_da_kupis_2x * 100}% da kupimo 2x",
        f"in osnoven more padet {koliko_da_kupis_3x * 100}% da kupimo 3x"
    ]
    # header vrstica
    row2 = ["Datum od kdaj do kdaj", "Zacetna investicija", "vse mesecne investicije",
            "skupaj vse investicije", "koliko smo v plusu oz minusu", "koliko imamo vse skupaj"]

    # izračuni za row3
    skupaj_vlozeno = zacetna_investicija + skupaj_mesecno
    plus_minus = round(skupno - skupaj_vlozeno, 2)
    row3 = [
        f"{datum_zacetka}-{datum_konca}",
        zacetna_investicija,
        round(skupaj_mesecno, 2),
        round(skupaj_vlozeno, 2),
        plus_minus,
        round(skupno, 2)
    ]

    if not file_exists:
        os.makedirs(os.path.dirname(output_csv_path) or ".", exist_ok=True)
        with open(output_csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(row1)
            writer.writerow(row2)
            writer.writerow(row3)
    else:
        with open(output_csv_path, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(row3)

    return skupno

# -------------------------------------------------------------------------------------


def funkcija_naredi_rezultate(zacetna_investicija, mesecne_investicije, interval, koliko_pade_da_2x, koliko_pade_da_3x):
    # izberi unikaten CSV za ta zagon
    output_csv_path = next_results_path(directory=".", base="rezultati", ext=".csv")

    intervali = generiraj_intervale_leto(sp_500, interval)

    with Progress() as progress:
        task = progress.add_task("[magenta]Računam...", total=len(intervali))
        for i in range(len(intervali)):
            investicija(
                sp_500, sp_500_2x, sp_500_3x,
                intervali[i][0], intervali[i][1],
                zacetna_investicija, mesecne_investicije,
                koliko_pade_da_2x, koliko_pade_da_3x,
                output_csv_path=output_csv_path
            )
            progress.advance(task)

    print(f"Ustvarjen file: {output_csv_path}")
    return 0


# -------------------------------------------------------------------------------------

# helper funkcija da ustvari vedno nov csv za zgornji funkciji
def next_results_path(directory=".", base="rezultati", ext=".csv"):
    n = 1
    while True:
        path = os.path.join(directory, f"{base}{n}{ext}")
        if not os.path.exists(path):
            return path
        n += 1


# -------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------


def primerjaj_vec_indeksov(*files, stolpec=5):
    """
    Primerja poljubno število CSV-jev v formatu:
      1. vrstica: opis pragov (poljubno besedilo)
      2. vrstica: header
      3.+ vrstice: podatki v obliki:
         "Datum od kdaj do kdaj,Zacetna investicija,vse mesecne investicije,skupaj vse investicije,koliko smo v plusu oz minusu,koliko imamo vse skupaj"

    :param files: poti do CSV datotek (2 ali več)
    :param stolpec: indeks stolpca, po katerem primerjamo (privzeto 5 = 'koliko imamo vse skupaj')
    :return: (wins_by_file: dict, ties_count: int)
    """

    if len(files) < 2:
        raise ValueError("Potrebujem vsaj 2 CSV datoteki za primerjavo.")

    # --- ANSI RGB helper ---
    def rgb(r, g, b): return f"\033[38;2;{r};{g};{b}m"
    RESET = "\033[0m"

    # Barvna paleta (cikliramo, če je datotek več)
    PALETTE = [
        (166,130,255),  # vijolična
        (85,193,255),   # svetlo modra
        (255,183,3),    # oranžna
        (0,200,83),     # zelena
        (255,99,132),   # rdeča
        (153,102,255),  # vijolična 2
        (54,162,235),   # modra
        (255,206,86),   # rumena
    ]
    DATE_COLOR = rgb(226, 226, 226)
    CYAN = rgb(23, 190, 207)
    GREEN = rgb(0, 200, 83)

    # EU format helper: 12345.67 -> 12.345,67
    def fmt_eu(x, decimals=2):
        try:
            val = float(x)
        except (TypeError, ValueError):
            return str(x)
        s = f"{val:,.{decimals}f}"  # 12,345.67
        return s.replace(",", "X").replace(".", ",").replace("X", ".")

    # Preberi vse tabele
    tables = []
    for fp in files:
        with open(fp, "r", encoding="utf-8") as f:
            tables.append(list(csv_reader(f)))

    # Upoštevamo, da se podatki začnejo od vrstice 2 naprej (0-based index)
    DATA_START = 2

    # Koliko vrstic lahko primerjamo (vzemi minimum po datotekah)
    rows = min(len(t) for t in tables)

    # Pripravi mapping: ime_datoteke -> barva in zmage
    file_colors = {}
    wins = {}
    for idx, fp in enumerate(files):
        r, g, b = PALETTE[idx % len(PALETTE)]
        file_colors[fp] = rgb(r, g, b)
        wins[fp] = 0

    ties = 0

    print()
    print("Datum | NAJBOLJŠI (plus/minus, vse skupaj)  >>  +%  >>  DRUGI  >>  +%  >>  ...  >>  ZADNJI")
    print()

    # Iteriramo po vrsticah s podatki
    for i in range(DATA_START, rows):
        # Zberemo kandidate iz vseh datotek
        candidates = []
        datum = None

        valid_row = True
        for fp, table in zip(files, tables):
            try:
                # Vrednost za rangiranje
                v = float(table[i][stolpec])

                # Dodatni podatki (gain in total) – tukaj:
                gain = float(table[i][4])
                total = float(table[i][5])

                # Datum (vzamemo iz prve tabele, če še ni)
                if datum is None:
                    datum = table[i][0]

                # String za lep obarvan izpis (gain, total)
                c_str = f"{file_colors[fp]}{fmt_eu(gain,2)}, {fmt_eu(total,2)}{RESET}"

                candidates.append((fp, v, c_str, v))
            except (ValueError, IndexError):
                valid_row = False
                break

        if not valid_row or not candidates:
            continue

        # Če so vsi enaki
        all_vals = [c[1] for c in candidates]
        if all(x == all_vals[0] for x in all_vals):
            ties += 1
            print(f"{DATE_COLOR}{datum}{RESET} | Vse enako (tie)")
            continue

        # Razvrsti po vrednosti (desc)
        ordered = sorted(candidates, key=lambda x: x[3], reverse=True)

        # Helper za % razliko
        def pct_diff(a, b):
            try:
                return (a - b) / b * 100.0
            except ZeroDivisionError:
                return float("inf")

        # Sestavimo izpis: najboljši >> +% >> drugi >> +% >> tretji ...
        parts = [f"{DATE_COLOR}{datum}{RESET} | "]
        for j, item in enumerate(ordered):
            name_j, val_j, str_j, _ = item
            parts.append(str_j)
            if j < len(ordered) - 1:
                # % razlika proti naslednjemu
                _, val_next, _, _ = ordered[j+1]
                diff = pct_diff(val_j, val_next)
                parts.append(f"  >>  {GREEN}+{fmt_eu(diff,2)}%{RESET}  >>  ")

        print("".join(parts))

        # Zmaga gre prvemu
        wins[ordered[0][0]] += 1

    total_compared = sum(wins.values())

    # Povzetek (metapodatki iz PRVE datoteke, prve podatkovne vrstice)
    print(rgb(166,130,255) + "══════════════════════════════════════════════════════" + RESET)
    print(CYAN + f"📊 Direktna primerjava med: {', '.join(files)}" + RESET)
    print()

    def safe_fmt(val):
        try:
            return fmt_eu(float(val), 2)
        except (TypeError, ValueError):
            return str(val)

    if len(tables[0]) > DATA_START:
        first_data = tables[0][DATA_START]
        if len(first_data) >= 4:
            print(CYAN + f"💰 Začetna investicija: {safe_fmt(first_data[1])}€" + RESET)
            print(CYAN + f"📈 Vse mesečne investicije: {safe_fmt(first_data[2])}€" + RESET)
            print(CYAN + f"💵 Vse skupaj investirano: {safe_fmt(first_data[3])}€" + RESET)
            print()

    print(CYAN + f"Procenti so izračunani na podlagi 'koliko imamo vse skupaj' (stolpec {stolpec})." + RESET)
    print(GREEN + "🏆 'Najboljši' je tisti z največjo vrednostjo v tem stolpcu." + RESET)
    print()

    for fp in files:
        w = wins[fp]
        pct = (w / (total_compared or 1)) * 100
        w_eu = fmt_eu(w, 0)
        pct_eu = fmt_eu(pct, 2)
        print(file_colors[fp] + f"✔ {fp} je bil najboljši v {w_eu} primerih ({pct_eu}%)" + RESET)

    if ties:
        ties_eu = fmt_eu(ties, 0)
        print(DATE_COLOR + f"⚖ Neodločeno (vsi enaki): {ties_eu}" + RESET)

    print()
    print(rgb(166,130,255) + "══════════════════════════════════════════════════════" + RESET)

    return wins, ties



# ----------------------------------------------------------------------------------------

def naredi():
    zacetna_investicija = int(input("Koliko naj bo zacetna investicija? "))
    mesecna_investicija = int(input("Koliko naj bo mesecna investicija? "))
    interval = int(input("Koliko let naj bo interval? "))
    koliko_pade_da_2x = int(input("Koliko % naj pade osnoven da kupimo 2x? "))
    koliko_pade_da_3x = int(input("Koliko % naj pade osnoven da kupimo 3x? "))
    

    funkcija_naredi_rezultate(zacetna_investicija, mesecna_investicija, interval, koliko_pade_da_2x, koliko_pade_da_3x)
    return 0
# 30000 in  in 400 in 15
# 2,3, pa 3,4 pa 4,5 pa 5,6 pa 6,7 pa 7,8 
# naredi()

primerjaj_vec_indeksov("testing/osnoven.csv", "testing/vzvod-2x.csv", "testing/vzvod-3x.csv", 
               "rezultati1.csv", "rezultati2.csv", "rezultati3.csv", 
               "rezultati4.csv", "rezultati5.csv", "rezultati6.csv")
