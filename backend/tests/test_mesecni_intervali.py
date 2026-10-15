import contextlib
import csv
import io
from datetime import date, timedelta
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

with contextlib.redirect_stdout(io.StringIO()):
    import main
from fastapi import HTTPException
from pydantic import ValidationError
from testing_file import generiraj_intervale_mesec


def podatki(datumi, donos=0):
    return [["Test"], ["Date", "Close", "Daily Return"]] + [
        [datum, "100", str(donos)] for datum in datumi
    ]


class MesecniIntervaliTest(unittest.TestCase):
    def test_mesecni_zacetki_in_konec_na_naslednji_trgovalni_dan(self):
        serija = podatki([
            "2019-01-02", "2019-01-03", "2019-02-01", "2019-03-01",
            "2020-01-02", "2020-02-03", "2020-03-02",
        ])
        self.assertEqual(generiraj_intervale_mesec(serija, 1), [
            ["2019-01-02", "2020-01-02"],
            ["2019-02-01", "2020-02-03"],
            ["2019-03-01", "2020-03-02"],
        ])

    def test_delni_prvi_mesec_in_prestopni_dan(self):
        serija = podatki(["2020-02-29", "2020-03-02", "2021-02-28", "2021-03-01"])
        self.assertEqual(generiraj_intervale_mesec(serija, 1), [["2020-02-29", "2021-02-28"]])

    def test_brez_celotnega_obdobja(self):
        self.assertEqual(generiraj_intervale_mesec(podatki([]), 1), [])
        self.assertEqual(generiraj_intervale_mesec(podatki(["2020-01-02", "2020-12-31"]), 1), [])

    def test_neveljavna_dolzina_ali_datumi(self):
        for interval in [0, -1, 1.5, True]:
            with self.subTest(interval=interval), self.assertRaises(ValueError):
                generiraj_intervale_mesec(podatki([]), interval)
        with self.assertRaises(ValueError):
            generiraj_intervale_mesec(podatki(["2020-02-01", "2020-01-01"]), 1)
        for interval in [0, 51, 1.5]:
            with self.subTest(interval=interval), self.assertRaises(ValidationError):
                main.podatki_iz_frontenda(zacetna_investicija=1000, mesecni_vlozek=100,
                                        indeks="S&P 500", interval=interval)

    def test_enaki_datumi_za_vse_strategije(self):
        serija = podatki(["2020-01-02", "2021-01-04"])
        with self.assertRaises(HTTPException) as error:
            main.pripravi_mesecne_intervale([serija, serija, podatki(["2020-01-03", "2021-01-04"])], 1)
        self.assertEqual(error.exception.status_code, 422)

    def test_endpointa_zavrneta_prekratko_zgodovino(self):
        serija = podatki(["2020-01-02", "2020-12-31"])
        request = main.podatki_iz_frontenda(zacetna_investicija=1000, mesecni_vlozek=100,
                                          indeks="S&P 500", interval=1)
        with patch.object(main, "pridobi_indekse", return_value=[serija] * 3):
            for path in ["/primerjava_vrstic", "/html-files"]:
                endpoint = next(route.endpoint for route in main.app.routes if route.path == path)
                with contextlib.redirect_stdout(io.StringIO()), self.assertRaises(HTTPException) as error:
                    endpoint(request)
                self.assertEqual(error.exception.status_code, 422)

    def test_tabela_csv_in_html_za_vseh_15_mesecnih_zacetkov(self):
        datumi = []
        datum = date(2020, 1, 2)
        while datum <= date(2022, 3, 5):
            if datum.weekday() < 5:
                datumi.append(datum.isoformat())
            datum += timedelta(days=1)
        serije = [podatki(datumi, donos) for donos in [0, 0.001, -0.001]]
        request = main.podatki_iz_frontenda(zacetna_investicija=1000, mesecni_vlozek=100,
                                          indeks="S&P 500", interval=1)
        # Vsi izhodi ostanejo v začasni mapi; obstoječih rezultatov se ne dotikamo.
        with tempfile.TemporaryDirectory() as folder, contextlib.chdir(folder), \
                patch.object(main, "pridobi_indekse", return_value=serije), \
                contextlib.redirect_stdout(io.StringIO()):
            endpoints = {route.path: route.endpoint for route in main.app.routes if hasattr(route, "endpoint")}
            tabela = endpoints["/primerjava_vrstic"](request)
            grafi = endpoints["/html-files"](request)["results"]
            self.assertEqual(tabela["summary"]["total_compared"], 15)
            self.assertEqual(tabela["summary"]["skupaj_investirano"], 2200)
            self.assertEqual(tabela["summary"]["vse_mesecne_investicije"], 1200)
            self.assertEqual(tabela["summary"]["wins"]["vzvod-2x.csv"]["count"], 15)
            self.assertEqual([row["graph_title"] for row in tabela["rows"]], [g["title"] for g in grafi])
            for row, graf in zip(tabela["rows"], grafi):
                with Path("rezultati-vsak-interval-vsi-indeksi", graf["title"] + ".csv").open() as f:
                    dnevni = list(csv.reader(f))
                koncne = {"osnoven.csv": float(dnevni[-1][1]),
                          "vzvod-2x.csv": float(dnevni[-1][2]),
                          "vzvod-3x.csv": float(dnevni[-1][3])}
                for rank in ["best", "second", "third"]:
                    self.assertEqual(row[rank]["total"], koncne[row[rank]["file"]])
                self.assertEqual(koncne["osnoven.csv"], 2200)
                html = Path("mapa-grafi", graf["filename"]).read_text()
                self.assertIn("2.200", html)
                self.assertIn("plotly", html)


if __name__ == "__main__":
    unittest.main()
