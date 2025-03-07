from datetime import datetime
from datetime import *

def calculate_daily_changes(podatki):
    """
    Sprejme dvojni array s podatki o indeksa in vrne array z dodatnim stolpcem; "daily change"
    Prva vrstica v csv file je ime indeksa in od kdaj do kdaj je
    Druga vrstica v csv file so poimenovanje podatkov
    Tretja so pa ze podatki, prvi(na indeksu 0) je datum drugi(na indeksu 1) je pa vrednost
    """
    def is_float(value):
        """Notranja funkcija; Preveri, ali je podana vrednost veljaven float."""
        try:
            float(value)
            return True
        except ValueError:
            return False
    # Dodamo stolpec 'Daily Change (%)' prvo vrstico
    result = [podatki[0]]
    # Inicializacija prve vrstice brez spremembe
    result.append(podatki[1] + ["Daily Change (%)"])  # Prvi dan ni spremembe
    # Drugi dan nastavim na '0%', ker ni spremembe
    result.append(podatki[2] + ['0%'])
    # Izračun spremembe za vsak naslednji dan
    for i in range(3, len(podatki)):
        current_value = podatki[i][1]
        previous_value = podatki[i - 1][1]  # Ena vrstica nazaj

        # Če je trenutna vrednost prazna, napišemo "holidays"
        if current_value == '':
            result.append(podatki[i] + ['Holidays'])
            # nadaljujemo loop - continue, ker ni nic za racunat pac
            continue

        # Če je trenutna vrednost veljaven float
        if is_float(current_value):
            current_value = float(current_value)
            #ugotovit moramo prejšno vrednost, oz ker dan nazadnje je pa bil trgovalni dan
            # v skoraj večini primerov je bil prejšni dan trgovalni-ima tecaj, razen ko je bil 11/9
            # zato sem kodo tako napisal
            if previous_value == '':
                #loopamo nazaj da ugotovimo ker dan je pa tazadnji ki ima tecaj
                vrstica = i - 1
                while vrstica >= 0:
                    #tisti ki ni prazen torej
                    if podatki[vrstica][1]!= '':
                        previous_value = float(podatki[vrstica][1])
                        break
                    else:
                        vrstica = vrstica - 1

            # tukaj pa zracunamo torej spremembo in jo zapisemo v vrstico v kateri smo trenutno
            previous_value = float(previous_value)
            daily_change = ((current_value - previous_value) / previous_value) * 100
            change_str = f"{'+' if daily_change > 0 else ''}{round(daily_change, 2)}%"
            result.append(podatki[i] + [change_str])
    return result

def convert_dates(podatki):
    """
    Sprejme list of lists, kjer je prvi stolpec datum v formatu MM/DD/YYYY.
    Pretvori datume od tretje vrstice naprej v format YYYY-MM-DD.
    Vrne posodobljen seznam.
    """
    for i in range(2, len(podatki)):  # Spremenimo datume od tretje vrstice naprej
        podatki[i][0] = datetime.strptime(podatki[i][0], "%m/%d/%Y").strftime("%Y-%m-%d")
    return podatki  # Vrne posodobljene podatke


def calculate_return(podatki):
    # ta funkcija za izracun dejansko dela
    """
    Sprejme seznam seznamov [[datum, tecaj]] in začetno investicijo.
    Izračuna končno vrednost investicije glede na spremembo SP500 indeksa.

    :param data: Seznam seznamov [[datum, vrednost SP500]]
    :param initial_investment: Začetni kapital (privzeto 1000 enot)
    :return: Končna vrednost investicije
    """
    # edin fiksat ker pac on ze prvi dan uposteva donos, to pogleedat, drugace pa dejansko dela
    podatki_daily_changes = calculate_daily_changes(podatki)
    initial_investment = int(input("Vpisi zacetno investicijo: "))
    investment = initial_investment
    print("Izberi; ne more bit 0 in 1 ker so to lastnosti file-a, ampak pri 2 lahko zacnemo")
    zacetek = int(input("Zacetek kdaj, kera vrstica: ")) # pol dat eno vec kar takrat je praznik, da vidm kaj bo
    konec = int(input("Konec kdaj, kera vrstica: "))
    # ko gledam na full chart sp500 moram da ni inflation adjuested, pol se cifre matchajo
# kle se malo pogledat ker pac prvi dan ko ti kupis tukaj ze uposteva donos iz prvega dne
    for i in range(zacetek, konec+1):
        # problem je ker v spx obeh ni "" v obicnem fileu
        if podatki_daily_changes[i][2] == "Holidays":
            continue
        else:
            #damo stran procent
            daily_change = podatki_daily_changes[i][2].replace("%", "")  # Remove '%'
            # spremenimo v int in zaokrozimo na dve decimalki
            daily_change_cifra = round(float(daily_change), 2) / 100  # Convert to decimal
            # izracunamo
            # !!! ce hocemo dat vsak dan notri 10 eur je ta vrstica ali pa pac jo zbrisemo
            #investment = investment + 10
            investment = investment * (1 + daily_change_cifra) # 1 zato ker ce je donos 0,5% kar je 0,005% je v bistvu: kart 1,005
            print(f"Vrednost pri vrstici {i} oz. datumu {podatki[i][0]}: {investment:.2f}eur ({daily_change}%)")

    print("-----------")
    print(f"Investirali smo {initial_investment}eur dne {podatki[zacetek][0]}")
    print(f"Od datuma {podatki[zacetek][0]} do {podatki[konec][0]} smo imeli notri in imamo sedaj: {investment:.2f}eur")
    zasluzili = round ((investment - initial_investment),2)
    zasluzili_formatirano = f"{zasluzili:,.2f}eur"
    print(f"Oz drugace receno; zasluzili/izgubili smo {zasluzili_formatirano}")
    # Zaokrožimo na 2 decimalni mesti
    koncni_izracun = round(investment,2)
    return koncni_izracun
