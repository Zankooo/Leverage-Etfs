from obcasno_pogosti_fajli.data_printer import *
from izracuni import *
from obcasno_pogosti_fajli.csv_operacije import *
from obcasno_pogosti_fajli.fancy_zakljucki_programa import *
import pandas as pd

print('----------')

podatki = load_csv('podatki_ustvarjeni/nasdaq-comp.csv')
print('----------')


#izracunamo dnevne spremembe
dnevni_izracuni = izracun_dnevnih_sprememb(podatki)

#damo to v funkcijo da dobimo leverage ven
leverage = naredi_leverage_iz_osnovnega(dnevni_izracuni)


# ustvarimo nov file z leverage
ustvari_nov_csv_file(leverage)






fancy1()



