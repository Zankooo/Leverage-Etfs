# tukaj je pa format taksen da mora biti se daily change !!!
from indeksi_zacetek_konec import najdi_indekse_zacetka_in_konca

# TA FUNKCIJA DELA PRAV, TUDI Z IZRACUN MESECNI
# CE DAMO SAMO ZACETNA INVESTICIJA PRIDE ISTO KOT JE DBPG. KAR JE ODLICNO!
# AMPAK CE DAMO LEVERAGE FOKTOR 1, NE DOBIMO ISTO, TO NE VEM ZAKAJ AMPAK JA... MAL S CHATOM, MOZNO KAKE DECIMALKE?
def calculate_leverage(podatki_z_daily_change):
    def parse_percentage(percent_str):
        return float(percent_str.strip('%')) / 100
    leveraged_data = [podatki_z_daily_change[0], podatki_z_daily_change[1]]  # Ohranimo glavo
    previous_close = float(podatki_z_daily_change[2][1])  # Začetna cena zapiranja (pretvorba iz niza v float)
    leverage = float(input("Kakšen x leverage želimo? "))
    # Preveri, ali je leverage v veljavnem območju
    if (leverage < 0) or (leverage > 4):
        print("Napaka: Leverage faktor mora biti med 0 in 4.")
        return
    # Dodaj "LEVERAGE" in faktor leverage v prvo vrstico
    leveraged_data[0].insert(1, f"LEVERAGE {leverage}x")

    for row in podatki_z_daily_change[2:]:
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