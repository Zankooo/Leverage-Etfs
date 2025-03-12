from data_printer import *
from izracuni import *
from csv_operacije import *
from fancy_zakljucki_programa import *




podatki = load_csv('podatki/spx_history_novi.csv')
print('----------')

daily_changes = calculate_daily_changes(podatki)
print_vsak_v_svoji_vrstici(daily_changes)
calculate_return(podatki)





fancy1()



