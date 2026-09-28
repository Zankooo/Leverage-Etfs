# naloudad csv
# PO POTREBI
# izbacit holidayse
# izlocit nepotrebne stolpce
# --
# naredit vzvode - tudi za 1x ker morajo bit dnevne spremembe notri za vse
# ustvari spet csv nazaj

from pathlib import Path
import sys


# Pri neposrednem zagonu te datoteke omogočimo uvoze iz mape backend.
BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from obcasno_pogosti_fajli.csv_operacije import (
    izbaci_ven_holidayse,
    izbrisi_nezelene_stoplce,
    load_csv,
    naredi_leverage_iz_osnovnih_podatkov,
    ustvari_nov_csv_file,
)


def main():
    """
    Najboljše je da delam po principu:
    1. Uvozim podatke z load_csv()
    2. pripravim podatke v smislu, izbrisi nezeljene stolpce, izbaci holidayse...
    3. Z funcijo ustvari_nov_csv_file() shranim v mapo podatki-pripravljeni-za-leverage-ustvarit
    4. Uredim prvi dve vrstici da sta:
                                        ime indeksa, 1927-2026
                                        Date,Price

    Potem:
    1. Iz mape podatki-pripravljeni-za-leverage-ustvarit preberem 
    2.Ustvarim leverage z funkcijo naredi_leverage_iz_osnovnih_podatkov()
    3. ustvari_nov_csv_file() -> sicer se potem te datoteke spet shranijo v mapo
    podatki-pripravljeni-za-leverage-ustvarit ampak jih jaz rocno premaknem v zeljeno mapo
    Torej 1x-leverage 2x-leverage ali 3x-leverage
    """
    # podatki_ustvarjeni -> in se iz njih potem naredi leverage
    # tudi navaden mora dati to cez ker pac so zraven dnevne spremembe



    csv_path = BACKEND_DIR / "podatki-pripravljeni-za-leverage-ustvarit" / "NASDAQCOM-sfiltriran.csv"

    
    # Nujna vrstica
    podatki =  load_csv(csv_path)
    # rezultat = izbrisi_nezelene_stoplce(podatki)
    # izbaceni_holidaysi = izbaci_ven_holidayse(podatki)
    rezultat = naredi_leverage_iz_osnovnih_podatkov(podatki)
   
    

    # Nujna vrstica
    ustvari_nov_csv_file(rezultat)


if __name__ == "__main__":
    main()
