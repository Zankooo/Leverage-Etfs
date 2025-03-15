from data_printer import *
from izracuni import *
from csv_operacije import *
from fancy_zakljucki_programa import *

print('----------')

podatki = load_csv('podatki/spx.csv')
print('----------')


# izracun_dobicka_mesecne_investicije_prvega(podatki)




podatkiii = [
    ["S&P500 1971 podatki"],  # naslovna vrstica
    ["Datum", "Tecaj"],       # glave stolpcev
    ["1971-03-25", 104], # nabavil tukaj
    ["1971-03-26", 100],
    ["1971-03-29", 105],
    ["1971-03-30", 105],
    ["1971-03-31", 105],
    ["1971-04-01", 106],
    ["1971-04-02", 106],
    ["1971-04-05", 107],
    ["1971-04-06", 102],
    ["1971-04-07", 108],
    ["1971-04-08", 108],
    ["1971-04-12", 109.5],
    ["1971-04-13", 110],
    ["1971-04-14", 109],
    ["1971-04-15", 109],
    ["1971-04-16", 109],
    ["1971-04-19", 110],
    ["1971-04-20", 115],
    ["1971-04-21", 110],
    ["1971-04-22", 109],
    ["1971-04-23", 110],
    ["1971-04-26", 111],
    ["1971-04-27", 112],
    ["1971-04-28", 113],
    ["1971-04-29", 105],
    ["1971-04-30", 114]
]

# preverit ce to dejasnko dela!?
izracun_dobicka_prodaj_kuppii(podatki)
#izracun_dobicka_mesecne_investicije_prvega(podatki)
#izracun_dobicka_mesecne_investicije_prvega(podatkiii)

fancy1()



