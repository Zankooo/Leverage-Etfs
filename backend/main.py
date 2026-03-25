
from izracuni import *
from testing_file import *
from obcasno_pogosti_fajli.csv_operacije import *
from obcasno_pogosti_fajli.fancy_zakljucki_programa import *
from rich.progress import Progress
from colorama import init, Fore, Style
import os
import glob
init(autoreset=True)
from fastapi.responses import JSONResponse
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Obvezno za frontend dostop
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# UPLOAD PODATKOV DA JIH PREBEREMO
sp_500 = load_csv('podatki_ustvarjeni/sp-500.csv')
sp_500_2x = load_csv('2x-leverage/sp-500-2x.csv')
sp_500_3x = load_csv('3x-leverage/sp-500-3x.csv')

nasdaq_100 = load_csv('podatki_ustvarjeni/nasdaq-100.csv')
nasdaq_100_2x = load_csv('2x-leverage/nasdaq-100-2x.csv')
nasdaq_100_3x = load_csv('3x-leverage/nasdaq-100-3x.csv')

nasdaq_comp = load_csv('podatki_ustvarjeni/nasdaq-comp.csv')
nasdaq_comp_2x = load_csv('2x-leverage/nasdaq-comp-2x.csv')
nasdaq_comp_3x = load_csv('3x-leverage/nasdaq-comp-3x.csv')


# probna funkcija če dela vse skup
@app.get("/")
def root():
    # dobit moramo json pravih podatkov in nazaj posljemo tudi nek json
    return {"message": "API deluje"}

#------------------------------------------------------

# -----------------------------------------------------
class UserInput(BaseModel):
    zacetna_investicija: int
    mesecni_vlozek: int
    indeks : str
    interval : int
@app.post("/parametri")
def root(data: UserInput):
    keri_indeksi = pridobi_indekse(data.indeks)
    funkcija_naredi_vse(
        data.zacetna_investicija,
        data.mesecni_vlozek,
        data.interval,
        keri_indeksi
        )
    print('----------')

    print("Uspešno ustvarjeni CSV-ji v mapi 'testing' ✅ ")

    # funkcija 'funkcija_naredi_vse' naredi csv fajle, da jih ta funkcija lahko prejme in naredi primerjavo
    odgovor = primerjaj_tri_indekse("testing/osnoven.csv", "testing/vzvod-2x.csv", "testing/vzvod-3x.csv")

    fancy_zakljucek_1()


    return odgovor
    
# ------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------------
# PRIDOBIVANJE PODATKOV - pomozne funkcije, ki jih rabimo
# Te printi so v veliki meri fancy stvari, če hočemo brez damo chatu in nam odstrani fancy stvari
# in koda bo krajsa, in ostala bo samo funkcionalnost

def pridobi_indekse(izbran_indeks):
    if  izbran_indeks== "S&P 500":
        indeksi = [sp_500, sp_500_2x, sp_500_3x]
    elif izbran_indeks == "Nasdaq 100":
        indeksi = [nasdaq_100, nasdaq_100_2x, nasdaq_100_3x]
    elif izbran_indeks == "Nasdaq Composite":
        indeksi = [nasdaq_comp, nasdaq_comp_2x, nasdaq_comp_3x]
    
    return indeksi


#---------------------------------------------------------------------------------------------------------------------------------------------------------
# GLAVNE TRI FUNKCIJE
def funkcija_naredi_1x_rezultate(zacetna_investicija, mesecne_investicije, interval, indeks):
    # izracuna intervale
    intervali = generiraj_intervale_leto(indeks, interval)
    # ta progress je basically v konzoli da je bolj fancy 
    with Progress() as progress:
        print()
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

#---------------------------------------------------------------------------------------------------------------------------------------------------------
#FUNKCIJA KI KLICE UNE TRI ZGORAJ
def funkcija_naredi_vse(zacetna_investicija, mesecne_investicije, interval, indeksi):
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



