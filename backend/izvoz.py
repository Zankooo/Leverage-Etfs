"""CSV-izvoz že izračunanih rezultatov za pregled; brez ponovnega DCA."""

import csv
from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory
from uuid import uuid4


def izvozi_simulacijo(intervali, ciljna_mapa, parametri):
    """Shrani parametre, povzetek in dnevni CSV za vsak interval.

    Številke se izvozijo brez dodatnega zaokroževanja. Dokončana mapa
    postane vidna šele po uspešnem zapisu vseh datotek.
    """
    ciljna_mapa = Path(ciljna_mapa)
    ciljna_mapa.mkdir(parents=True, exist_ok=True)
    zdaj = datetime.now(timezone.utc)
    ime = f"{zdaj:%Y-%m-%d_%H-%M-%S}_UTC_{uuid4().hex[:12]}"
    koncna_mapa = ciljna_mapa / ime

    with TemporaryDirectory(prefix=".izvoz-", dir=ciljna_mapa) as zacasna:
        mapa = Path(zacasna)
        with (mapa / "parametri.csv").open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["parameter", "vrednost"])
            writer.writerows(parametri.items())
            writer.writerow(["ustvarjeno_utc", zdaj.isoformat()])
            writer.writerow(["stevilo_intervalov", len(intervali)])

        with (mapa / "povzetek.csv").open("w", newline="", encoding="utf-8") as f:
            povzetek = csv.writer(f)
            povzetek.writerow([
                "datum_od", "datum_do", "zacetni_vlozek", "mesecni_vlozek",
                "stevilo_mesecnih_vplacil", "skupaj_vplacano",
                "koncna_vrednost_1x", "koncna_vrednost_2x", "koncna_vrednost_3x",
                "dobicek_1x", "dobicek_2x", "dobicek_3x",
            ])
            for rezultati in intervali:
                if len(rezultati) != 3:
                    raise ValueError("CSV-izvoz potrebuje rezultate za 1x, 2x in 3x.")
                prvi = rezultati[0]
                if any(
                    r.datumi != prvi.datumi or r.vplacano_po_dnevih != prvi.vplacano_po_dnevih
                    or len(r.vrednosti) != len(prvi.datumi)
                    or len(r.vplacano_po_dnevih) != len(prvi.datumi)
                    for r in rezultati
                ):
                    raise ValueError("Datumi, vplačila ali dolžine izvoznih serij se ne ujemajo.")
                povzetek.writerow([
                    prvi.datumi[0], prvi.datumi[-1], prvi.zacetni_vlozek,
                    prvi.mesecni_vlozek, prvi.stevilo_vplacil, prvi.skupaj_vplacano,
                    *(r.koncna_vrednost for r in rezultati),
                    *(r.dobicek for r in rezultati),
                ])
                ime_csv = f"{prvi.datumi[0]}--{prvi.datumi[-1]}.csv"
                with (mapa / ime_csv).open("w", newline="", encoding="utf-8") as dnevni:
                    writer = csv.writer(dnevni)
                    writer.writerow([
                        "datum", "vrednost_1x", "vrednost_2x", "vrednost_3x", "skupaj_vplacano",
                    ])
                    writer.writerows(
                        (datum, *(r.vrednosti[i] for r in rezultati), prvi.vplacano_po_dnevih[i])
                        for i, datum in enumerate(prvi.datumi)
                    )
        mapa.rename(koncna_mapa)
    return koncna_mapa
