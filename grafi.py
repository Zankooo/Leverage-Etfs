import pandas as pd
import plotly.express as px

# to dela perfektno, 
# mores dat pa csv v takem formatu:
# date,A,B,C
# 2025-02-06,6444.75,6510.10,6420.20
# 2025-02-07,6468.56,6522.40,6432.10
# 2025-02-08,6617.75,6543.20,6454.55
# 2025-02-09,6591.32,6530.15,6460.75
# 2025-02-10,6524.19,6509.85,6415.90

# tukaj dolocis ime csv
df = pd.read_csv("fajl-za-grafe.csv", parse_dates=["date"])
df = df.rename(columns={"A": "Graf 1", "B": "Graf 2", "C": "Graf 3"})

fig = px.line(
    df, x="date", y=["Graf 1", "Graf 2", "Graf 3"],
    template="simple_white", markers=False
)

fig.update_traces(line=dict(width=2.5),
                  hovertemplate="%{fullData.name}: %{y:,.2f} €")

fig.update_layout(
    hovermode="x unified",
    title=dict(text="Tri krivulje skozi čas", x=0.0, xanchor="left", y=0.98),
    xaxis_title="Datum",
    yaxis_title="Vrednost",
    font=dict(family="Arial, Helvetica, sans-serif", size=14),
    margin=dict(l=60, r=30, t=120, b=60),
    hoverlabel=dict(font_size=13),
    legend_title_text=""   # <<<<< to odstrani besedo "variable"
)

fig.update_xaxes(showgrid=True, gridcolor="rgba(0,0,0,0.08)",
                 showspikes=True, spikemode="across", spikesnap="cursor", spikedash="solid")
fig.update_yaxes(showgrid=True, gridcolor="rgba(0,0,0,0.08)",
                 tickformat=",.0f", zeroline=True, zerolinewidth=1, zerolinecolor="rgba(0,0,0,0.25)")

# >>> rangeselector med naslovom in legendo
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

fig.write_html("graf_pro.html", auto_open=True)
