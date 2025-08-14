from obcasno_pogosti_fajli.data_printer import *
from izracuni import *
from testing_file import *
from obcasno_pogosti_fajli.csv_operacije import *
from obcasno_pogosti_fajli.fancy_zakljucki_programa import *
import pandas as pd

print('----------')

podatki = load_csv('podatki_ustvarjeni/nasdaq-comp.csv')
print('----------')


#izracunamo dnevne spremembe



intervali = generiraj_intervale_leto(podatki,15)
print_vsak_v_svoji_vrstici(intervali)


#for i in range(0, len(intervali)):
   # metoda_dca_za_testing_prilagojena(podatki, 10000, 100, intervali[i][0], intervali[i][1], "rezultati-nasdaq-comp")


primerjaj_stolpec("testing/rezultati-nasdaq-100.csv", "testing/rezultati-nasdaq-100-2x.csv")



fancy1()



