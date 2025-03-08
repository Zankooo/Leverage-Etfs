from datetime import datetime
from datetime import *
import re
def calculate_daily_changes(podatki):
    """
    Sprejme dvojni array s podatki o indeksu in vrne array z dodatnim stolpcem; "daily change"
    Prva vrstica v csv file je ime indeksa in od kdaj do kdaj je
    Druga vrstica v csv file so poimenovanje podatkov
    Tretja so pa ze podatki, prvi(na indeksu 0) je datum drugi(na indeksu 1) je pa vrednost
    """

    # ce je format datuma tako, klicemo funkcijo da spremenimo datum,
    # drugace pa ne...
    # ker hocemo da je pac v formatu 2021-10-06
    # to tuki dejansko ne rabimo ampak za vsak sluca
    # uzamemo datum iz tretje vrstice da pogledamo kako so datumi zapisani
    date_string = podatki[2][0]
    # in ce ni tako; 2021-10-06, potem klicemo funkcijo da spremenimo
    if not re.match(r"\d{4}-\d{2}-\d{2}", date_string):
        podatki = convert_dates(podatki)
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
        elif is_float(current_value):
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





def calculate_return(podatki):
    """
    Sprejme seznam seznamov [[datum, tečaj]] in omogoča začetno investicijo + mesečne vložke.
    Izračuna končno vrednost investicije glede na spremembo S&P 500 indeksa.
    :param podatki: Seznam seznamov [[datum, vrednost SP500]]
    :return: int končna vrednost investicije
    """

    podatki_daily_changes = calculate_daily_changes(podatki)
    initial_investment = int(input("Vpisi začetno investicijo: "))
    monthly_investment = int(input("Vpisi mesečni vložek: "))  # Nov vnos za mesečno investicijo
    investment = initial_investment
    mesecni_vlozki_vsota = 0
    print("Izberi začetni dan investiranja (indeks vrstice, npr. 2)")
    zacetek = int(input("Začetek (katera vrstica): "))
    konec = int(input("Konec (katera vrstica): "))

    # Nastavimo začetni mesec za mesečne vložke
    current_month = datetime.strptime(podatki[zacetek][0], "%Y-%m-%d").month

    for i in range(zacetek, konec + 1):
        if podatki_daily_changes[i][2] == "Holidays":
            continue  # Preskoči dneve, ko borza ne deluje
#CE NE DAS ZA SPX DO DANES NOVI BI MOGLO DELAT LEPO. PAC MORM POGLEDAT VSE CSV FILE IN FORMATE IN DA POL NAPISM FUNKCIJE DA PREOBLIKUJEM V EN FORMAT IN POL Z NJIM DELAM
        daily_change = podatki_daily_changes[i][2].replace("%", "")  # Odstrani "%"
        daily_change_cifra = round(float(daily_change), 2) / 100  # Pretvori v decimalno vrednost

        # Pridobimo mesec trenutnega datuma
        date = datetime.strptime(podatki[i][0], "%Y-%m-%d")

        # Če je nov mesec, dodamo mesečni vložek
        if date.month != current_month:
            investment = investment + monthly_investment
            mesecni_vlozki_vsota = mesecni_vlozki_vsota + monthly_investment
            current_month = date.month  # Posodobimo trenutni mesec

        # Izračun vrednosti portfelja
        investment = investment * (1 + daily_change_cifra)

        print(f"Vrednost pri vrstici {i} oz. datumu {podatki[i][0]}: {investment:.2f} EUR ({daily_change}%)")

    print("-----------")
    print(f"Začetna investicija: {initial_investment} EUR dne {podatki[zacetek][0]}")
    print(f"Vseh mesečnih vložkov je bilo: {mesecni_vlozki_vsota}EUR")
    print(f"Od {podatki[zacetek][0]} do {podatki[konec][0]} smo imeli skupno investicijo: {investment:.2f} EUR")

    zasluzili = round(investment - initial_investment, 2)
    zasluzili_formatirano = f"{zasluzili:,.2f} EUR"
    print(f"Zaslužek / izguba: {zasluzili_formatirano}")

    return round(investment, 2)


#-----------FUNKCIJE KI JIH KLIČEMO ZNOTRAJ DRUGIH FUNKCIJ-----------

def is_float(value):
    """Notranja funkcija; Preveri, ali je podana vrednost veljaven float."""
    try:
        float(value)
        return True
    except ValueError:
        return False


def convert_dates(podatki):
    """
    Sprejme list of lists, kjer je prvi stolpec datum v formatu MM/DD/YYYY.
    Pretvori datume od tretje vrstice naprej v format YYYY-MM-DD.
    Vrne posodobljen list of lists.
    """
    for i in range(2, len(podatki)):  # Spremenimo datume od tretje vrstice naprej
        podatki[i][0] = datetime.strptime(podatki[i][0], "%m/%d/%Y").strftime("%Y-%m-%d")
    return podatki  # Vrne posodobljene podatke