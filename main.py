from data_printer import *
from izracuni import *
import sys
from csv_operacije import *
from fancy_zakljucki_programa import *

# Naložimo podatke
# podatki = load_csv('podatki/nasdaq-comp.csv')
#
#
# # Izračunamo dnevne spremembe
# obdelani_podatki = calculate_daily_changes(podatki)
#
# # Izpišemo podatke
# print_vsak_v_svoji_vrstici(obdelani_podatki)


te_obrnit = load_csv('podatki/spx_do_danes_novi.csv')
te_obrnit = obrni_csv(te_obrnit)
print_vsak_v_svoji_vrstici(te_obrnit)





fancy1()



