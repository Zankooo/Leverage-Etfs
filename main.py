from data_printer import *
from izracuni import *
import sys
from csv_operacije import *
from fancy_zakljucki_programa import *




te_obrnit = load_csv('podatki/spx_do_danes_novi.csv')
te_obrnit = obrni_csv(te_obrnit)
print_vsak_v_svoji_vrstici(te_obrnit)





fancy1()



