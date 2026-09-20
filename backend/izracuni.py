import re
import os
from math import isfinite
import pandas as pd

from obcasno_pogosti_fajli.csv_operacije import *
# karkoli tukaj delamo oz kero kol funkcijo klicemo moramo imeti
# dogovorjen format podatkov oz csv.ja

# to funkcijo verjetno najbolje rabis v obcasno_pogosti_fajli
# ko ustvarjas primerno strukturo 
def izracun_dnevnih_sprememb(podatki):
    """
    Funkcija, ki izracuna dnevne spremembe indeksa
    :param list of lists (dogovorjen format)
    :return list of lists tak kot je bil podan in mu doda dnevne spremembe "daily changes"
    """
    # Dodamo stolpec 'Daily Change (%)' prvo vrstico
    result = [podatki[0]]
    # Inicializacija prve vrstice brez spremembe
    result.append(podatki[1] + ["Daily Change (%)"])  # Prvi dan ni spremembe
    # Drugi dan nastavim na '0%', ker pac je prvi dan
    result.append(podatki[2] + ['0%'])
    # Izračun spremembe za vsak naslednji dan
    for i in range(3, len(podatki)):
        trenutni_tecaj = float(podatki[i][1])
        dan_prej_tecaj = float(podatki[i - 1][1])
        daily_change = ((trenutni_tecaj - dan_prej_tecaj) / dan_prej_tecaj) * 100
        sprememba_procentualno = f"{'+' if daily_change > 0 else ''}{daily_change}%"
        result.append(podatki[i] + [sprememba_procentualno])
    return result




#----------- POMOZNE FUNKCIJE KI JIH KLIČEMO ZNOTRAJ DRUGIH FUNKCIJ-----------

def is_float(value):
    """Notranja funkcija; Preveri, ali je podana vrednost veljaven float."""
    try:
        float(value)
        return True
    except ValueError:
        return False



# -------------------------- spremenjena funkcija dca za testing
# --------------------------------------------

# ta funkcija tocno zracuna isto k kot funkcija 'izracun dca metoda' le da vse tri 1x in 2x in 3x naredi
# in jih da v locen csv!!
import csv
from datetime import datetime

def izracun_dca_metoda_prilagojena_da_naredi_csv(
    podatki1, podatki2, podatki3,  # morajo biti isti indeks: osnovni, 2x, 3x
    initial_investment: float,
    monthly_investment: float,
    datum_zacetka: str,
    datum_konca: str,
    output_file: str  = "rezultati_investicije.csv",
):
    """
    Prejme pripravljene serije istega indeksa za 1x, 2x in 3x:
    Nasdaq-100 2x, 2025
    Date,Close,Daily Return
    2025-01-02,100,0
    2025-01-03,102,0.02
    2025-01-06,101.49,-0.005

    Tretji stolpec že vsebuje končni dnevni donos v decimalkah:
    0.02 pomeni 2 %. Vključuje vzvod, dividende in funding.
    Donos preberemo neposredno, brez ponovnega računanja iz cen,
    brez deljenja s 100 in brez zaokroževanja pred izračunom naložbe.
    Funkcija ustvari CSV dnevnih vrednosti naložbe za izbrano obdobje.

    To funkcija ustvari
    date, A,B,C
    1928-01-03,1005.7,1011.3,1017.0
    1928-01-04,1003.39,1006.75,1010.08
    1928-01-05,993.75,987.42,980.99
    1928-01-06,1000.02,999.76,999.44
    1928-01-09,990.91,981.67,972.25

    """

    # poiščemo indekse intervala v vseh treh
    s1 = next(i for i, row in enumerate(podatki1) if row[0] == datum_zacetka)
    e1 = next(i for i, row in enumerate(podatki1) if row[0] == datum_konca)
    s2 = next(i for i, row in enumerate(podatki2) if row[0] == datum_zacetka)
    e2 = next(i for i, row in enumerate(podatki2) if row[0] == datum_konca)
    s3 = next(i for i, row in enumerate(podatki3) if row[0] == datum_zacetka)
    e3 = next(i for i, row in enumerate(podatki3) if row[0] == datum_konca)

    len1 = e1 - s1 + 1
    len2 = e2 - s2 + 1
    len3 = e3 - s3 + 1
    if not (len1 == len2 == len3):
        raise ValueError(f"Intervali serij se ne ujemajo (len1={len1}, len2={len2}, len3={len3}).")

    # začetno stanje (enako za vse tri)
    inv1 = float(initial_investment)
    inv2 = float(initial_investment)
    inv3 = float(initial_investment)

    # števci mesečnih vložkov (na serijo)
    vsota_mesecnih_vlozkov = 0.0
    st_vplacil = 0

    current_month = datetime.strptime(datum_zacetka, "%Y-%m-%d").month
    results = []

    for k in range(len1):
        i1, i2, i3 = s1 + k, s2 + k, s3 + k
        date_str = podatki1[i1][0]

        # poravnava datumov
        if podatki2[i2][0] != date_str or podatki3[i3][0] != date_str:
            raise ValueError(f"Datumi se ne ujemajo pri k={k}: {date_str} vs {podatki2[i2][0]} / {podatki3[i3][0]}")

        date_obj = datetime.strptime(date_str, "%Y-%m-%d")

        # ob prehodu v nov mesec dodamo mesečni vložek vsem trem (vplačilo šteje ENKRAT na serijo)
        if date_obj.month != current_month:
            inv1 += monthly_investment
            inv2 += monthly_investment
            inv3 += monthly_investment
            vsota_mesecnih_vlozkov += monthly_investment
            st_vplacil += 1
            current_month = date_obj.month

        # Končni dnevni donosi so že shranjeni v tretjem stolpcu: 0.02 = 2 %.
        try:
            change1 = float(podatki1[i1][2])
            change2 = float(podatki2[i2][2])
            change3 = float(podatki3[i3][2])
        except (IndexError, TypeError, ValueError) as exc:
            raise ValueError(
                f"Na datum {date_str} vse tri serije potrebujejo tretji stolpec "
                "z dnevnim donosom v decimalkah (npr. 0.02, brez %)."
            ) from exc
        if not all(isfinite(change) for change in (change1, change2, change3)):
            raise ValueError(f"Dnevni donosi na datum {date_str} morajo biti končna števila.")

        inv1 *= (1.0 + change1)
        inv2 *= (1.0 + change2)
        inv3 *= (1.0 + change3)

        results.append([date_str, round(inv1, 2), round(inv2, 2), round(inv3, 2)])

    # zapis CSV
    with open(output_file, mode="w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["date", "A", "B", "C"])
        w.writerows(results)

    # izpis povzetka (na serijo)
    
    # print(f"Začetna investicija (na serijo): {initial_investment:.2f} $")
    # print(f"Vsota mesečnih vložkov (na serijo): {vsota_mesecnih_vlozkov:.2f} $  (št. vplačil: {st_vplacil})")
    # print("Za obdobje " + datum_zacetka + " in " + datum_konca + " narejeno.")
    return round(inv1, 2), round(inv2, 2), round(inv3, 2)




# TA METODA JE FIXERICA KER SE JO KLICE V FOR LOOPU - POTREBNA ZA PRIMERJAVO PO LETIH 
def metoda_dca_za_testing_prilagojena(podatki, initial_investment, monthly_investment, datum_zacetka, datum_konca, ime_novega_filea):
    """
    Simulira DCA (Dollar Cost Averaging) investiranje za TOČNO DOLOČEN interval.
    
    Funkcija je namenjena večkratnemu klicanju v zanki (for loop). 
    Izračuna dnevno rast/padec portfelja za podano obdobje in na koncu 
    zapiše ZBIRNO VRSTICO rezultatov (začetni vložek, donos, končna vrednost) 
    na konec izbrane CSV datoteke v mapo 'testing/'. To nam omogoči 
    kasnejšo primerjavo vseh intervalov med seboj.
    
    @param podatki: seznam vrstic pripravljene serije: opis, glava in nato
        [datum, vrednost, dnevni_donos]. Tretji stolpec je decimalni donos
        (0.02 = 2 %), ki že vključuje vzvod, dividende in funding.
        Donos preberemo neposredno; ne računamo ga ponovno iz cen.
    @param initial_investment: Začetni enkratni vložek
    @param monthly_investment: Mesečni vložek ob začetku vsakega meseca
    @param datum_zacetka: Datum začetka simulacije (format 'YYYY-MM-DD')
    @param datum_konca: Datum konca simulacije (format 'YYYY-MM-DD')
    @param ime_novega_filea: Ime ciljne datoteke (npr. 'osnoven', 'vzvod-2x'), v katero se prilepi nov rezultat
    @return: 0 (Rezultat se ne vrača, temveč zapiše neposredno v CSV)
    """
    # ta funkcija je misljena da se jo klice v mainu v for loopu toliko koliko je intervalov in da se ji podaja razlicne datume pridobljena iz intervali letni
    #kle je fora ker tist dan ko mi kupimo se uposta tudi koliko je ta dan zrastlo
    # ampak tega verjetno ne bi smel upostevat, idk
    # pogledat tudi za mesecne investicije kdaj dejansko se kupjo

     # Nov vnos za mesečno investicijo
    investment = initial_investment
    mesecni_vlozki_vsota = 0

    # PROBLEM JE KER CE PRIMERJAS Z GOOGLE GRAFOM NISO CIST CIST ISTI DONOSI IN ZDEJ GRUNTAM KJE JE PROBLEM
    # zdej je okej sem testiral ampak mi ni jasno kako je lahko okej ce v for loopu ze prvi dan vzamemo, idk ampak je zlo prou
    
    # Nastavimo začetni mesec za mesečne vložke
    current_month = datetime.strptime(datum_zacetka, "%Y-%m-%d").month

    # to rabimo da lahko pozenemo loop cez vse dneve
    vrstica_zacetka = (next(i for i, row in enumerate(podatki) if row[0] == datum_zacetka))
    
    vrstica_konca = (next(i for i, row in enumerate(podatki) if row[0] == datum_konca))

    # od kere do kere vrstice gre? -> pac mi smatramo da kupimo ob close ob zaprtju, po tisti ceni
    for i in range(vrstica_zacetka, vrstica_konca + 1):
        # Donos je že pripravljen v tretjem stolpcu: 0.02 pomeni 2 %.
        # Ne delimo s 100 in ne zaokrožujemo pred izračunom naložbe.
        try:
            daily_change_cifra = float(podatki[i][2])
        except (IndexError, TypeError, ValueError) as exc:
            raise ValueError(
                f"Na datum {podatki[i][0]} serija potrebuje tretji stolpec "
                "z dnevnim donosom v decimalkah (npr. 0.02, brez %)."
            ) from exc
        if not isfinite(daily_change_cifra):
            raise ValueError(f"Dnevni donos na datum {podatki[i][0]} mora biti končno število.")

        # Pridobimo mesec trenutnega datuma, da lahko upalimo mesecno investicijo ce je nov mesec
        date = datetime.strptime(podatki[i][0], "%Y-%m-%d")

        # Če je nov mesec, dodamo mesečni vložek
        if date.month != current_month:
            investment = investment + monthly_investment
            mesecni_vlozki_vsota = mesecni_vlozki_vsota + monthly_investment
            current_month = date.month

        # Izračun vrednosti portfelja
        investment = investment * (1 + daily_change_cifra)
        
    zasluzili = round(investment - initial_investment - mesecni_vlozki_vsota, 2)
   
    # od tukaj naprej je pa pisanje v file
    # da bi v csv file pisal ane..
    # od kdaj do kdaj, zacetna investicija, vse mesecne investicije, total contribution, zasluzili in koliko imamo
    vrstica = [datum_zacetka + "-" + datum_konca, initial_investment, mesecni_vlozki_vsota, initial_investment + mesecni_vlozki_vsota, zasluzili, investment]
    
    ime_novega_filea = ime_novega_filea + ".csv"
    pot = f"testing/{ime_novega_filea}"

    # Ustvari mapo testing, če ne obstaja
    os.makedirs("testing", exist_ok=True)

    # Če datoteka obstaja, dodaj v obstoječo, drugače ustvari novo
    mode = "a" if os.path.exists(pot) else "w"

    with open(pot, mode=mode, newline="") as f:
        writer = csv.writer(f)
        
        if mode == "w":  # pišemo header samo če ustvarjamo novo datoteko
            writer.writerow([ime_novega_filea])
            writer.writerow([
                "Datum od kdaj do kdaj",
                "Zacetna investicija",
                "vse mesecne investicije",
                "skupaj vse investicije",
                "koliko smo v plusu oz minusu",
                "koliko imamo vse skupaj"
            ])
        
        writer.writerow(vrstica)
    
    return 0


 # ------------------------------------------------------
