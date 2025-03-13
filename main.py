from data_printer import *
from izracuni import *
from csv_operacije import *
from fancy_zakljucki_programa import *

print('----------')

podatki = load_csv('podatki/spx_history.csv')
print('----------')
#calculate_return(podatki)




podatki = calculate_annual_returns(podatki)
print_vsak_v_svoji_vrstici(podatki)


fancy1()



