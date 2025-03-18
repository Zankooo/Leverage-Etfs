# tukaj je pa format taksen da mora biti se daily change !!!


def calculate_leverage(data):
    def parse_percentage(percent_str):
        return float(percent_str.strip('%')) / 100

    leveraged_data = [data[0], data[1]]  # Ohranimo glavo
    previous_close = float(data[2][1])  # Začetna cena zapiranja (pretvorba iz niza v float)
    leverage = float(input("Kakšen x leverage želimo? "))

    # Preveri, ali je leverage v veljavnem območju
    if (leverage < 0) or (leverage > 5):
        print("Napaka: Leverage faktor mora biti med 0 in 5.")
        return

    # Dodaj "LEVERAGE" in faktor leverage v prvo vrstico
    leveraged_data[0].insert(1, f"LEVERAGE {leverage}x")

    for row in data[2:]:
        date, close_price, daily_change = row
        close_price = float(close_price)  # Pretvori Close-Price iz niza v float
        daily_change_decimal = parse_percentage(daily_change)  # Pretvori Daily Change (%) v decimalno obliko

        # Izračunaj novo dnevno spremembo z leverage
        leveraged_daily_change = daily_change_decimal * leverage

        # Izračunaj novo ceno zapiranja in zaokroži na 2 decimalki
        new_close_price = round(previous_close * (1 + leveraged_daily_change), 2)

        # Dodaj novo vrstico v leveraged_data
        leveraged_data.append([date, new_close_price, f"{leveraged_daily_change * 100:.2f}%"])

        # Posodobi previous_close za naslednjo iteracijo
        previous_close = new_close_price

    return leveraged_data
