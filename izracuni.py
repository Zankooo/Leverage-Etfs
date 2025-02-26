

def calculate_daily_changes(podatki):
    """
    Sprejme dvojni array s podatki o NASDAQ indeksu in vrne array z dodatnim stolpcem
    'Daily Change (%)', ki prikazuje dnevno spremembo v odstotkih.
    """

    def is_float(value):
        """Preveri, ali je podana vrednost veljaven float."""
        try:
            float(value)
            return True
        except ValueError:
            return False

    # Dodamo nov stolpec v glavo
    result = [podatki[0]]  # Glava
    result.append(podatki[1] + ['Daily Change (%)'])  # Prva vrstica
    result.append(podatki[2] + ['0%'])

    # Izračun spremembe za vsak naslednji dan
    for i in range(3, len(podatki)):
        if is_float(podatki[i - 1][1]) and is_float(podatki[i][1]):
            previous_value = float(podatki[i - 1][1])
            current_value = float(podatki[i][1])
            daily_change = ((current_value - previous_value) / previous_value) * 100
            change_str = f"{'+' if daily_change > 0 else ''}{round(daily_change, 2)}%"
            result.append(podatki[i] + [change_str])
        else:
            result.append(podatki[i] + ['Invalid'])

    return result
