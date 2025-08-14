from obcasno_pogosti_fajli.data_printer import *
from izracuni import *
from testing_file import *
from obcasno_pogosti_fajli.csv_operacije import *
from obcasno_pogosti_fajli.fancy_zakljucki_programa import *
import pandas as pd

print('----------')

podatki = load_csv('2x-leverage/sp-500-2x.csv')
print('----------')


#izracunamo dnevne spremembe



intervali = generiraj_intervale_15let_leto(podatki)

#for i in range(0, len(intervali)):
    #metoda_dca_za_testing_prilagojena(podatki, 10000, 100, intervali[i][0], intervali[i][1])

primerjaj_stolpec("testing/rezultat-sp-500.csv", "testing/rezultat-sp500-2x.csv")



fancy1()



