from data_printer import *
from izracuni import *
from csv_operacije import *
from fancy_zakljucki_programa import *
from leverage_csv_file import calculate_leverage

print('----------')


podatki = load_csv('podatki/spx.csv')

izracunn = izracun_dobicka_mesecne_investicije_prvega(podatki)





#calculated_leverage = calculate_leverage(daily_changes)
#izracuni = izracun_dobicka_mesecne_investicije_prvega(calculated_leverage)


fancy_zakljucek_1()



