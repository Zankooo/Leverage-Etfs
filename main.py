from data_loader import *
from data_printer import *
from izracuni import *

# Naložimo podatke
podatki = load_csv('podatki/nasdaq.csv')


# Izračunamo dnevne spremembe
obdelani_podatki = calculate_daily_changes(podatki)

# Izpišemo podatke
print_vsak_v_svoji_vrstici(obdelani_podatki)
