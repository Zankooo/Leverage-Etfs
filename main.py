from glavna_funkcija import kdaj_kupiti_katerega, kdaj_kupiti_katerega_ta_dela
from izracuni import izracun_dobicka_dca
from ne_pogosto_uporabljene.data_printer import *
from csv_operacije import *
from ne_pogosto_uporabljene.fancy_zakljucki_programa import *
from leverage_csv_file import calculate_leverage

print('----------')


podatki = load_csv('podatki/spx.csv')



kdaj_kupiti_katerega_ta_dela(podatki)





fancy_zakljucek_1()



