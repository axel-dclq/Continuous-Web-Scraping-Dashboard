from dash import Dash, html, dcc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Charger les données
names = ["date","world_population","male_population","female_population","birth_year_to_date","birth_today",
         "deaths_year_to_date","deaths_today","population_growth_year_to_date","population_growth_today"]

df = pd.read_csv('data.csv', delimiter=';', names = names)

df["date"] = pd.to_datetime(df["date"])
df.iloc[:, 1:] = df.iloc[:, 1:].apply(lambda x: x.str.replace(',', '').astype(float)) # convert to float because not possible to convert to int

# Créer une application Dash
app = Dash(__name__)

# Créer une mise en page simple pour le graphique
fig = go.Figure()
fig.add_trace(go.Histogram(x = df["date"],
                           y = df["male_population"]*10**-9,
                           histfunc = "sum",
                           name = 'Male population',
                           marker_color = '#000080'
                           # xbins = dict(size = 10000)
                           ))
fig.add_trace(go.Histogram(x = df["date"],
                           y = df["female_population"]*10**-9,
                           histfunc = "sum",
                           name = 'Female population',
                           marker_color = "#FF1493"))

fig.update_layout(title_text = "Male/Female population comparaison",
                  xaxis_title_text = "Date",
                  yaxis_title_text = 'Population (in billion)',
                  font_family = "Rockwell")

app.layout = html.Div(children=[
    html.H1(children='Population mondiale'),

    html.Div(children='''
        Evolution de la population mondiale au fil du temps.
    '''),

    # Créer le graphique avec plotly express
    dcc.Graph(
        id='world-population-graph',
        # figure={
        #     'data': [
        #         {'x': df['date'], 'y': df['world_population'], 'type': 'line', 'name': 'Population mondiale'},
        #     ],
        #     'layout': {
        #         'title': 'Population mondiale',
        #         'xaxis': {'title': 'Date'},
        #         'yaxis': {'title': 'Population'}
        #     }
        # }
        figure = fig
    ),
    dcc.Graph(
        id='world-population-graph',
        # figure={
        #     'data': [
        #         {'x': df['date'], 'y': df['world_population'], 'type': 'line', 'name': 'Population mondiale'},
        #     ],
        #     'layout': {
        #         'title': 'Population mondiale',
        #         'xaxis': {'title': 'Date'},
        #         'yaxis': {'title': 'Population'}
        #     }
        # }
        figure = fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
