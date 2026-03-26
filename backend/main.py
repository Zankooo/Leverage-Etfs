from izracuni import *
from testing_file import *
from obcasno_pogosti_fajli.csv_operacije import *
from obcasno_pogosti_fajli.fancy_zakljucki_programa import *
from rich.progress import Progress
from colorama import init
import os
import glob
init(autoreset=True)
from fastapi.responses import JSONResponse
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path
from grafi import  narisi_logaritmicne_grafe

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
class podatki_iz_frontenda(BaseModel):
    zacetna_investicija: int
    mesecni_vlozek: int
    indeks : str
    interval : int

@app.post("/primerjava_vrstic")
def root(data: podatki_iz_frontenda):
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
    return odgovor
    # ------------------------------
    # to zgoraj je ex main.py
    # to spodaj je pa zdej ex main-2.py
@app.post("/html-files")
def root(data: podatki_iz_frontenda):
    keri_indeksi = pridobi_indekse(data.indeks)
    cela_investicija_skupaj = data.zacetna_investicija + data.interval * 12 * data.mesecni_vlozek


    funkcija_naredi_rezultat_za_csvje(keri_indeksi, data.interval, data.zacetna_investicija, data.mesecni_vlozek)
    funkcija_ki_narise_grafe(data.zacetna_investicija, data.mesecni_vlozek, cela_investicija_skupaj)

    def dobi_grafe():
        mapa = "mapa-grafi"

        files = sorted(
            [f for f in os.listdir(mapa) if f.endswith(".html")]
        )

        results = []
        for i, file_name in enumerate(files, start=1):
            results.append({
                "id": i,
                "title": file_name,
                "content": f"http://localhost:8000/mapa-grafi/{file_name}"
            })

        return {
            "results": results
        }

    fancy_zakljucek_1()

    # vse htmlje
    return 0
    
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



# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------









def funkcija_naredi_rezultat_za_csvje(keri_indeksi, interval, zacetna_investicija, mesecni_vlozki):
    # rezultate shranjujemo v mapo: 'rezultati-vsak-interval-vsi-indeksi'
    # ce se ni ustvarjena mapa jo ustvarimo
    folder = "rezultati-vsak-interval-vsi-indeksi"
    os.makedirs(folder, exist_ok=True)  # Ustvari mapo (če še ne obstaja)

    # da pripravimo prostor da nove fajle damo notri moremo prej use zbrisat. to naredi pa ta koda
    for csv_file in glob.glob(os.path.join(folder, "*.csv")):  # 🔍 Najdi vse CSV datoteke
        os.remove(csv_file)

    # izračuna intervale -> na podlagi osnovnega indeksa.. pac itak bodo imeli vsi iste intervale 
    # in iste datume imajo.. teoreticno bi lahko tudi dali ker kol indeksi[1] ali indeksi[2]
    intervali = generiraj_intervale_leto(keri_indeksi[0], interval)

    with Progress() as progress:
        task = progress.add_task("[cyan]Računam...", total=len(intervali))
        # števec začnemo pri 1, da bo ...1.csv, ...2.csv, ...
        stevec = 1
        for i in range(len(intervali)):
            output_file = f"rezultati-vsak-interval-vsi-indeksi/rezultati_investicije{stevec}.csv"
            # ker v for loopu klicemo je to zato ker za razlicne intervale
            izracun_dca_metoda_prilagojena_da_naredi_csv(
                keri_indeksi[0], keri_indeksi[1], keri_indeksi[2],
                initial_investment = zacetna_investicija,
                monthly_investment = mesecni_vlozki,
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








