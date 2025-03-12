def remove_empty_values(data):
    """
    Odstrani vrstice, kjer je drugi stolpec (data[i][1]) prazen niz "".

    :param data: Seznam seznamov, kjer je vsaka podseznam vrstica CSV-ja.
    """
    i = 0
    while i < len(data):  # Iteriramo po seznamu
        if len(data[i]) > 1 and data[i][1] == "":  # Če drugi stolpec vsebuje "", izbrišemo vrstico
            del data[i]  # Odstranimo vrstico
        else:
            i += 1  # Premaknemo se na naslednji element samo, če ni bilo brisanja
    return data  # Vrnemo urejeni seznam

# Primer podatkov
data = [
    ["1971-02-05", ""],
    ["1971-02-08", "100.840"],
    ["1971-02-09", "100.760"],
    ["1971-02-10", ""],
    ["1971-02-11", "101.450"],
    ["1971-02-12", "102.050"],
    ["1971-02-15", ""],
    ["1971-02-16", "102.190"],
    ["1971-02-17", "101.740"],
    ["1971-02-18", "101.420"],
    ["1971-02-19", "100.700"],
    ["1971-02-22", "99.680"],
    ["1971-02-23", "99.720"],
    ["1971-02-24", "100.640"],
    ["1971-02-25", "101.230"],
    ["1971-02-26", ""],
    ["1971-03-01", "101.780"],
    ["1971-03-02", "101.840"],
    ["1971-03-03", "102.070"],
]




def printt(data):
    for i in range(len(data)):
        print(data[i])

data = remove_empty_values(data)
printt(data)