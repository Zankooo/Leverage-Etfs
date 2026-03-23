
from izracuni import *
from testing_file import *
from obcasno_pogosti_fajli.csv_operacije import *
from obcasno_pogosti_fajli.fancy_zakljucki_programa import *
from rich.progress import Progress
from colorama import init, Fore, Style
from grafi import  narisi_logaritmicne_grafe
import os
import glob
from pathlib import Path
from rich.progress import Progress  # če še ni uvoženo
init(autoreset=True)



print('----------')

# PREBEREMO PODATKE
sp_500 = load_csv('podatki_ustvarjeni/sp-500.csv')
sp_500_2x = load_csv('2x-leverage/sp-500-2x.csv')
sp_500_3x = load_csv('3x-leverage/sp-500-3x.csv')

nasdaq_100 = load_csv('podatki_ustvarjeni/nasdaq-100.csv')
nasdaq_100_2x = load_csv('2x-leverage/nasdaq-100-2x.csv')
nasdaq_100_3x = load_csv('3x-leverage/nasdaq-100-3x.csv')

nasdaq_comp = load_csv('podatki_ustvarjeni/nasdaq-comp.csv')
nasdaq_comp_2x = load_csv('2x-leverage/nasdaq-comp-2x.csv')
nasdaq_comp_3x = load_csv('3x-leverage/nasdaq-comp-3x.csv')


#---------------------------------------------------------------------------------------------------------------------------------------------------------

# PRIDOBIVANJE PODATKOV - pomozne funkcije, ki jih upoabljamo v glavnima dvema funkcijama!
# Te printi so v veliki meri fancy stvari, če hočemo brez damo chatu in nam odstrani fancy stvari
# in koda bo krajsa, in ostala bo samo funkcionalnost

LINE = "═" * 54

def pridobi_indekse():
    print(Fore.MAGENTA + LINE + Style.RESET_ALL)
    print(Fore.CYAN + "📊 Izberi indeks:" + Style.RESET_ALL)
    print()

    print(Fore.GREEN + "1. S&P 500" + Style.RESET_ALL)
    print(Fore.LIGHTCYAN_EX + "2. Nasdaq 100" + Style.RESET_ALL)
    print(Fore.LIGHTYELLOW_EX + "3. Nasdaq Composite" + Style.RESET_ALL)    
    print()

    izbira = input(Fore.CYAN + "Vnesi številko (1/2/3): " + Style.RESET_ALL)

    if izbira == "1":
        indeksi = [sp_500, sp_500_2x, sp_500_3x]
    elif izbira == "2":
        indeksi = [nasdaq_100, nasdaq_100_2x, nasdaq_100_3x]
    elif izbira == "3":
        indeksi = [nasdaq_comp, nasdaq_comp_2x, nasdaq_comp_3x]
    else:
        print(Fore.YELLOW + "Napačna izbira!" + Style.RESET_ALL)
        indeksi = []

    return indeksi


def pridobi_zneske():
    print(Fore.MAGENTA + LINE + Style.RESET_ALL)
    print(Fore.CYAN + "💰 Vnesi zneske" + Style.RESET_ALL)
    print()

    zacetna = int(input(Fore.CYAN + "Začetna investicija? " + Style.RESET_ALL))
    mesecne = int(input(Fore.CYAN + "Mesečne investicije? " + Style.RESET_ALL))
    dolzina = int(input(Fore.CYAN + "Dolžina intervalov? " + Style.RESET_ALL))

    print(Fore.MAGENTA + LINE + Style.RESET_ALL)
    return [zacetna, mesecne, dolzina]


#---------------------------------------------------------------------------------------------------------------------------------------------------------
# GLAVNI FUNKCIJI

# tukaj se pa zacne glavni del te nase famozne funkcije

# to smo dali ven iz funkcije ker pac potrebujemo to v dveh funkcijah (prvi in drugi) in drugace ne gre


# 1. GLAVNA FUNKCIJA - ustvari csvje 
def funkcija_naredi_rezultat_za_csvje():
    # rezultate shranjujemo v mapo: 'rezultati-vsak-interval-vsi-indeksi'
    # ce se ni ustvarjena mapa jo ustvarimo
    folder = "rezultati-vsak-interval-vsi-indeksi"
    os.makedirs(folder, exist_ok=True)  # Ustvari mapo (če še ne obstaja)

    # da pripravimo prostor da nove fajle damo notri moremo prej use zbrisat. to naredi pa ta koda
    for csv_file in glob.glob(os.path.join(folder, "*.csv")):  # 🔍 Najdi vse CSV datoteke
        os.remove(csv_file)

    # izračuna intervale -> na podlagi osnovnega indeksa.. pac itak bodo imeli vsi iste intervale 
    # in iste datume imajo.. teoreticno bi lahko tudi dali ker kol indeksi[1] ali indeksi[2]
    intervali = generiraj_intervale_leto(indeksi[0], zneski[2])

    with Progress() as progress:
        task = progress.add_task("[cyan]Računam...", total=len(intervali))
        # števec začnemo pri 1, da bo ...1.csv, ...2.csv, ...
        stevec = 1
        for i in range(len(intervali)):
            output_file = f"rezultati-vsak-interval-vsi-indeksi/rezultati_investicije{stevec}.csv"
            # ker v for loopu klicemo je to zato ker za razlicne intervale
            izracun_dca_metoda_prilagojena_da_naredi_csv(
                indeksi[0], indeksi[1], indeksi[2],
                initial_investment = zneski[0],
                monthly_investment = zneski[1],
                datum_zacetka = intervali[i][0],
                datum_konca = intervali[i][1],
                output_file = output_file
            )
            stevec = stevec + 1
            progress.advance(task)
    return 0

# ------

# 2. GLAVNA FUNKCIJA - funkcija ki narise grafe iz vseh csvjev v mapi: 'rezultati-vsak-interval-vsi-indeksi'
def funkcija_ki_narise_grafe(zacetna_investicija, mesecna_investicija, cela_investicija_skupaj):
    print()
    # usvarimo mapo ce se ne obstaja
    folder = Path('mapa-grafi')
    folder.mkdir(parents=True, exist_ok=True)
    # če obstaja, izbriši vse .csv datoteke v njej da pripravimo za nove grafe.html
    for csv_file in folder.glob("*.csv"):
        csv_file.unlink()

    # preštej csv-je v mapi, da vemo koliko dolg for loop
    mapa = Path("rezultati-vsak-interval-vsi-indeksi")
    stevilo_csvjev = len(list(mapa.glob("*.csv")))

    # tukaj dodaj da ustvari mapo ce se ne obstaja... 
    # ce pa ze obstaja pa iz nje vse odstrani
    for i in range(1, stevilo_csvjev + 1):
        pot = f"rezultati-vsak-interval-vsi-indeksi/rezultati_investicije{i}.csv"
        narisi_logaritmicne_grafe(
            zacetna_investicija,
            mesecna_investicija,
            cela_investicija_skupaj,
            pot,
            f'mapa-grafi/graf{i}.html'
        )
    
    
# ---------------------------------------------------------------------------------------------

# POKLICEMO TO KAR JE TUKAJ IN JE TO TO

# to rabimo ker te podatke uporabljata obe glavni funkciji
indeksi = pridobi_indekse()

zneski = pridobi_zneske()
# zacetna investicija
zacetna_investicija = int(zneski[0])
# mesecne investicije
mesecna_investicija = int(zneski[1])
# interval, recimo 10
interval = int(zneski[2])

cela_investicija_skupaj = zacetna_investicija + 12 * interval * mesecna_investicija


funkcija_naredi_rezultat_za_csvje()
funkcija_ki_narise_grafe(zacetna_investicija, mesecna_investicija, cela_investicija_skupaj)



fancy_zakljucek_1()




