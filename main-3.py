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


sp_500 = load_csv('podatki_ustvarjeni/sp-500.csv')
sp_500_2x = load_csv('2x-leverage/sp-500-2x.csv')
sp_500_3x = load_csv('3x-leverage/sp-500-3x.csv')

# prvo ta funkcija, ki jo bomo klicali v for loopu za vse intervale
# pol pa funkcija ki bo primerjala use in izpisala
# datume dobis iz funkcijo naredi intervale
from datetime import datetime



import csv
from datetime import datetime

def to_float(x):
    if isinstance(x, (int, float)):
        return float(x)
    s = str(x).replace(",", "").replace(" ", "")
    if s.endswith("%"):
        s = s[:-1]
    return float(s)


def investicija(podatki1, podatki2, podatki3, datum_zacetka, datum_konca, 
                zacetna_investicija, mesecna_investicija, koliko_da_kupis_2x, 
                koliko_da_kupis_3x, output_csv_path="rezultatiii.csv"):
    
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
    
    row0 = [f"Zacetna investicija {zacetna_investicija}, vseh mesecnih {skupaj_mesecno}"]
    row1 = [
    f"SP500 osnoven more padet {koliko_da_kupis_2x * 100}% da kupimo 2x",
    f"in osnoven more padet {koliko_da_kupis_3x * 100}% da kupimo 3x"
    ]
    row2 = ["Datum", "Skupno (eur)"]
    row3 = [f"{datum_zacetka}-{datum_konca}", f"{round(skupno, 2)}"]

    file_exists = os.path.exists(output_csv_path)

    # če ne obstaja -> ustvari in zapiši row1, row2, row3
    if not file_exists:
        # poskrbi, da mapa obstaja (opcijsko)
        os.makedirs(os.path.dirname(output_csv_path) or ".", exist_ok=True)
        with open(output_csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(row1)
            writer.writerow(row0)
            writer.writerow(row2)
            writer.writerow(row3)
    # če csv ze obstajaobstaja -> dodaj le row3
    else:
        with open(output_csv_path, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(row3)

    return skupno




def funkcija_naredi_rezultate(zacetna_investicija, mesecne_investicije, interval):
    # izracuna intervale
    intervali = generiraj_intervale_leto(sp_500, interval)
    # ta progress je basically v konzoli da je bolj fancy 
    with Progress() as progress:
        task = progress.add_task("[magenta]Računam...", total=len(intervali))
        # for loop za vse datume pac
        for i in range(len(intervali)):
            investicija(sp_500, sp_500_2x, sp_500_3x, intervali[i][0], intervali[i][1], 
                        zacetna_investicija, mesecne_investicije, koliko_pade_da_2x, koliko_pade_da_3x)
            progress.advance(task)
    
    print("Ustvarjen fiel rezultatiii.csv !")
    return 0


zacetna_investicija = int(input("Koliko naj bo zacetna investicija? "))
mesecna_investicija = int(input("Koliko naj bo mesecna investicija? "))
koliko_pade_da_2x = int(input("Koliko % naj pade osnoven da kupimo 2x? "))
koliko_pade_da_3x = int(input("Koliko % naj pade osnoven da kupimo 3x? "))







interval = int(input("Koliko let naj bo interval? "))


funkcija_naredi_rezultate(zacetna_investicija, mesecna_investicija, interval)
