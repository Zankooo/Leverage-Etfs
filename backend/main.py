import os
import glob
import re
from pathlib import Path
from typing import Literal
from uuid import UUID, uuid4

# Third-party libraries
from colorama import init, Fore, Style
from rich.progress import Progress
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# Local imports
from izracuni import *
from testing_file import *
from obcasno_pogosti_fajli.csv_operacije import *
from obcasno_pogosti_fajli.fancy_zakljucki_programa import *
from grafi import narisi_vec_grafov, narisi_logaritmicne_grafe

init(autoreset=True)

# spletna stran za primerjavo, oziroma dela isto ali zelo podobno
# pobrat se kaksno idejo iz nje in jo narest tuki notri
# https://www.leveraged-etfs.com/

app = FastAPI()

# te tri vrstice so da se grafi prikazejo na frontnedu
# kje se nahaja main.py -> to rabimo ker bo koda laufala nekje drgje in tam 
# ne ve kje pac je main.oy
BASE_DIR = Path(__file__).resolve().parent

# definiramo oz imena map kamor bomo shranjevali
MAPA_GRAFI = BASE_DIR / "mapa-grafi"
MAPA_REZULTATI = BASE_DIR / "rezultati-vsak-interval-vsi-indeksi"
MAPA_TESTING = BASE_DIR / "testing"

# Ustvari mape, če še ne obstajajo
MAPA_GRAFI.mkdir(parents=True, exist_ok=True)
MAPA_REZULTATI.mkdir(parents=True, exist_ok=True)
MAPA_TESTING.mkdir(parents=True, exist_ok=True)

app.mount("/grafi", StaticFiles(directory=str(MAPA_GRAFI)), name="grafi")


# Obvezno za frontend dostop
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# UPLOAD PODATKOV
print()
print(Fore.GREEN + "Začetek programa " + Style.RESET_ALL + "----------------------------------------------------------------")
# UPLOAD PODATKOV DA JIH PREBEREMO
sp_500 = load_csv(BASE_DIR / '1x-leverage' / 'sp-500-1x.csv')
sp_500_2x = load_csv(BASE_DIR / '2x-leverage' / 'sp-500-2x.csv')
sp_500_3x = load_csv(BASE_DIR / '3x-leverage' / 'sp-500-3x.csv')
print()
nasdaq_100 = load_csv(BASE_DIR / '1x-leverage' / 'nasdaq-100-1x.csv')
nasdaq_100_2x = load_csv(BASE_DIR / '2x-leverage' / 'nasdaq-100-2x.csv')
nasdaq_100_3x = load_csv(BASE_DIR / '3x-leverage' / 'nasdaq-100-3x.csv')
print()
nasdaq_comp = load_csv(BASE_DIR / '1x-leverage' / 'nasdaq-comp-1x.csv')
nasdaq_comp_2x = load_csv(BASE_DIR / '2x-leverage' / 'nasdaq-comp-2x.csv')
nasdaq_comp_3x = load_csv(BASE_DIR / '3x-leverage' / 'nasdaq-comp-3x.csv')
print("----------------------------------------------------------------------------------")

# probna funkcija če dela vse skup
@app.get("/")
def root():
    # dobit moramo json pravih podatkov in nazaj posljemo tudi nek json
    return {"message": "Backend deluje"}

#------------------------------------------------------

# -----------------------------------------------------
class podatki_iz_frontenda(BaseModel):
    zacetna_investicija: int
    mesecni_vlozek: int
    indeks : str
    interval : int
    tip_intervala: Literal["letni", "mesecni"] = "mesecni"
    language: Literal["sl", "en"] = "sl"

# primerjava_vrstic ti zračuna številke in statistiko, 
# kdo je zmagovalec (1x, 2x ali 3x).
@app.post("/primerjava_vrstic")
def root(data: podatki_iz_frontenda):
    print()
    print("PRVI REST API CALL ")
    print(" PRIMERJAVA PO VRSTICAH:")
    keri_indeksi = pridobi_indekse(data.indeks)
    print(" Funkcija kater indeksi ✅ ")
    funkcija_naredi_vse(
        data.zacetna_investicija,
        data.mesecni_vlozek,
        data.interval,
        keri_indeksi,
        data.tip_intervala
        )
    print('----------')

    print("Uspešno ustvarjeni CSV-ji v mapi 'testing' ✅ ")
    print()
    # funkcija 'funkcija_naredi_vse' naredi csv fajle od vseh treh za vsak interval, 
    # da jih ta funkcija lahko prejme in naredi primerjavo
    primerjave = primerjaj_tri_indekse("testing/osnoven.csv", "testing/vzvod-2x.csv", "testing/vzvod-3x.csv")
    print(" Funkcija primerjaj tri indekse ✅")
    return primerjave
    
    

# html-files ti zgenerira podrobne podatke za vsako obdobje 
# posebej in ti iz njih nariše grafe, 
# da lahko gibanje investicije dejansko vidiš!
@app.post("/html-files")
def ustvari_grafe(data: podatki_iz_frontenda, request: Request):
    print()
    print("DRUGI REST API CALL ")
    
    print("GRAFKI")
    keri_indeksi = pridobi_indekse(data.indeks)
    print(" Funkcija kater indeksi ✅ ")
    
    cela_investicija_skupaj = data.zacetna_investicija + data.interval * 12 * data.mesecni_vlozek

    # Vsaka simulacija ohrani svoje številčne rezultate in obe jezikovni različici.
    simulation_id = uuid4().hex
    csv_folder = MAPA_REZULTATI / simulation_id
    graph_folder = MAPA_GRAFI / simulation_id / data.language

    funkcija_naredi_rezultat_za_csvje(
        keri_indeksi, data.interval, data.zacetna_investicija, data.mesecni_vlozek,
        data.tip_intervala, output_dir=csv_folder,
    )
    (csv_folder / "parametri.json").write_text(data.model_dump_json(), encoding="utf-8")
    print(" funkcija_naredi_rezultat_za_csvje ✅ ")
    print()
    
    funkcija_ki_narise_grafe(
        data.zacetna_investicija, data.mesecni_vlozek, cela_investicija_skupaj,
        language=data.language, csv_folder=csv_folder, graph_folder=graph_folder,
    )
    print(" funkcija_ki_narise_grafe ✅ ")
    

    
    
    # vse htmlje
    json_grafi = dobi_grafe_v_json(simulation_id, data.language, request)
    print(" vrnemo json grafov ✅ ")
    
    fancy_zakljucek_1()
    return json_grafi


@app.get("/graf/{simulation_id}/{language}/{filename}", name="graf_v_jeziku")
def graf_v_jeziku(simulation_id: UUID, language: Literal["sl", "en"], filename: str):
    """Drugi jezik izrišemo ob prvem odprtju iz istih CSV-jev, brez nove simulacije."""
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}--\d{4}-\d{2}-\d{2}\.html", filename):
        raise HTTPException(status_code=404, detail="Graph not found")

    csv_folder = MAPA_REZULTATI / simulation_id.hex
    csv_path = csv_folder / Path(filename).with_suffix(".csv")
    parameters_path = csv_folder / "parametri.json"
    if not csv_path.is_file() or not parameters_path.is_file():
        raise HTTPException(status_code=404, detail="Graph not found")

    html_path = MAPA_GRAFI / simulation_id.hex / language / filename
    if not html_path.is_file():
        data = podatki_iz_frontenda.model_validate_json(parameters_path.read_text(encoding="utf-8"))
        total = data.zacetna_investicija + data.interval * 12 * data.mesecni_vlozek
        narisi_logaritmicne_grafe(
            data.zacetna_investicija, data.mesecni_vlozek, total,
            csv_path, html_path, language=language,
        )
    return FileResponse(html_path, media_type="text/html")
    
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
def funkcija_naredi_1x_rezultate(zacetna_investicija, mesecne_investicije, interval, indeks, tip_intervala="mesecni"):
    # izracuna intervale
    intervali = generiraj_intervale(indeks, interval, tip_intervala)
    # ta progress je basically v konzoli da je bolj fancy 
    with Progress() as progress:
        print()
        task = progress.add_task("[cyan]Izdelava osnoven.csv...", total=len(intervali))
        # for loop za vse datume pac
        for i in range(len(intervali)):
            metoda_dca_za_testing_prilagojena(indeks, zacetna_investicija, mesecne_investicije,intervali[i][0], intervali[i][1], "osnoven")
            progress.advance(task)
    return 0

def funkcija_naredi_2x_rezultate(zacetna_investicija, mesecne_investicije, interval, indeks, tip_intervala="mesecni"):
    # izracuna intervale
    intervali = generiraj_intervale(indeks, interval, tip_intervala)
    # ta progress je basically v konzoli da je bolj fancy 
    with Progress() as progress:
        task = progress.add_task("[magenta]Izdelava vzvod-2x.csv...", total=len(intervali))
        # for loop za vse datume pac
        for i in range(len(intervali)):
            metoda_dca_za_testing_prilagojena(indeks, zacetna_investicija, mesecne_investicije,intervali[i][0], intervali[i][1], "vzvod-2x")
            progress.advance(task)
    return 0

def funkcija_naredi_3x_rezultate(zacetna_investicija, mesecne_investicije, interval, indeks, tip_intervala="mesecni"):
    # izracuna intervale
    intervali = generiraj_intervale(indeks, interval, tip_intervala)
    # ta progress je basically v konzoli da je bolj fancy 
    with Progress() as progress:
        task = progress.add_task("[orange1]Izdelava vzvod-3x.csv...", total=len(intervali))
        # for loop za vse datume pac
        for i in range(len(intervali)):
            metoda_dca_za_testing_prilagojena(indeks, zacetna_investicija, mesecne_investicije,intervali[i][0], intervali[i][1], "vzvod-3x")
            progress.advance(task)
    return 0


#---------------------------------------------------------------------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------------------------------------------------------------------
#FUNKCIJA KI KLICE UNE TRI ZGORAJ
def funkcija_naredi_vse(zacetna_investicija, mesecne_investicije, interval, indeksi, tip_intervala="mesecni"):
    # Najprej se prepričamo, da mapa 'testing' sploh obstaja
    os.makedirs('testing', exist_ok=True)
    
    # preverimo ce so od prejsnega zagona programa ze kaksne datoteke v testing mapi, 
    # in ce so jih izbrisemo, da ustvarimo prostor da se ustvarijo nove -> brez tega filtra moramo sami zbrisat rocno
    test_files = glob.glob('testing/*.csv')
    if test_files:
        for file in test_files:
            os.remove(file)
    funkcija_naredi_1x_rezultate(zacetna_investicija, mesecne_investicije, interval, indeksi[0], tip_intervala)
    funkcija_naredi_2x_rezultate(zacetna_investicija, mesecne_investicije, interval, indeksi[1], tip_intervala)
    funkcija_naredi_3x_rezultate(zacetna_investicija, mesecne_investicije, interval, indeksi[2], tip_intervala)
    return 0



# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def funkcija_naredi_rezultat_za_csvje(keri_indeksi, interval, zacetna_investicija, mesecni_vlozki,
                                   tip_intervala="mesecni", output_dir=None):
    # rezultate shranjujemo v mapo: 'rezultati-vsak-interval-vsi-indeksi'
    # ce se ni ustvarjena mapa jo ustvarimo
    folder = Path(output_dir) if output_dir is not None else MAPA_REZULTATI
    folder.mkdir(parents=True, exist_ok=True)

    # da pripravimo prostor da nove fajle damo notri moremo prej use zbrisat. to naredi pa ta koda
    for csv_file in glob.glob(os.path.join(folder, "*.csv")):  # 🔍 Najdi vse CSV datoteke
        os.remove(csv_file)

    # izračuna intervale -> na podlagi osnovnega indeksa.. pac itak bodo imeli vsi iste intervale 
    # in iste datume imajo.. teoreticno bi lahko tudi dali ker kol indeksi[1] ali indeksi[2]
    intervali = generiraj_intervale(keri_indeksi[0], interval, tip_intervala)

    
    with Progress() as progress:
        task = progress.add_task("[green]Ustvarjam CSV-je...", total=len(intervali))
        for i in range(len(intervali)):
            datum_zacetka = intervali[i][0]
            datum_konca = intervali[i][1]
            output_file = folder / f"{datum_zacetka}--{datum_konca}.csv"
            # ker v for loopu klicemo je to zato ker za razlicne intervale
            izracun_dca_metoda_prilagojena_da_naredi_csv(
                keri_indeksi[0], keri_indeksi[1], keri_indeksi[2],
                initial_investment = zacetna_investicija,
                monthly_investment = mesecni_vlozki,
                datum_zacetka = datum_zacetka,
                datum_konca = datum_konca,
                output_file = output_file
            )
            progress.advance(task)
            
    return 0

# ------

# 2. GLAVNA FUNKCIJA - funkcija ki narise grafe iz vseh csvjev v mapi: 'rezultati-vsak-interval-vsi-indeksi'
def funkcija_ki_narise_grafe(zacetna_investicija, mesecna_investicija, cela_investicija_skupaj,
                           language="sl", csv_folder=None, graph_folder=None):
    print()
    # usvarimo mapo ce se ne obstaja
    folder = Path(graph_folder) if graph_folder is not None else MAPA_GRAFI / language
    if folder.exists():
        for file in folder.iterdir():
            if file.is_file():
                file.unlink()
    else:
        folder.mkdir(parents=True, exist_ok=True)

    # preštej csv-je v mapi in jih ustrezno vzemi
    mapa = Path(csv_folder) if csv_folder is not None else MAPA_REZULTATI
    csv_files = sorted(list(mapa.glob("*.csv")))

    # tukaj dodaj da ustvari mapo ce se ne obstaja... 
    # ce pa ze obstaja pa iz nje vse odstrani
    with Progress() as progress:
        task = progress.add_task("[yellow]Izdelava HTML grafov...", total=len(csv_files))
        html_files = [folder / f"{csv_path.stem}.html" for csv_path in csv_files]
        for _ in narisi_vec_grafov(
            zacetna_investicija, mesecna_investicija, cela_investicija_skupaj,
            csv_files, html_files, language=language,
        ):
            progress.advance(task)
    
    

def dobi_grafe_v_json(simulation_id, language, request):
    """Vrne grafe po datumih ter URL za vsak jezik iste simulacije."""
    mapa = MAPA_GRAFI / simulation_id / language

    # Datoteke so sedaj poimenovane po datumih (YYYY-MM-DD--YYYY-MM-DD.html)
    # Zato jih navadno abecedno sortiranje avtomatsko uredi kronološko!
    files = sorted([f for f in mapa.iterdir() if f.suffix == ".html"])

    results = []
    for i, file_path in enumerate(files, start=1):
        urls = {
            lang: str(request.url_for("graf_v_jeziku", simulation_id=simulation_id,
                                      language=lang, filename=file_path.name))
            for lang in ("sl", "en")
        }
        results.append({
            "id": i,
            "title": file_path.stem,
            "filename": file_path.name,
            "url": urls[language],
            "urls": urls,
        })

    return {
        "simulation_id": simulation_id,
        "language": language,
        "results": results
    }
# ---------------------------------------------------------------------------------------------

# POKLICEMO TO KAR JE TUKAJ IN JE TO TO

# to rabimo ker te podatke uporabljata obe glavni funkciji







