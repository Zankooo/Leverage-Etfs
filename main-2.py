
from izracuni import *
from testing_file import *
from obcasno_pogosti_fajli.csv_operacije import *
from obcasno_pogosti_fajli.fancy_zakljucki_programa import *
from rich.progress import Progress
from colorama import init, Fore, Style
import os
import glob
from rich.progress import Progress  # če še ni uvoženo
init(autoreset=True)



print('----------')

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

# PRIDOBIVANJE PODATKOV 
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

#---------------------------------------------------------------------------------------------------------------------------------------------------------
# GLAVNE FUNKCIJE KI KLIČEJO USE VSE ZGORAJ
#indeksi = pridobi_indekse()
#zneski = pridobi_zneske()
#funkcija_naredi_vse(zneski[0],zneski[1],zneski[2], indeksi)


#primerjaj_dva_indeksa("testing/rezultati-1.csv", "testing/rezultati-2.csv")
#primerjaj_tri_indekse("testing/osnoven.csv", "testing/vzvod-2x.csv", "testing/vzvod-3x.csv")

# izracun_dca_metoda(sp_500_3x)



#---------------------------------------------------------------------------------------------------------------------------------------------------------
# GLAVNE FUNKCIJE KI KLIČEJO USE VSE ZGORAJ





def funkcija_naredi_rezultat_za_csvje():
    # na zacetku; ce so od prej fajli, jih zbrise da je plac za nove
    test_files = glob.glob('rezultati-vsak-interval-vsi-indeksi/*.csv')
    if test_files:
        for file in test_files:
            os.remove(file)

    # indeksi[0] = osnoven indeks, indeksi[1] = 2x indeks, indeksi[2] = 3x indeks
    indeksi = pridobi_indekse()
    #zneski[0] = zacetna investicija, zneski[1] = mesecne investicije, zneski[2] = dolzina intervala, 
    zneski = pridobi_zneske()

    # izračuna intervale -> na podlagi osnovnega indeksa.. pac itak bodo imeli vsi iste intervale 
    # in iste datume imajo.. teoreticno bi lahko tudi dali ker kol indeksi[1] ali indeksi[2]
    intervali = generiraj_intervale_leto(indeksi[0], zneski[2])

    with Progress() as progress:
        task = progress.add_task("[cyan]Računam 1x...", total=len(intervali))
        # števec začnemo pri 1, da bo ...1.csv, ...2.csv, ...
        stevec = 1
        for i in range(len(intervali)):
            output_file = f"rezultati-vsak-interval-vsi-indeksi/rezultati_investicije{stevec}.csv"

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



def funkcija_zbrisi_kar_je_v_mapi():
    test_files = glob.glob('rezultati-vsak-interval-vsi-indeksi/*.csv')
    if test_files:
        for file in test_files:
            os.remove(file)


funkcija_zbrisi_kar_je_v_mapi()

#funkcija_naredi_rezultat_za_csvje()
# izracun_dca_metoda_prilagojena_da_naredi_csv(nasdaq_100,nasdaq_100_2x,nasdaq_100_3x, 1000,100)









# CILJ JE NAREDITI WEB APP IN DA POTEM V WEBAPPU DOLOCIS PARAMETRE 
# IN TI IZPISE TAKO KOT TI TUKAJ IZPISE KATER JE BIL BOLJSI
# AMPAK DA TI LAHKO KLIKNES SE NA VRSTICO IN TI POKAZE GRAF VSEH TREH KAKO JE POTEKAL


# v enem csv file moram imeti 
# od tega leta pa do tega, koliko imamo pri 1x, koliko imamo pri 2x, koliko imamo pri 3x
# datumi, tecaj, tecaj, tecaj
# in iz tega pol narisemo grafe


fancy1()




