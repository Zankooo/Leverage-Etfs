import pandas as pd
import plotly.express as px


def narisi_tri_krivulje_na_graf(csv_path: str, output_html: str = "graf.html", 
                               naslov: str = "Tri krivulje skozi čas"):
    """
    Narise graf iz csv-ja. Format csvja more bit pa:
    date,A,B,C
    2025-02-06,6444.75,6510.10,6420.20,
    2025-02-07,6468.56,6522.40,6432.10

    Pac tri stolpci
    """
    
    
    # preberi CSV in preimenuj stolpce
    df = pd.read_csv(csv_path, parse_dates=["date"])
    df = df.rename(columns={"A": "Graf 1", "B": "Graf 2", "C": "Graf 3"})

    # osnovni graf
    fig = px.line(
        df,
        x="date",
        y=["Graf 1", "Graf 2", "Graf 3"],
        template="simple_white",
        markers=False
    )

    # stil črt in hover
    fig.update_traces(
        line=dict(width=2.5),
        hovertemplate="%{fullData.name}: %{y:,.2f} €"
    )

    # layout
    fig.update_layout(
        hovermode="x unified",
        title=dict(
            text=naslov,
            x=0.0,
            xanchor="left",
            y=0.98
        ),
        xaxis_title="Datum",
        yaxis_title="Vrednost",
        font=dict(
            family="Arial, Helvetica, sans-serif",
            size=14
        ),
        margin=dict(l=60, r=30, t=120, b=60),
        hoverlabel=dict(font_size=13),
        legend_title_text=""  # odstrani besedo "variable"
    )

    # nastavitve osi
    fig.update_xaxes(
        showgrid=True,
        gridcolor="rgba(0,0,0,0.08)",
        showspikes=True,
        spikemode="across",
        spikesnap="cursor",
        spikedash="solid"
    )
    
    fig.update_yaxes(
        showgrid=True,
        gridcolor="rgba(0,0,0,0.08)",
        tickformat=",.0f",
        zeroline=True,
        zerolinewidth=1,
        zerolinecolor="rgba(0,0,0,0.25)"
    )

    # rangeselector in legenda
    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                x=0,
                xanchor="left",
                y=1.05,
                yanchor="top",
                buttons=list([
                    dict(count=7, label="7D", step="day", stepmode="backward"),
                    dict(count=1, label="1M", step="month", stepmode="backward"),
                    dict(count=3, label="3M", step="month", stepmode="backward"),
                    dict(count=6, label="6M", step="month", stepmode="backward"),
                    dict(count=1, label="YTD", step="year", stepmode="todate"),
                    dict(count=1, label="1Y", step="year", stepmode="backward"),
                    dict(step="all", label="All")
                ])
            ),
            rangeslider=dict(visible=True)
        ),
        legend=dict(
            orientation="h",
            yanchor="top",
            y=1.0,  # legenda pod rangeselectorjem
            xanchor="left",
            x=0
        )
    )

    # shrani in odpri
    fig.write_html(output_html, auto_open=True)


# ------------------------------------------------------------------------------------------------------------------------

def narisi_en_graf(csv_path: str,
                   output_html: str = "graf_en.html",
                   naslov: str = "Graf skozi čas",
                   col_name: str | None = "A",
                   label: str = "Graf 1"):
    """
    Narise graf iz csv-ja. Format csvja more bit pa:
    date,A
    2025-02-06,6444.75,
    2025-02-07,6468.56
    Pac en stolpeec
    """
    # preberi CSV
    df = pd.read_csv(csv_path, parse_dates=["date"])

    # če ni podan col_name, vzemi prvi ne-`date` stolpec
    if col_name is None:
        col_candidates = [c for c in df.columns if c.lower() != "date"]
        if not col_candidates:
            raise ValueError("V datoteki ni stolpcev razen 'date'.")
        col_name = col_candidates[0]

    # preimenuj izbrani stolpec v prijazen label
    df = df.rename(columns={col_name: label})

    # osnovni graf (ena krivulja)
    fig = px.line(
        df, x="date", y=label,
        template="simple_white", markers=False
    )

    # stil črte in hover
    fig.update_traces(
        line=dict(width=2.5),
        hovertemplate=f"{label}: "+"%{y:,.2f} €"
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
        showlegend=False  # legenda ni potrebna za eno krivuljo
    )

    # osi + spike line
    fig.update_xaxes(showgrid=True, gridcolor="rgba(0,0,0,0.08)",
                     showspikes=True, spikemode="across", spikesnap="cursor", spikedash="solid")
    fig.update_yaxes(showgrid=True, gridcolor="rgba(0,0,0,0.08)",
                     tickformat=",.0f", zeroline=True, zerolinewidth=1, zerolinecolor="rgba(0,0,0,0.25)")

    # rangeselector pod naslovom + rangeslider
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
        )
    )

    # shrani in odpri
    fig.write_html(output_html, auto_open=True)


# narisi_en_graf("fajl-za-grafe.csv")
# narisi_tri_krivulje_na_graf("fajl-za-grafe.csv")