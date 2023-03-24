import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

# Charger les données
names = ["date","world_population","male_population","female_population","birth_year_to_date","birth_today","deaths_year_to_date","deaths_today","population_growth_year_to_date","population_growth_today"]
df = pd.read_csv('data.csv', delimiter=';', names = names)
df["date"] = pd.to_datetime(df["date"])
df.iloc[:, 1:] = df.iloc[:, 1:].apply(lambda x: x.str.replace(',', '').astype(float)) # convertir en float

# Créer une application Dash
app = dash.Dash(__name__)

# Créer une mise en page simple pour le graphique
app.layout = html.Div(children=[
    html.H1(children='Population mondiale'),

    html.Div(children='''
        Evolution de la population mondiale au fil du temps.
    '''),

    # Créer le graphique avec plotly express
    dcc.Graph(
        id='world-population-graph',
        figure={
            'data': [
                {'x': df['date'], 'y': df['world_population'], 'type': 'line', 'name': 'Population mondiale'},
            ],
            'layout': {
                'title': 'Population mondiale',
                'xaxis': {'title': 'Date'},
                'yaxis': {'title': 'Population'}
            }
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
