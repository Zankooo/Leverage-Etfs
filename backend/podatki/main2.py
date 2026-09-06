# naloudad csv
# PO POTREBI
# izbacit holidayse
# izlocit nepotrebne stolpce
# --
# naredit vzvode
# ustvari spet csv nazaj

from pathlib import Path

from izracuni import izracun_dnevnih_sprememb
from obcasno_pogosti_fajli.csv_operacije import (
    load_csv,
    naredi_leverage_iz_osnovnega,
    ustvari_nov_csv_file,
)


def main():
    

    csv_path = "tukaj_das_path_do_datoteke_ki_je_v_tej_isti_mapi"

    # Nujna vrstica
    podatki = load_csv(csv_path)

    # izbacit holidayse
    # izlocit nepotrebne stolpce
    # --
    # naredit vzvode
    

    # Nujna vrstica
    ustvari_nov_csv_file(podatki)


if __name__ == "__main__":
    main()