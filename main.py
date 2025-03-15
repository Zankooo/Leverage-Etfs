from data_printer import *
from izracuni import *
from csv_operacije import *
from fancy_zakljucki_programa import *

print('----------')

podatki = load_csv('podatki/histori_data.csv')
print('----------')

obrnjen = obrni_csv(podatki)
spremenjen_datum = spremeni_format_datumov(obrnjen)
brez_nezeljenih_stoplcev = izbrisi_nezelene_stoplce(spremenjen_datum)
print_vsak_v_svoji_vrstici(brez_nezeljenih_stoplcev)
ustvari_nov_csv_file(brez_nezeljenih_stoplcev)




fancy1()



