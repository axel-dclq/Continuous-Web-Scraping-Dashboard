from dash import Dash, html, dcc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

#%% Charger les données
names = ["date","world_population","male_population","female_population","birth_year_to_date","birth_today",
         "deaths_year_to_date","deaths_today","population_growth_year_to_date","population_growth_today"]

df = pd.read_csv('data.csv', delimiter=';', names = names)

df["date"] = pd.to_datetime(df["date"])
df.iloc[:, 1:] = df.iloc[:, 1:].apply(lambda x: x.str.replace(',', '').astype(float)) # convert to float because not possible to convert to int

# Créer une application Dash
app = Dash(__name__)

#%% FIG1
fig1 = go.Figure()
fig1.add_trace(go.Histogram(x = df["date"],
                           y = df["male_population"]*10**-9,
                           histfunc = "sum",
                           name = 'Male population',
                           marker_color = '#000080'
                           # xbins = dict(size = 10000)
                           ))
fig1.add_trace(go.Histogram(x = df["date"],
                           y = df["female_population"]*10**-9,
                           histfunc = "sum",
                           name = 'Female population',
                           marker_color = "#FF1493"))

fig1.update_layout(title_text = "Male/Female population comparaison",
                  xaxis_title_text = "Date",
                  yaxis_title_text = 'Population (in billion)',
                  font_family = "Rockwell")
### END FIG1 ###

#%% FIG2
df2 = df[['date',"world_population",'population_growth_year_to_date']].copy()
df2["population_growth"] = df2.population_growth_year_to_date / (df2.world_population - df2.population_growth_year_to_date) * 100
df2["world_population"] = df2["world_population"].apply(lambda x:x*10**-11)

area_trace = go.Scatter(x=df2['date'], y=df2['world_population'], 
                        name='World&nbsp;Population', 
                        fill='tozeroy',
                        marker_color = '#146C94')

# Créer une trace en ligne pour le taux de croissance de la population
line_trace = go.Scatter(x=df2['date'], y=df2['population_growth'], 
                        name='Population Growth year to date (%)',
                        mode='lines',
                        marker_color = '#E90064')

# Ajouter une trace invisible pour l'axe y secondaire
invisible_trace = go.Scatter(x=df2['date'], y=[0]*len(df2), 
                             mode='markers', 
                             name='invisible', 
                             marker=dict(color='rgba(0,0,0,0)'), 
                             showlegend=False, yaxis='y2', visible=False)


# Créer la figure en combinant les deux traces
fig2 = go.Figure(data=[area_trace, line_trace, invisible_trace])

# Configurer l'axe y secondaire pour l'axe du taux de croissance de la population
fig2.add_trace(go.Scatter(x=df2['date'], y=df2['population_growth'], visible=False, yaxis='y2', showlegend=False))

# Configurer l'aspect des deux axes y
fig2.update_layout(title_text = "Population Growth and World Population",
                  xaxis = dict(title = "Date", showgrid = False),
                  yaxis=dict(title='World Population (trillions)'), 
                  yaxis2=dict(title='Pop Growth year to date (%)',
                              overlaying='y', 
                              side='right',
                              showgrid = False),
                  font_family = "Rockwell",
                  )
### END FIG2###

#%% 
app.layout = html.Div(children=[
    html.H1(children='World Population Satistics'),

    html.Div(children='''
        This app will be presenting visualizations of population data that includes world population, male and female population, number of births and deaths to date, and population growth to date. These graphs will give us a  clear understanding of the changes in world population  over time and provide insights into demographic trends that shape our societies. By using advanced visualization techniques, we can uncover patterns and relationships that are not always apparent in the raw data. We hope that these graphics will help us to better understand the complex dynamics of global population growth and inform us about the challenges and opportunities that lie ahead.
    '''),

    # Créer le graphique avec plotly express
    dcc.Graph(
        id='male-female-population-graph',
        
        figure = fig1
    ),
    html.Div(children = '''
        population and growth population
    '''),
    dcc.Graph(
        id='world-growth-population-graph',
        
        figure = fig2
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
