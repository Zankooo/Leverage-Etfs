from datetime import datetime
from dateutil.relativedelta import relativedelta
from csv import reader
from csv import reader
import os

def generiraj_intervale_leto(podatki, dolzina_intervala_let):
    """
    Funkcija generira intervale za izbrano število let
    Da nato lahko naredimo testing na teh datumih 
    :param podatki: List of lists (dogovorjen format, prve 2 vrstice sta naslova): 
    Nasdaq-composite, 1971-2025
    Date, Close-price
    1971-02-05,100.000
    1971-02-08,100.840
    1971-02-09,100.760
    :param dolzina_intervala_let: int, dolžina intervala v letih
    :return: list of lists [[zacetni_datum, koncni_datum], ...]: 
    [
    ['1962-01-02', '1967-01-03']
    ['1963-01-02', '1968-01-02']
    ['1964-01-02', '1969-01-02']
    ['1965-01-04', '1970-01-05']
    ['1966-01-03', '1971-01-04']
    ['1967-01-03', '1972-01-03']
    ['1968-01-02', '1973-01-02']
    ['1969-01-02', '1974-01-02']
    ['1970-01-02', '1975-01-02']
    ['1971-01-04', '1976-01-05']
    ['1972-01-03', '1977-01-03']
    ]
    """
    # Preskoči naslovne vrstice
    podatki = podatki[2:]

    # Pretvori v datetime in poišči prvi datum v vsakem letu
    datumi = [datetime.strptime(row[0], "%Y-%m-%d") for row in podatki]
    prvi_v_letu = {}
    for d in datumi:
        if d.year not in prvi_v_letu:
            prvi_v_letu[d.year] = d

    # Naredi intervale
    intervali = []
    leta = sorted(prvi_v_letu.keys())
    for leto in leta:
        start_date = prvi_v_letu[leto]
        konec_date = start_date + relativedelta(years=dolzina_intervala_let)

        # Poišči prvi datum >= konec_date
        konec = next((d for d in datumi if d >= konec_date), None)
        if konec:
            intervali.append([start_date.strftime("%Y-%m-%d"), konec.strftime("%Y-%m-%d")])

    return intervali





def primerjaj_tri_indekse(file1, file2, file3, stolpec=5):
    def pct_diff(a, b):
        try:
            return round((a - b) / b * 100, 2)
        except ZeroDivisionError:
            return None

    with open(file1, "r", encoding="utf-8") as f1, \
         open(file2, "r", encoding="utf-8") as f2, \
         open(file3, "r", encoding="utf-8") as f3:

        podatki1 = list(reader(f1))
        podatki2 = list(reader(f2))
        podatki3 = list(reader(f3))

    wins = {
        os.path.basename(file1): {"count": 0, "procent": 0},
        os.path.basename(file2): {"count": 0, "procent": 0},
        os.path.basename(file3): {"count": 0, "procent": 0},
    }

    
    rows_output = []

    rows = min(len(podatki1), len(podatki2), len(podatki3))

    for i in range(1, rows):
        try:
            v1 = float(podatki1[i][stolpec])
            v2 = float(podatki2[i][stolpec])
            v3 = float(podatki3[i][stolpec])

            f1_gain, f1_tot = float(podatki1[i][4]), float(podatki1[i][5])
            f2_gain, f2_tot = float(podatki2[i][4]), float(podatki2[i][5])
            f3_gain, f3_tot = float(podatki3[i][4]), float(podatki3[i][5])
        except (ValueError, IndexError):
            continue

        datum = podatki1[i][0]

        candidates = [
            {
                "file": os.path.basename(file1),
                "compare_value": v1,
                "gain": round(f1_gain, 2),
                "total": round(f1_tot, 2),
            },
            {
                "file": os.path.basename(file2),
                "compare_value": v2,
                "gain": round(f2_gain, 2),
                "total": round(f2_tot, 2),
            },
            {
                "file": os.path.basename(file3),
                "compare_value": v3,
                "gain": round(f3_gain, 2),
                "total": round(f3_tot, 2),
            },
        ]

        ordered = sorted(candidates, key=lambda x: x["compare_value"], reverse=True)

        best = ordered[0]
        second = ordered[1]
        third = ordered[2]

        diff_best_second = pct_diff(best["compare_value"], second["compare_value"])
        diff_second_third = pct_diff(second["compare_value"], third["compare_value"])

        rows_output.append({
            "datum": datum,
            "best": best,
            "second": second,
            "third": third,
            "diff_best_second_pct": diff_best_second,
            "diff_second_third_pct": diff_second_third
        })

        wins[best["file"]]["count"] += 1

    total_compared = sum(item["count"] for item in wins.values())

    if total_compared > 0:
        for file_name in wins:
            wins[file_name]["procent"] = round(
                wins[file_name]["count"] / total_compared * 100, 2
            )
    else:
        for file_name in wins:
            wins[file_name]["procent"] = 0

    def safe_float(value):
        try:
            return round(float(value), 2)
        except (TypeError, ValueError):
            return value

    summary = {
        "zacetna_investicija": safe_float(podatki1[1][1]) if len(podatki1) > 1 else None,
        "vse_mesecne_investicije": safe_float(podatki1[1][2]) if len(podatki1) > 1 else None,
        "skupaj_investirano": safe_float(podatki1[1][3]) if len(podatki1) > 1 else None,
        "wins": wins,
        "total_compared": total_compared
    }

    return {
        "summary": summary,
        "rows": rows_output
    }

