from dash import dash, html, dcc, callback, Output, Input
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

df = pd.read_csv("a07_data.csv")
df_amt = df["Winner"].value_counts().reset_index()
df_amt.columns = ["Country", "Won"]

#a
figA = px.choropleth(
    df_amt,
    locations="Country",
    locationmode="ISO-3",
    color="Won",
    color_continuous_scale="blugrn",
    title="FIFA Soccer World Cup Winners",
    width = 1250,
    height = 525
)

figA.update_layout(
    coloraxis_colorbar=dict(
        tickvals = [1, 2, 3, 4, 5],
        title = "Legend"
    )
)

#b
figB = px.choropleth(
    df_amt,
    locations="Country",
    locationmode="ISO-3",
    color="Won",
    color_continuous_scale="Plasma",
    animation_frame="Country",
    title="FIFA Soccer World Cup Times Won",
    width = 1250,
    height = 600
)

figB.update_layout(
    coloraxis_showscale=False,
    annotations= [go.layout.Annotation(
            text=f"BRA has won 5 times!",
            x=0.99, y=0.95,
            xref="paper", yref="paper",
            showarrow=False,
            font=dict(size=15, color="black"),
        )])

for frame in figB.frames:
    country = frame.name
    win = df_amt.loc[df_amt["Country"] == "BRA"]["Won"].values[0]
    frame.layout.annotations = [
        go.layout.Annotation(
            text=f"{country} has won {win} times!",
            x=0.99, y=0.95,
            xref="paper", yref="paper",
            showarrow=False,
            font=dict(size=15, color="black"),
        )
    ]

#c
'''
df["Color"] = 0
figC1 = px.choropleth(
    df,
    locations="Winner",
    locationmode="ISO-3", 
    color = "Color",
    color_continuous_scale="Viridis",
    animation_frame="Year",
    title="FIFA Soccer World Cup Winners",
    hover_data = {"Color" : False}
)

figC2 = px.choropleth(
    df,
    locations="Runner",
    locationmode="ISO-3",
    color="Color",
    color_continuous_scale="Plasma",
    animation_frame="Year",
    title="FIFA Soccer World Cup Winners",
    hover_data = {"Color" : False}
)
'''

df_c = (df.melt(id_vars=["Year"])).sort_values(by=["Year", "variable"])
df_c["Color"] = [i % 2 for i in range(len(df_c))]
df_c = df_c.rename(columns={"value" : "Country", "variable" : "Place"})

figC = px.choropleth(
    df_c,
    locations="Country",
    color="Color",
    color_continuous_scale=[[0,"red"], [1,"green"]],
    animation_frame="Year",
    hover_data = {"Color" : False, "Year" : False, "Place" : True},
    title="FIFA Soccer World Cup Winners and Runners in 1930",
    width = 1250,
    height = 600
)

for frame in figC.frames:
    year = frame.name
    frame.layout = {"title": f"FIFA Soccer World Cup Winners and Runners in {year}"}

figC.update_layout(
    coloraxis_colorbar=dict(
        tickvals = [0, 1], 
        ticktext = ["Runner", "Winner"],
        title = "Legend"
    )
)

app = dash.Dash()
server = app.server
app.layout = ([
    html.H1("Choropleth Maps of FIFA Soccer World Cup"),
    dcc.Dropdown(
        id="type",
        options=[
            {"label": "All winners", "value": "graphA"},
            {"label": "Times won by country", "value": "graphB"},
            {"label": "Winners and runner ups by year", "value": "graphC"}
        ], 
        value="graphA",
        style={"width": 1250}
        ),

    dcc.Graph(id="map"),
])

@callback(
    Output("map", "figure"),
    Input("type", "value")
)

def update_graph(type):
    if type == "graphA":
        return figA
    elif type == "graphB":
        return figB
    else:
        return figC
    
if __name__ == "__main__":
    app.run(debug=True)
