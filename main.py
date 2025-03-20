from data_printer import *
from izracuni import *
from csv_operacije import *
from fancy_zakljucki_programa import *
from leverage_csv_file import calculate_leverage

print('----------')


podatki = load_csv('podatki/nasdaq100.csv')



leverage = calculate_leverage(podatki)
fancy_print(leverage)

ustvari_nov_csv_file(leverage)



fancy_zakljucek_1()



