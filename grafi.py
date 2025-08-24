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



def narisi_navadne_grafe(
    csv_path: str,
    columns: Optional[List[str]] = None,     # katere stolpce narisati; če None -> vsi razen 'date'
    rename_to_graf: bool = True,             # preimenuj izbrane stolpce v "Graf 1..n"
    custom_labels: Optional[Dict[str,str]] = None,  # alternativno: {"A":"Moja A", "B":"Druga"}
    naslov: str = "Več krivulj skozi čas",
    output_html: str = "graf_vec.html",
    y_tickformat: str = ",.0f",              # formatiranje Y osi
    hover_fmt: str = "%{y:,.2f}"             # format za številke v hoverju (npr. dodaj " €" če želiš)
):
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
    rename_map: Dict[str, str] = {}
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
        margin=dict(l=60, r=30, t=150, b=60),   # ↑ več prostora zgoraj
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

    # ➕ NAPIS NAD GRAFOM (rahlo nižje, da je viden)
    start_date_str = pd.to_datetime(df["date"].min()).strftime("%Y-%m-%d")
    end_date_str   = pd.to_datetime(df["date"].max()).strftime("%Y-%m-%d")

    fig.add_annotation(
        x=0.5, y=1.07,               # sredinsko nad grafom
        xref="paper", yref="paper",
        xanchor="center", yanchor="bottom",
        text=f"<b style='font-size:18px'>{start_date_str} → {end_date_str}</b>",
        showarrow=False, align="center",
        bgcolor="rgba(255,255,255,0.95)",
        bordercolor="rgba(0,0,0,0.2)", borderwidth=1, borderpad=6,
        font=dict(size=18)
    )

    # shrani in odpri
    fig.write_html(output_html, auto_open=True)


# -----------------------------------------------------------------------------------


# LOGARITMICNA, KER ZGORNJA JE NAVADNA



from typing import Optional, List, Dict
import pandas as pd
import plotly.express as px

def narisi_logaritmicne_grafe(
    zacetna_investicija,
    mesecna_investicija,
    vse_investicije_skupaj,
    csv_path: str,
    columns: Optional[List[str]] = None,     # katere stolpce narisati; če None -> vsi razen 'date'
    rename_to_graf: bool = True,             # preimenuj izbrane stolpce v "Graf 1..n"
    custom_labels: Optional[Dict[str,str]] = None,  # alternativno: {"A":"Moja A", "B":"Druga"}
    naslov: str = "Več krivulj skozi čas (log skala)",
    output_html: str = "graf_vec.html",
    y_tickformat: str = ",.0f",              # formatiranje Y osi (d3-format; separators poskrbi za EU)
    hover_fmt: str = "%{y:,.2f}"             # format za številke v hoverju (EU z separators)
):
    # EU format helper (npr. 12.345,67)
    def fmt_eu(x, decimals=2):
        try:
            x = float(x)
        except (TypeError, ValueError):
            return str(x)
        s = f"{x:,.{decimals}f}"
        return s.replace(",", "X").replace(".", ",").replace("X", ".")

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
    rename_map: Dict[str, str] = {}
    if custom_labels:
        rename_map.update(custom_labels)
    if rename_to_graf:
        cnt = 1
        for c in y_cols:
            if c not in rename_map:
                rename_map[c] = f"Graf {cnt}"
                cnt += 1
    if rename_map:
        df = df.rename(columns=rename_map)
        y_cols = [rename_map.get(c, c) for c in y_cols]

    # varovalo za log skalo
    if (df[y_cols] <= 0).to_numpy().any():
        raise ValueError("Logaritmična os Y zahteva pozitivne vrednosti (> 0) v vseh izbranih stolpcih.")

    # osnovni graf
    fig = px.line(
        df, x="date", y=y_cols,
        template="simple_white", markers=False
    )

    # stil črt in hover (EU format bo prek layout.separators)
    fig.update_traces(
        line=dict(width=2.5),
        hovertemplate= hover_fmt + " $ ali €"
    )

    # layout
    fig.update_layout(
        hovermode="x unified",
        xaxis_title="Datum",
        yaxis_title="Vrednost (log)",
        font=dict(family="Arial, Helvetica, sans-serif", size=14),
        margin=dict(l=60, r=30, t=190, b=60),   # več prostora zgoraj za daljši tekst
        hoverlabel=dict(font_size=13),
        legend_title_text="",
        separators=",."  # KLJUČNO: decimalna vejica, tisočice s piko
    )

    # osi + spike line
    fig.update_xaxes(
        showgrid=True, gridcolor="rgba(0,0,0,0.08)",
        showspikes=True, spikemode="across", spikesnap="cursor", spikedash="solid",
        tickformat="%d.%m.%Y",   # EU datum na osi
        hoverformat="%d.%m.%Y"   # EU datum v hover headerju
    )
    fig.update_yaxes(
        type="log",                   # log skala
        showgrid=True, gridcolor="rgba(0,0,0,0.08)",
        tickformat=y_tickformat,
        zeroline=False
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
                    dict(count=1,   label="1Y",  step="year",  stepmode="backward"),
                    dict(step="all",label="All")
                ])
            ),
            rangeslider=dict(visible=True)
        ),
        legend=dict(
            orientation="h",
            yanchor="top", y=1.0,
            xanchor="left", x=0
        )
    )

    # ➕ NAPIS NAD GRAFOM: datumi + tri vrednosti + končni tečaji vseh serij
    start_date_str = pd.to_datetime(df["date"].min()).strftime("%d.%m.%Y")
    end_date_str   = pd.to_datetime(df["date"].max()).strftime("%d.%m.%Y")

    z_str = f"{fmt_eu(zacetna_investicija, 2)} €"
    m_str = f"{fmt_eu(mesecna_investicija, 2)} €"
    s_str = f"{fmt_eu(vse_investicije_skupaj, 2)} €"

    # končni tečaji (zadnja vrstica) za vsako serijo v y_cols
    last_row = df.iloc[-1]
    finals_str = " &nbsp;•&nbsp; ".join(
        f"{col}: {fmt_eu(last_row[col], 2)} €" for col in y_cols
    )

    # fancy napis nad grafom (z EU številkami in datumi)
    fig.add_annotation(
        x=0.5, y=1.08,
        xref="paper", yref="paper",
        xanchor="center", yanchor="bottom",
        showarrow=False, align="center",
        bgcolor="rgba(255,255,255,0.96)",
        bordercolor="rgba(0,0,0,0.15)", borderwidth=1, borderpad=10,
        font=dict(size=18),
        text=(
            f"<span style='font-size:26px; font-weight:800'>"
            f"🗓️ <span style='color:#6C63FF'>{start_date_str}</span> "
            f"<span style='color:#9AA0A6'>→</span> "
            f"<span style='color:#6C63FF'>{end_date_str}</span>"
            f"</span><br>"
            f"<span style='font-size:21px; color:#444'>"
            f"💰 Začetna investicija: <b style='color:#111'>{z_str}</b> &nbsp;•&nbsp; "
            f"📈 Mesečne investicije: <b style='color:#111'>{m_str}</b> &nbsp;•&nbsp; "
            f"Σ Vse skupaj: <b style='color:#111'>{s_str}</b>"
            f"</span><br>"
            f"<span style='font-size:21px; color:#444'>"
            f"🏁 Končne vrednosti: <b style='color:#111'>{finals_str}</b>"
            f"</span>"
        )
    )

    # shrani in odpri (separators poskrbi za EU ločila na osi in v hoverju)
    fig.write_html(output_html, auto_open=True)

