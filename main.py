from data_printer import *
from izracuni import *
from csv_operacije import *
from fancy_zakljucki_programa import *




te_obrnit = load_csv('podatki/spx_do_danes_novi.csv')
obrnjeno = obrni_csv(te_obrnit)


sprintaj = convert_dates(obrnjeno)

print_vsak_v_svoji_vrstici(sprintaj)







fancy1()



