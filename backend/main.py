"""Backend za primerjavo naložb in pripravo grafov.

POTEK PO KLIKU »IZRAČUNAJ« V Home.vue:
1. Frontend pošlje POST /primerjava_vrstic → primerjaj_rezultate().
   ustvari_primerjalne_csvje() izbere po vrsti 1x, 2x in 3x.
   ustvari_rezultate() za vsak vzvod obdela vsa časovna obdobja.
   primerjaj_tri_indekse() prebere te CSV-je in vrne podatke za tabelo.
2. Frontend nato pošlje POST /html-files → ustvari_grafe().
   ustvari_dnevne_csvje() shrani dnevne vrednosti vseh treh vzvodov.
   ustvari_grafe_iz_csvjev() iz njih nariše grafe v poslanem jeziku.
   dobi_grafe_v_json() vrne povezave do ustvarjenih HTML-datotek.
3. Frontend prikaže rezultate; ob kliku »Graf« odpre izbrano povezavo.

Funkcije spodaj se izvedejo šele ob klicu. Ob zagonu se pripravijo
aplikacija, mape in vhodni podatki; izračun sprožita zgornji POST-zahtevi.
"""

from pathlib import Path
from typing import Literal

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from rich.progress import Progress

from grafi import narisi_vec_grafov
from izracuni import (
    izracun_dca_metoda_prilagojena_da_naredi_csv,
    metoda_dca_za_testing_prilagojena,
)
from obcasno_pogosti_fajli.csv_operacije import load_csv
from testing_file import generiraj_intervale, primerjaj_tri_indekse


# Nastavitve aplikacije in map

app = FastAPI()
BASE_DIR = Path(__file__).resolve().parent
MAPA_GRAFI = BASE_DIR / "mapa-grafi"
MAPA_REZULTATI = BASE_DIR / "rezultati-vsak-interval-vsi-indeksi"
MAPA_TESTING = BASE_DIR / "testing"

MAPA_GRAFI.mkdir(parents=True, exist_ok=True)
MAPA_REZULTATI.mkdir(parents=True, exist_ok=True)
MAPA_TESTING.mkdir(parents=True, exist_ok=True)

# Brskalnik dobi ustvarjeni HTML prek povezave /grafi/ime-datoteke.html.
app.mount("/grafi", StaticFiles(directory=str(MAPA_GRAFI)), name="grafi")

# Frontendu na portu 3000 dovolimo klice na backend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Vhodne podatke preberemo enkrat ob zagonu.
# Vsak indeks ima že pripravljene serije za 1x, 2x in 3x.

sp_500 = load_csv(BASE_DIR / "1x-leverage" / "sp-500-1x.csv")
sp_500_2x = load_csv(BASE_DIR / "2x-leverage" / "sp-500-2x.csv")
sp_500_3x = load_csv(BASE_DIR / "3x-leverage" / "sp-500-3x.csv")

nasdaq_100 = load_csv(BASE_DIR / "1x-leverage" / "nasdaq-100-1x.csv")
nasdaq_100_2x = load_csv(BASE_DIR / "2x-leverage" / "nasdaq-100-2x.csv")
nasdaq_100_3x = load_csv(BASE_DIR / "3x-leverage" / "nasdaq-100-3x.csv")

nasdaq_comp = load_csv(BASE_DIR / "1x-leverage" / "nasdaq-comp-1x.csv")
nasdaq_comp_2x = load_csv(BASE_DIR / "2x-leverage" / "nasdaq-comp-2x.csv")
nasdaq_comp_3x = load_csv(BASE_DIR / "3x-leverage" / "nasdaq-comp-3x.csv")


# Podatki, ki jih frontend pošlje kot JSON

class podatki_iz_frontenda(BaseModel):
    zacetna_investicija: int
    mesecni_vlozek: int
    indeks: str
    interval: int
    tip_intervala: Literal["letni", "mesecni"] = "mesecni"
    language: Literal["sl", "en"] = "sl"


# API: tukaj se začne obdelava zahteve iz frontenda.

@app.get("/")
def preveri_delovanje():
    """Vrne sporočilo za preprost preizkus povezave z backendom."""
    return {"message": "Backend deluje"}


@app.post("/primerjava_vrstic")
def primerjaj_rezultate(data: podatki_iz_frontenda):
    """Iz prejetih parametrov pripravi primerjavo 1x, 2x in 3x za tabelo."""
    print("Pripravljam primerjavo naložb ...")

    # 1. Izberemo tri serije podatkov za zahtevani indeks.
    izbrani_indeksi = pridobi_indekse(data.indeks)

    # 2. Ustvarimo tri CSV-je: vsak vsebuje končne rezultate enega vzvoda.
    ustvari_primerjalne_csvje(
        data.zacetna_investicija, data.mesecni_vlozek, data.interval,
        izbrani_indeksi, data.tip_intervala,
    )

    # 3. Primerjamo rezultate vsakega obdobja in jih vrnemo frontendu.
    return primerjaj_tri_indekse(
        "testing/osnoven.csv", "testing/vzvod-2x.csv", "testing/vzvod-3x.csv",
    )


@app.post("/html-files")
def ustvari_grafe(data: podatki_iz_frontenda, request: Request):
    """Iz prejetih parametrov ustvari HTML-grafe in vrne njihove povezave."""
    print(f"Pripravljam grafe v jeziku '{data.language}' ...")
    izbrani_indeksi = pridobi_indekse(data.indeks)
    skupaj_vlozeno = data.zacetna_investicija + data.interval * 12 * data.mesecni_vlozek

    # 1. Za grafe potrebujemo dnevne vrednosti, ne samo končnih rezultatov.
    ustvari_dnevne_csvje(
        izbrani_indeksi, data.interval, data.zacetna_investicija,
        data.mesecni_vlozek, data.tip_intervala,
    )

    # 2. Iz vsakega dnevnega CSV-ja naredimo en HTML-graf.
    ustvari_grafe_iz_csvjev(
        data.zacetna_investicija, data.mesecni_vlozek, skupaj_vlozeno,
        language=data.language,
    )

    # 3. Frontend prejme povezave; ob odprtju grafa se izračun ne ponovi.
    return dobi_grafe_v_json(request)


# Izbira vhodnih podatkov

def pridobi_indekse(izbran_indeks):
    """Za izbrani indeks vrne serije v vrstnem redu: 1x, 2x, 3x."""
    if izbran_indeks == "S&P 500":
        indeksi = [sp_500, sp_500_2x, sp_500_3x]
    elif izbran_indeks == "Nasdaq 100":
        indeksi = [nasdaq_100, nasdaq_100_2x, nasdaq_100_3x]
    elif izbran_indeks == "Nasdaq Composite":
        indeksi = [nasdaq_comp, nasdaq_comp_2x, nasdaq_comp_3x]
    return indeksi


# Prvi API-klic: končni rezultati za primerjavo

def ustvari_primerjalne_csvje(
    zacetna_investicija, mesecni_vlozek, interval, izbrani_indeksi,
    tip_intervala="mesecni",
):
    """Pripravi osnoven.csv, vzvod-2x.csv in vzvod-3x.csv z rezultati obdobij."""
    # Ta mapa je relativna mapi zagona, tako kot zapis v izracuni.py.
    mapa = Path("testing")
    mapa.mkdir(parents=True, exist_ok=True)
    for datoteka in mapa.glob("*.csv"):
        datoteka.unlink()

    # ZUNANJA ZANKA: skupno funkcijo pokličemo trikrat, enkrat za vsak vzvod.
    for podatki_indeksa, ime_datoteke, barva in (
        (izbrani_indeksi[0], "osnoven", "cyan"),
        (izbrani_indeksi[1], "vzvod-2x", "magenta"),
        (izbrani_indeksi[2], "vzvod-3x", "orange1"),
    ):
        ustvari_rezultate(
            zacetna_investicija, mesecni_vlozek, interval, podatki_indeksa,
            ime_datoteke, barva, tip_intervala,
        )
    return 0


def ustvari_rezultate(
    zacetna_investicija, mesecni_vlozek, interval, podatki_indeksa,
    ime_datoteke, barva, tip_intervala="mesecni",
):
    """Za EN vzvod izračuna vsa obdobja in rezultate zapiše v izbrani CSV."""
    intervali = generiraj_intervale(podatki_indeksa, interval, tip_intervala)

    # Progress prikazuje samo napredek v terminalu; ne računa rezultatov.
    with Progress() as progress:
        task = progress.add_task(f"[{barva}]Izdelava {ime_datoteke}.csv...", total=len(intervali))
        # NOTRANJA ZANKA: vsak klic doda eno obdobje v isti CSV.
        for datum_zacetka, datum_konca in intervali:
            metoda_dca_za_testing_prilagojena(
                podatki_indeksa, zacetna_investicija, mesecni_vlozek,
                datum_zacetka, datum_konca, ime_datoteke,
            )
            progress.advance(task)
    return 0


# Drugi API-klic: dnevne vrednosti, grafi in povezave

def ustvari_dnevne_csvje(
    izbrani_indeksi, interval, zacetna_investicija, mesecni_vlozek,
    tip_intervala="mesecni",
):
    """Za vsako obdobje ustvari CSV z dnevnimi vrednostmi vseh treh vzvodov."""
    MAPA_REZULTATI.mkdir(parents=True, exist_ok=True)
    for datoteka in MAPA_REZULTATI.glob("*.csv"):
        datoteka.unlink()

    # Vse tri serije imajo iste datume, zato obdobja določimo po seriji 1x.
    intervali = generiraj_intervale(izbrani_indeksi[0], interval, tip_intervala)

    with Progress() as progress:
        task = progress.add_task("[green]Ustvarjam CSV-je...", total=len(intervali))
        for datum_zacetka, datum_konca in intervali:
            csv_pot = MAPA_REZULTATI / f"{datum_zacetka}--{datum_konca}.csv"
            izracun_dca_metoda_prilagojena_da_naredi_csv(
                izbrani_indeksi[0], izbrani_indeksi[1], izbrani_indeksi[2],
                initial_investment=zacetna_investicija,
                monthly_investment=mesecni_vlozek,
                datum_zacetka=datum_zacetka,
                datum_konca=datum_konca,
                output_file=csv_pot,
            )
            progress.advance(task)
    return 0


def ustvari_grafe_iz_csvjev(
    zacetna_investicija, mesecni_vlozek, skupaj_vlozeno, language="sl",
):
    """Prebere dnevne CSV-je in zamenja stare HTML-grafe z novimi."""
    MAPA_GRAFI.mkdir(parents=True, exist_ok=True)
    for datoteka in MAPA_GRAFI.glob("*.html"):
        datoteka.unlink()

    # Imena vsebujejo datume, zato sortiranje ohrani kronološki vrstni red.
    csv_poti = sorted(MAPA_REZULTATI.glob("*.csv"))
    html_poti = [MAPA_GRAFI / f"{csv_pot.stem}.html" for csv_pot in csv_poti]

    with Progress() as progress:
        task = progress.add_task("[yellow]Izdelava HTML grafov...", total=len(csv_poti))
        for _ in narisi_vec_grafov(
            zacetna_investicija, mesecni_vlozek, skupaj_vlozeno,
            csv_poti, html_poti, language=language,
        ):
            progress.advance(task)


def dobi_grafe_v_json(request: Request):
    """Vrne seznam povezav do že ustvarjenih HTML-grafov, urejen po datumih."""
    datoteke = sorted(MAPA_GRAFI.glob("*.html"))
    rezultati = []
    for stevilka, html_pot in enumerate(datoteke, start=1):
        rezultati.append({
            "id": stevilka,
            "title": html_pot.stem,
            "filename": html_pot.name,
            "url": str(request.url_for("grafi", path=html_pot.name)),
        })
    return {"results": rezultati}
