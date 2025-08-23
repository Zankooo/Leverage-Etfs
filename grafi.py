import pandas as pd
import plotly.express as px
import pandas as pd
import plotly.express as px
from typing import List, Optional, Dict
# to dela perfektno, 
# mores dat pa csv v takem formatu:
# date,A,B,C
# 2025-02-06,6444.75,6510.10,6420.20
# 2025-02-07,6468.56,6522.40,6432.10
# 2025-02-08,6617.75,6543.20,6454.55
# 2025-02-09,6591.32,6530.15,6460.75
# 2025-02-10,6524.19,6509.85,6415.90




# ------------------------------------------------------------------------------------------------------------



def narisi_graf(
    csv_path: str,
    columns: Optional[List[str]] = None,     # katere stolpce narisati; če None -> vsi razen 'date'
    rename_to_graf: bool = True,             # preimenuj izbrane stolpce v "Graf 1..n"
    custom_labels: Optional[Dict[str,str]] = None,  # alternativno: {"A":"Moja A", "B":"Druga"}
    naslov: str = "Več krivulj skozi čas",
    output_html: str = "graf_vec.html",
    y_tickformat: str = ",.0f",              # formatiranje Y osi
    hover_fmt: str = "%{y:,.2f}"             # format za številke v hoverju (npr. dodaj " €" če želiš)
):
    """
    Nimam pojma kako ta funkcija dela, to je chat skuhu.
    Vem sam da dela to kar hočem da dela..
    Kot parameter funkciji daš csv file ki je take oblike:
    date,A,B,C
    2025-02-06,6444.75,6510.10,6420.20
    2025-02-07,6468.56,6522.40,6432.10
    2025-02-08,6617.75,6543.20,6454.55
    2025-02-09,6591.32,6530.15,6460.75
    2025-02-10,6524.19,6509.85,6415.90
    2025-02-11,6520.28,6512.10,6409.40
    Stolpcev je poljubno ;)
    In pol ti funkcija ustvari html file in ta html je v bistvu graf
    """
    # preberi CSV
    df = pd.read_csv(csv_path, parse_dates=["date"])

    # izberi stolpce za izris
    if columns is None:
        y_cols = [c for c in df.columns if c.lower() != "date"]
    else:
        y_cols = columns

    if not y_cols:
        raise ValueError("Ni najdenih stolpcev za izris (potrebujem vsaj enega poleg 'date').")

    # po želji preimenuj stolpce
    rename_map = {}
    if custom_labels:
        rename_map.update(custom_labels)
    if rename_to_graf:
        # preimenuj le tiste, ki niso že custom-labelani
        cnt = 1
        for c in y_cols:
            if c not in rename_map:
                rename_map[c] = f"Graf {cnt}"
                cnt += 1

    if rename_map:
        df = df.rename(columns=rename_map)
        # posodobi y_cols na preimenovana imena
        y_cols = [rename_map.get(c, c) for c in y_cols]

    # osnovni graf
    fig = px.line(
        df, x="date", y=y_cols,
        template="simple_white", markers=False
    )

    # stil črt in hover
    fig.update_traces(
        line=dict(width=2.5),
        hovertemplate= hover_fmt + " $ ali €"
    )

    # layout
    fig.update_layout(
        hovermode="x unified",
        title=dict(text=naslov, x=0.0, xanchor="left", y=0.98),
        xaxis_title="Datum",
        yaxis_title="Vrednost",
        font=dict(family="Arial, Helvetica, sans-serif", size=14),
        margin=dict(l=60, r=30, t=120, b=60),
        hoverlabel=dict(font_size=13),
        legend_title_text=""   # odstrani "variable"
    )

    # osi + spike line
    fig.update_xaxes(
        showgrid=True, gridcolor="rgba(0,0,0,0.08)",
        showspikes=True, spikemode="across", spikesnap="cursor", spikedash="solid"
    )
    fig.update_yaxes(
        showgrid=True, gridcolor="rgba(0,0,0,0.08)",
        tickformat=y_tickformat,
        zeroline=True, zerolinewidth=1, zerolinecolor="rgba(0,0,0,0.25)"
    )

    # rangeselector med naslovom in legendo
    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                x=0, xanchor="left",
                y=1.05, yanchor="top",
                buttons=list([
                    dict(count=7,   label="7D",  step="day",  stepmode="backward"),
                    dict(count=1,   label="1M",  step="month",stepmode="backward"),
                    dict(count=3,   label="3M",  step="month",stepmode="backward"),
                    dict(count=6,   label="6M",  step="month",stepmode="backward"),
                    dict(count=1,   label="YTD", step="year", stepmode="todate"),
                    dict(count=1,   label="1Y",  step="year", stepmode="backward"),
                    dict(step="all",label="All")
                ])
            ),
            rangeslider=dict(visible=True)
        ),
        legend=dict(
            orientation="h",
            yanchor="top", y=1.0,  # legenda pod rangeselectorjem
            xanchor="left", x=0
        )
    )

    # shrani in odpri
    fig.write_html(output_html, auto_open=True)


# -----------------------------------------------------------------------------------
