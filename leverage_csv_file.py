# tukaj je pa format taksen da mora biti se daily change !!!
from izracuni import izracun_dnevnih_sprememb
# TA FUNKCIJA DELA PRAV, TUDI Z IZRACUN MESECNI
# CE DAMO SAMO ZACETNA INVESTICIJA PRIDE ISTO KOT JE DBPG. KAR JE ODLICNO!
# AMPAK CE DAMO LEVERAGE FOKTOR 1, NE DOBIMO ISTO, TO NE VEM ZAKAJ AMPAK JA... MAL S CHATOM, MOZNO KAKE DECIMALKE?
def calculate_leverage(podatki):

    podatki = izracun_dnevnih_sprememb(podatki)

    def parse_percentage(percent_str):
        return float(percent_str.strip('%')) / 100
    leveraged_data = [podatki[0], podatki[1]]  # Ohranimo glavo
    previous_close = float(podatki[2][1])  # Začetna cena zapiranja (pretvorba iz niza v float)
    leverage = float(input("Kakšen x leverage želimo? "))
    # Preveri, ali je leverage v veljavnem območju
    if (leverage < 0) or (leverage > 4):
        print("Napaka: Leverage faktor mora biti med 0 in 4.")
        return
    # Dodaj "LEVERAGE" in faktor leverage v prvo vrstico
    leveraged_data[0].insert(1, f"LEVERAGE {leverage}x")

    for row in podatki[2:]:
        date, close_price, daily_change = row
        daily_change_decimal = parse_percentage(daily_change)  # Pretvori Daily Change (%) v decimalno obliko
        # Izračunaj novo dnevno spremembo z leverage
        leveraged_daily_change = daily_change_decimal * leverage
        # Izračunaj novo ceno zapiranja in zaokroži na 2 decimalki
        # lahko zaokrozimo ampak ob 3x leverage bo slo na nulo ker od 0,01 se ne more vec dvignt
        new_close_price = previous_close * (1 + leveraged_daily_change)
        # Dodaj novo vrstico v leveraged_data
        leveraged_data.append([date, new_close_price, f"{leveraged_daily_change * 100:.2f}%"])
        # Posodobi previous_close za naslednjo iteracijo
        previous_close = new_close_price
    return leveraged_data

# ce dam 1 faktor, bi mogu dobit istega nazaja, ampak so majhne spremembe


def calculate_leverage_dodaj_stolpce(podatki):
    """Funkcija, ki izračuna leverage in doda nove stolpce v obstoječ seznam.
    :param podatki dogovorjena struktura
    :return: List of list: datum, tecaj, daily change, leverage tecaj, leverage daily change in primerjava true false
    """
    #izracunamo daily change
    podatki = izracun_dnevnih_sprememb(podatki)

    # Določimo število decimalnih mest na podlagi najbolj natančnega podatka
    def max_decimalk(podatki):
        najvec_decimalk = 0
        for i in range(2, len(podatki)):
            vrednost_str = str(podatki[i][1])
            if '.' in vrednost_str:
                decimale = vrednost_str.split('.')[1]
                dolzina = len(decimale)
                if dolzina > najvec_decimalk:
                    najvec_decimalk = dolzina
        return najvec_decimalk

    decimalk = max_decimalk(podatki)
    print(f"Max decimalk je {decimalk}")

    def parse_percentage(percent_str):
        return float(percent_str.strip('%')) / 100

    previous_close = float(podatki[2][1])  # Začetna cena zapiranja
    leverage = float(input("Kakšen x leverage želimo? "))

    if leverage < 0 or leverage > 4:
        print("Napaka: Leverage faktor mora biti med 0 in 4.")
        return

    # Posodobimo glavo s tremi novimi stolpci
    podatki[0].extend([f"LEVERAGE {leverage}x", f"DAILY CHANGE {leverage}x", "SAME PRICE?"])

    for row in podatki[2:]:
        date, close_price, daily_change = row
        daily_change_decimal = parse_percentage(daily_change)

        # Izračunamo novo dnevno spremembo z leverage
        leveraged_daily_change = daily_change_decimal * leverage

        # Izračunamo nov tečaj zapiranja in ga zaokrožimo
        new_close_price = previous_close * (1 + leveraged_daily_change)
        zaokrozeno = f"{new_close_price:.{decimalk}f}"

        # Primerjamo osnovni in leverage tečaj
        enaka_vrednost = float(zaokrozeno) == float(close_price)

        # Dodamo podatke v obstoječi seznam
        row.extend([zaokrozeno, f"{leveraged_daily_change * 100:+.2f}%", enaka_vrednost])

        # Posodobimo previous_close
        previous_close = new_close_price

    return podatki