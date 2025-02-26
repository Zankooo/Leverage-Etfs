

def calculate_daily_changes(podatki):
    """
    Sprejme dvojni array s podatki o NASDAQ indeksu in vrne array z dodatnim stolpcem; "daily change"
    Prva vrstica je ime indeksa in od kdaj do kdaj
    Druga vrstica so poimenovanje podatkov
    Tretja so pa ze podatki, prvi je datum drugi pa vrednost

    """

    def is_float(value):
        """Notranja funkcija; Preveri, ali je podana vrednost veljaven float."""
        try:
            float(value)
            return True
        except ValueError:
            return False

    # Dodamo stolpec 'Daily Change (%)' prvo vrstico
    result = [podatki[0] + ['Daily Change (%)']]

    # Inicializacija prve vrstice brez spremembe
    result.append(podatki[1] + [None])  # Prvi dan ni spremembe

    # Drugi dan nastavim na '0%', ker ni spremembe
    result.append(podatki[2] + ['0%'])




    # Izračun spremembe za vsak naslednji dan
    for i in range(3, len(podatki)):
        current_value = podatki[i][1]
        previous_value = podatki[i - 1][1]  # Ena vrstica nazaj
        previous_two_value = podatki[i - 2][1]  # Dve vrstici nazaj

        # Če je trenutna vrednost prazna, napišemo "holidays"
        if current_value == '':
            result.append(podatki[i] + ['Holidays'])
            # nadaljujemo loop
            continue  # Ne računamo spremembe za ta dan

        # Če je trenutna vrednost veljaven float
        if is_float(current_value):
            current_value = float(current_value)
            last_known_value = current_value  # Posodobimo zadnjo znano vrednost

            # Če je prejšnja vrednost prazna, uporabimo dve vrstice nazaj
            if previous_value == '' and is_float(previous_two_value):
                print(f"⚠️ Warning: Missing data at line {i}. Using value from two days ago.")
                previous_value = float(previous_two_value)

            # Če sta prejšnja in dve vrstice nazaj prazni, uporabimo še starejšo vrednost
            elif previous_value == '' and previous_two_value == '' and last_known_value is not None:
                print(f"⚠️ Warning: Two previous values missing at line {i}. Using last known value {last_known_value}.")
                previous_value = last_known_value

            # Če je prejšnja vrednost še vedno prazna, napišemo "prejsni je holidays"
            if previous_value == '':
                result.append(podatki[i] + ['prejsni je holidays'])
                continue

            # Če je vse v redu, izračunamo spremembo
            previous_value = float(previous_value)
            daily_change = ((current_value - previous_value) / previous_value) * 100
            change_str = f"{'+' if daily_change > 0 else ''}{round(daily_change, 2)}%"
            result.append(podatki[i] + [change_str])
        else:
            result.append(podatki[i] + ['Invalid'])

    return result


# TO DEJANSKO DELA AMPAK MOREM KODO NASTUDIRAT.
