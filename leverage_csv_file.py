from izracuni import izracun_dnevnih_sprememb


# ustvari iz navadnega csv indeksa
# mora bit v pravem formatu
def ustvari_2x_leverate_iz_navadnega_indeksa(podatki):
    podatki_daily_changes = izracun_dnevnih_sprememb(podatki)
    for i in range(2, len(podatki)):
        daily_change = podatki_daily_changes[i][2]
        #vrednost = podatki_daily_changes[]
