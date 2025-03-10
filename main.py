from data_printer import *
from izracuni import *
from csv_operacije import *
from fancy_zakljucki_programa import *




podatki = load_csv('podatki/spx_do_danes_novi.csv')
print('----------')
podatki_datumi_novi = convert_dates(podatki)
print_vsak_v_svoji_vrstici(podatki_datumi_novi)

podatki_changes = calculate_daily_changes(podatki)
print_vsak_v_svoji_vrstici(podatki_changes)

#calculate_return(podatki)



fancy1()



