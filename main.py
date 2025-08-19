from obcasno_pogosti_fajli.data_printer import *
from izracuni import *
from testing_file import *
from obcasno_pogosti_fajli.csv_operacije import *
from obcasno_pogosti_fajli.fancy_zakljucki_programa import *
import pandas as pd

print('----------')

podatki = load_csv('podatki_ustvarjeni/sp-500.csv')
print('----------')


#izracunamo dnevne spremembe



intervali = generiraj_intervale_leto(podatki,15)
print_vsak_v_svoji_vrstici(intervali)

#for i in range(0, len(intervali)):
  # metoda_dca_za_testing_prilagojena(podatki, 10000, 100, intervali[i][0], intervali[i][1], "rezultati-sp-500-1x")


primerjaj_stolpec("testing/rezultati-sp-500-1x.csv", "testing/rezultati-sp-500-2x.csv")



fancy1()



