from ne_pogosto_uporabljene.data_printer import *
from csv_operacije import *
from ne_pogosto_uporabljene.fancy_zakljucki_programa import *
from leverage_csv_file import calculate_leverage

print('----------')


podatki = load_csv('podatki/nasdaq100.csv')



leverage = calculate_leverage(podatki)
fancy_print(leverage)





fancy_zakljucek_1()



