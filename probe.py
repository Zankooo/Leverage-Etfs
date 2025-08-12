podatki = [
    ["Date", "Value"],
    ["2024-05-14", 5000],
    ["2024-05-15", 5050]
]

datum = "2024-05-15"
index_vrstice = next(i for i, row in enumerate(podatki) if row[0] == datum)
print(index_vrstice)  # 2