
from izracuni import *
from testing_file import *
from obcasno_pogosti_fajli.csv_operacije import *
from obcasno_pogosti_fajli.fancy_zakljucki_programa import *
from rich.progress import Progress
from colorama import init, Fore, Style
import os
import glob
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


def funkcija_naredi_1x_rezultate(zacetna_investicija, mesecne_investicije, interval, indeks):
    # izracuna intervale
    intervali = generiraj_intervale_leto(indeks, interval)
    # ta progress je basically v konzoli da je bolj fancy 
    with Progress() as progress:
        task = progress.add_task("[cyan]Računam 1x...", total=len(intervali))
        # for loop za vse datume pac
        for i in range(len(intervali)):
            metoda_dca_za_testing_prilagojena(indeks, zacetna_investicija, mesecne_investicije,intervali[i][0], intervali[i][1], "osnoven")
            progress.advance(task)
    return 0

def funkcija_naredi_2x_rezultate(zacetna_investicija, mesecne_investicije, interval, indeks):
    # izracuna intervale
    intervali = generiraj_intervale_leto(indeks, interval)
    # ta progress je basically v konzoli da je bolj fancy 
    with Progress() as progress:
        task = progress.add_task("[magenta]Računam 2x...", total=len(intervali))
        # for loop za vse datume pac
        for i in range(len(intervali)):
            metoda_dca_za_testing_prilagojena(indeks, zacetna_investicija, mesecne_investicije,intervali[i][0], intervali[i][1], "vzvod-2x")
            progress.advance(task)
    return 0

def funkcija_naredi_3x_rezultate(zacetna_investicija, mesecne_investicije, interval, indeks):
    # izracuna intervale
    intervali = generiraj_intervale_leto(indeks, interval)
    # ta progress je basically v konzoli da je bolj fancy 
    with Progress() as progress:
        task = progress.add_task("[orange1]Računam 3x...", total=len(intervali))
        # for loop za vse datume pac
        for i in range(len(intervali)):
            metoda_dca_za_testing_prilagojena(indeks, zacetna_investicija, mesecne_investicije,intervali[i][0], intervali[i][1], "vzvod-3x")
            progress.advance(task)
    return 0


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



def funkcija_naredi_vse(zacetna_investicija,mesecne_investicije, interval, indeksi):
    # preverimo ce so od prejsnega zagona programa ze kaksne datoteke v testing mapi, 
    # in ce so jih izbrisemo, da ustvarimo prostor da se ustvarijo nove -> brez tega filtra moramo sami zbrisat rocno
    test_files = glob.glob('testing/*.csv')
    if test_files:
        for file in test_files:
            os.remove(file)

    funkcija_naredi_1x_rezultate(zacetna_investicija, mesecne_investicije, interval, indeksi[0])
    funkcija_naredi_2x_rezultate(zacetna_investicija, mesecne_investicije, interval, indeksi[1])
    funkcija_naredi_3x_rezultate(zacetna_investicija, mesecne_investicije, interval, indeksi[2])
    return 0



#---------------------------------------------------------------------------------------------------------------------------------------------------------
# GLAVNE FUNKCIJE KI KLIČEJO USE VSE ZGORAJ
indeksi = pridobi_indekse()
zneski = pridobi_zneske()
funkcija_naredi_vse(zneski[0],zneski[1],zneski[2], indeksi)


print('----------')


print("Uspešno ustvarjeni CSV-ji v mapi 'testing' ✅ ")


#primerjaj_dva_indeksa("testing/rezultati-1.csv", "testing/rezultati-2.csv")
primerjaj_tri_indekse("testing/osnoven.csv", "testing/vzvod-2x.csv", "testing/vzvod-3x.csv")





# CILJ JE NAREDITI WEB APP IN DA POTEM V WEBAPPU DOLOCIS PARAMETRE 
# IN TI IZPISE TAKO KOT TI TUKAJ IZPISE KATER JE BIL BOLJSI
# AMPAK DA TI LAHKO KLIKNES SE NA VRSTICO IN TI POKAZE GRAF VSEH TREH KAKO JE POTEKAL




fancy1()




