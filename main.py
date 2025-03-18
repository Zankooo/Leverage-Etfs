from data_printer import *
from izracuni import *
from csv_operacije import *
from fancy_zakljucki_programa import *
from leverage_csv_file import calculate_leverage

print('----------')

podatki = load_csv('podatki/spx.csv')
daily_change = izracun_dnevnih_sprememb(podatki)
calculated_leverage = calculate_leverage(daily_change)
print_vsak_v_svoji_vrstici(calculated_leverage)


data = [
    ['SP500', '1927-2020'],
    ['Date', 'Close-Price'],
    ['1927-12-30', '100'],
    ['1928-01-03', '102'],
    ['1928-01-04', '103'],
    ['1928-01-05', '106'],
    ['1928-01-06', '104'],
    ['1928-01-10', '103'],
    ['1928-01-11', '103'],
    ['1928-01-12', '104'],
    ['1928-01-16', '106'],
    ['1928-01-17', '107'],
    ['1928-01-18', '110'],
    ['1928-01-19', '115'],

]



fancy_zakljucek_1()



