from obcasno_pogosti_fajli.data_printer import *
from izracuni import *
from testing_file import *
from obcasno_pogosti_fajli.csv_operacije import *
from obcasno_pogosti_fajli.fancy_zakljucki_programa import *
import pandas as pd
from tqdm import tqdm
from rich.progress import Progress


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


print('----------')



def funkcija_naredi_1x_rezultate(zacetna_investicija, mesecne_investicije, interval, indeks):
    # izracuna intervale
    intervali = generiraj_intervale_leto(indeks, interval)
    print('----------')
    # ta progress je basically v konzoli da je bolj fancy 
    with Progress() as progress:
        task = progress.add_task("[cyan]Računam 1x...", total=len(intervali))
        # for loop za vse datume pac
        for i in range(len(intervali)):
            metoda_dca_za_testing_prilagojena(indeks, zacetna_investicija, mesecne_investicije,intervali[i][0], intervali[i][1], "rezultati-1")
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
            metoda_dca_za_testing_prilagojena(indeks, zacetna_investicija, mesecne_investicije,intervali[i][0], intervali[i][1], "rezultati-2")
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
            metoda_dca_za_testing_prilagojena(indeks, zacetna_investicija, mesecne_investicije,intervali[i][0], intervali[i][1], "rezultati-3")
            progress.advance(task)
    return 0


#---------------------------------------------------------------------------------------------------------------------------------------------------------

def pridobi_indekse():
   print("Izberi indeks:")
   print("1. S&P 500")
   print("2. Nasdaq 100")
   print("3. Nasdaq Composite")

   izbira = input("Vnesi številko (1/2/3): ")

   if izbira == "1":
      indeksi = [sp_500, sp_500_2x, sp_500_3x]
   elif izbira == "2":
      indeksi = [nasdaq_100, nasdaq_100_2x, nasdaq_100_3x]
   elif izbira == "3":
      indeksi = [nasdaq_comp, nasdaq_comp_2x, nasdaq_comp_3x]
   else:
      print("Napačna izbira!")
      indeksi = []
      
   return indeksi


def pridobi_zneske():
    return [
        int(input("Začetna investicija? ")),
        int(input("Mesečne investicije? ")),
        int(input("Dolžina intervalov? "))
    ]
   

def funkcija_naredi_vse(zacetna_investicija,mesecne_investicije, interval, indeksi):
   funkcija_naredi_1x_rezultate(zacetna_investicija, mesecne_investicije, interval, indeksi[0])
   funkcija_naredi_2x_rezultate(zacetna_investicija, mesecne_investicije, interval, indeksi[1])
   funkcija_naredi_3x_rezultate(zacetna_investicija, mesecne_investicije, interval, indeksi[2])
   return 0




# GLAVNE FUNKCIJE KI KLIČEJO USE VSE ZGORAJ
#indeksi = pridobi_indekse()
#zneski = pridobi_zneske()
#funkcija_naredi_vse(zneski[0],zneski[1],zneski[2], indeksi)

print('----------')

#print("Uspešno ustvarjeni CSV-ji v mapi 'testing' ✅ ")


primerjaj_dva_indeksa("testing/rezultati-1.csv", "testing/rezultati-2.csv")
primerjaj_tri_indekse("testing/rezultati-1.csv", "testing/rezultati-2.csv", "testing/rezultati-3.csv")


fancy1()



