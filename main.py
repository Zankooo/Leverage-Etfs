from izracuni import *
from testing_file import *
from obcasno_pogosti_fajli.csv_operacije import *
from obcasno_pogosti_fajli.fancy_zakljucki_programa import *
from rich.progress import Progress
from colorama import init, Fore, Style
from dataclasses import dataclass
import threading
import os
import glob
import json
from flask import Flask, request, jsonify, send_from_directory,session

init(autoreset=True)

# ------------------------------------------------------------------------------------------
# NALOŽI CSV-je NA ZAGON STREŽNIKA
sp_500         = load_csv('podatki_ustvarjeni/sp-500.csv')
sp_500_2x      = load_csv('2x-leverage/sp-500-2x.csv')
sp_500_3x      = load_csv('3x-leverage/sp-500-3x.csv')

nasdaq_100     = load_csv('podatki_ustvarjeni/nasdaq-100.csv')
nasdaq_100_2x  = load_csv('2x-leverage/nasdaq-100-2x.csv')
nasdaq_100_3x  = load_csv('3x-leverage/nasdaq-100-3x.csv')

nasdaq_comp    = load_csv('podatki_ustvarjeni/nasdaq-comp.csv')
nasdaq_comp_2x = load_csv('2x-leverage/nasdaq-comp-2x.csv')
nasdaq_comp_3x = load_csv('3x-leverage/nasdaq-comp-3x.csv')

LINE = "═" * 54

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-secret")  


# ---------- FRONTEND -> ZA PRIDOBITEV ZNESKOV IN LE IME INDEKSA ----------
@app.get("/")
def home():
    # posrezi /frontend/index.html
    return send_from_directory("frontend", "index.html")

# ---------- API ----------
@app.post("/api/calc")
def api_calc():
    """
    Pričakuje JSON iz frontenda:
    {
      "initial": <int>,        # začetna investicija
      "monthly": <int>,        # mesečni vložek
      "index": "sp500" | "nasdaq100" | "nasdaqcomposite",
      "interval": <int>        # leta
    }
    """
    data = request.get_json(force=True, silent=True) or {}

    zacetna_investicija   = data.get("initial")
    mesecna_investicija   = data.get("monthly")
    indeks = data.get("index")
    interval  = data.get("interval")

    # Lep izpis v konzolo (pred validacijo)
    print("\n" + "="*46)
    print("📊 PREJETI PODATKI IZ FRONTENDA")
    print("="*46)
    # print(json.dumps(payload, indent=4, ensure_ascii=False))
    print("Zacetna investicija je " , zacetna_investicija)
    print("Mesecna je " , mesecna_investicija)
    print("Indeks je bil izbran" , indeks)
    print("Interval pa je bil " , interval)
    print("="*46 + "\n")

    # Vrni OK + echo + kratki status; 'primerjava' vključimo, če je serializabilen tip
    resp = {
        "ok": True,
        "echo": {
            "initial": zacetna_investicija,
            "monthly": mesecna_investicija,
            "indeks": indeks,
            "interval": interval
        },
        "status": "CSV-ji ustvarjeni v 'testing/' in primerjava izvedena."
    }
    
    
    return jsonify(resp)



# -------------



def pridobi_indekse(index_key: str):
    if index_key == "sp-500":
        return [sp_500, sp_500_2x, sp_500_3x]
    if index_key == "nasdaq-100":
        return [nasdaq_100, nasdaq_100_2x, nasdaq_100_3x]
    if index_key == "nasdaq-composite":
        return [nasdaq_comp, nasdaq_comp_2x, nasdaq_comp_3x]
    


# -----------------------------------------------------------------------------
# TRI GLAVNE FUNKCIJE 
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
#FUNKCIJA KI KLICE UNE TRI ZGORAJ
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
# GLAVNE FUNKCIJE KI KLICE ZGORNJO FUNKCIJO


#funkcija_naredi_vse(initial, mesecne_investicije, interval,indeksi)

print('----------')

print("Uspešno ustvarjeni CSV-ji v mapi 'testing' ✅ ")

# funkcija 'funkcija_naredi_vse' naredi csv fajle, da jih ta funkcija lahko prejme in naredi primerjavo
#primerjaj_tri_indekse("testing/osnoven.csv", "testing/vzvod-2x.csv", "testing/vzvod-3x.csv")












# ---- EDINI zagon strežnika ----
if __name__ == "__main__":
    app.run(debug=True, port=5001)
