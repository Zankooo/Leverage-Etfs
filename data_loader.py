import csv

def load_csv(filepath):
    """
    Prebere CSV datoteko in vrne podatke kot dvojni array (list of lists).
    """
    with open(filepath, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        array = [row for row in csv_reader]
        return array
