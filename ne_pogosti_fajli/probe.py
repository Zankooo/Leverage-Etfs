import csv

def my_function():
    # primer funkcije, ki vrne seznam vrednosti
    return [1927, 1942, "1927-01-03", "1942-12-31", 10000, 300, 54000, 64000, 100000, 36000, 56.25]

# Pokličemo funkcijo
row_data = my_function()

# Zapišemo v CSV kot eno vrstico
with open("rezultat.csv", mode="a", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(row_data)
