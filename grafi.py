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



def narisi_logaritmicne_grafe(
    zacetna_investicija,
    mesecna_investicija,
    vse_investicije_skupaj,
    csv_path: str,
    columns: Optional[List[str]] = None,
    rename_to_graf: bool = True,
    custom_labels: Optional[Dict[str,str]] = None,

    output_html: str = "graf_vec.html",
    y_tickformat: str = ",.0f",
    hover_fmt: str = "%{y:,.2f}"
):
    def fmt_eu_intbold_html(x, decimals=2, int_color="#111", dec_color="#111"):
        try:
            val = float(x)
        except (TypeError, ValueError):
            return str(x)
        s = f"{val:,.{decimals}f}"
        s_eu = s.replace(",", "X").replace(".", ",").replace("X", ".")
        if "," in s_eu:
            int_part, dec_part = s_eu.split(",")
            return (
                f"<b style='font-weight:700; color:{int_color}'>{int_part}</b>"
                f"<span style='font-weight:400; color:{dec_color}'>,{dec_part}</span>"
            )
        else:
            return f"<b style='font-weight:700; color:{int_color}'>{s_eu}</b>"

    df = pd.read_csv(csv_path, parse_dates=["date"])

    if columns is None:
        y_cols = [c for c in df.columns if c.lower() != "date"]
    else:
        y_cols = columns
    if not y_cols:
        raise ValueError("Ni najdenih stolpcev za izris (potrebujem vsaj enega poleg 'date').")

    rename_map: Dict[str, str] = {}
    if custom_labels:
        rename_map.update(custom_labels)

    if rename_to_graf:
        fixed_names = ["Osnoven indeks", "Vzvod 2x", "Vzvod 3x"]
        for i, c in enumerate(y_cols):
            if i < len(fixed_names):
                rename_map[c] = fixed_names[i]
            else:
                rename_map[c] = f"Graf {i+1}"  # če bi bilo stolpcev več kot 3

    if rename_map:
        df = df.rename(columns=rename_map)
        y_cols = [rename_map.get(c, c) for c in y_cols]

    if (df[y_cols] <= 0).to_numpy().any():
        raise ValueError("Logaritmična os Y zahteva pozitivne vrednosti (> 0) v vseh izbranih stolpcih.")

    color_seq = ["rgb(166,130,255)", "rgb(85,193,255)", "rgb(255,183,3)"]
    color_seq = color_seq[:len(y_cols)]

    fig = px.line(
        df, x="date", y=y_cols,
        template="simple_white", markers=False,

        color_discrete_sequence=color_seq
    )

    for i in range(min(len(fig.data), len(color_seq))):
        fig.data[i].line.color = color_seq[i]

    fig.update_layout(
        hovermode="x unified",
        xaxis_title="Datum",
        yaxis_title="Vrednost (log)",
        font=dict(family="Arial, Helvetica, sans-serif", size=14),
        margin=dict(l=60, r=30, t=190, b=80),
        hoverlabel=dict(font_size=13, namelength=-1),
        legend_title_text="",
        separators=",."
    )

    fig.update_xaxes(
        showgrid=True, gridcolor="rgba(0,0,0,0.08)",
        showspikes=True, spikemode="across", spikesnap="cursor", spikedash="solid",
        tickformat="%d.%m.%Y",
        hoverformat="%d.%m.%Y",
        rangeslider=dict(visible=True, thickness=0.08, bgcolor="rgba(108,99,255,0.08)")
    )
    fig.update_yaxes(
        type="log",
        showgrid=True, gridcolor="rgba(0,0,0,0.08)",
        tickformat=y_tickformat,
        zeroline=False
    )

    dolar = "<span style='font-weight:400; color:#111'> $</span>"
    for i, col in enumerate(y_cols):
        values_html = [fmt_eu_intbold_html(v, 2) + dolar for v in df[col].tolist()]
        fig.data[i].customdata = values_html
        fig.data[i].hovertemplate = "<b>%{fullData.name}</b>: %{customdata}<extra></extra>"

    start_date_str = pd.to_datetime(df["date"].min()).strftime("%d.%m.%Y")
    end_date_str   = pd.to_datetime(df["date"].max()).strftime("%d.%m.%Y")

    z_html = fmt_eu_intbold_html(zacetna_investicija, 2) + dolar
    m_html = fmt_eu_intbold_html(mesecna_investicija, 2) + dolar
    s_html = fmt_eu_intbold_html(vse_investicije_skupaj, 2) + dolar

    color_seq = ["rgb(166,130,255)", "rgb(85,193,255)", "rgb(255,183,3)"][:len(y_cols)]
    label_colors = dict(zip(y_cols, color_seq))

    last_row = df.iloc[-1]
    finals_parts = []
    for col in y_cols:
        colored_label = f"<span style='color:{label_colors[col]}; font-weight:700'>{col}</span>"
        value_html = fmt_eu_intbold_html(last_row[col], 2) + dolar
        finals_parts.append(f"{colored_label}: {value_html}")
    finals_html = " &nbsp;•&nbsp; ".join(finals_parts)

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
            f"🗓️ {start_date_str} "
            f"<span style='color:#9AA0A6'>→</span> "
            f"{end_date_str}"
            f"</span><br>"
            f"<span style='font-size:21px; color:#444'>"
            f"💰 Začetna investicija: {z_html} &nbsp;•&nbsp; "
            f"📈 Mesečne investicije: {m_html} &nbsp;•&nbsp; "
            f"Σ Vse skupaj: {s_html}"
            f"</span><br>"
            f"<span style='font-size:21px; color:#444'>"
            f"🏁 Končne vrednosti: {finals_html}"
            f"</span>"
        )
    )

    fig.write_html(output_html, auto_open=True)



