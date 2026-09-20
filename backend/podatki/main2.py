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
    load_csv,
    naredi_leverage_iz_osnovnih_podatkov,
    ustvari_nov_csv_file,
)


def main():
    # predlaga se da se prvo pripravi podatke
    # podatki_ustvarjeni -> in se iz njih potem naredi leverage
    # tudi navaden mora dati to cez ker pac so zraven dnevne spremembe

    csv_path = BACKEND_DIR / "podatki_ustvarjeni" / "nasdaq-comp.csv"

    # Nujna vrstica
    podatki =  load_csv(csv_path)
    # 
    rezultat = naredi_leverage_iz_osnovnih_podatkov(podatki)
   
    

    # Nujna vrstica
    ustvari_nov_csv_file(rezultat)


if __name__ == "__main__":
    main()
