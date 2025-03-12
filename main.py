from data_printer import *
from izracuni import *
from csv_operacije import *
from fancy_zakljucki_programa import *




podatki = load_csv('podatki/nasdaq-comp.csv')
print('----------')
podatki = izbaci_ven_holidayse(podatki)






fancy1()



