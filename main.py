from data_printer import *
from izracuni import *
from csv_operacije import *
from fancy_zakljucki_programa import *




podatki = load_csv('podatki/spx_do_danes_novi.csv')
print('----------')
podatki = spremeni_format_datumov(podatki)
podatki = obrni_csv(podatki)
print_vsak_v_svoji_vrstici(podatki)
ustvari_nov_csv_file(podatki)






fancy1()



