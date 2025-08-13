import pandas as pd

def print_original(podatki):
    """Izpiše podatke v originalni obliki."""
    print("Izpis v originalni obliki: 📝")
    print(podatki)

def print_vsak_v_svoji_vrstici(podatki):
    """Funkcija sprinta vsak line v svoji vrstici
    @:param dvojni array
    """
    print("Izpis vsak list v svoji vrstici: 📝")
    for i in range(0, len(podatki)):
        print(podatki[i])



def print_lepo_s_pandas(podatki):
    """
    Sprejme list-of-lists ali DataFrame in ga lepo izpiše kot tabelo.
    """
    # Če je list-of-lists, pretvori v DataFrame
    if isinstance(podatki, list):
        df = pd.DataFrame(podatki)
    else:
        df = podatki.copy()

    print("Izpis podatkov v tabeli 📊")
    print(df.to_string(index=False))
