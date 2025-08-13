from obcasno_pogosti_fajli.data_printer import *
from izracuni import *
from obcasno_pogosti_fajli.csv_operacije import *
from obcasno_pogosti_fajli.fancy_zakljucki_programa import *
import pandas as pd

print('----------')

podatki = load_csv('podatki_obdelani/nasdaq-100.csv')
print('----------')

podatki_dnevne_spremembe = izracun_dnevnih_sprememb(podatki)
leverage = naredi_leverage_iz_osnovnega(podatki_dnevne_spremembe)



#dodajmo leverage se dnevne spremembe pa ga ustvarimo kot file
leverage_z_dnevnimi_spremembami = izracun_dnevnih_sprememb(leverage)

ustvari_nov_csv_file(leverage_z_dnevnimi_spremembami)






fancy1()



