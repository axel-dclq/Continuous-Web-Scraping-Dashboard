import dash
from dash import Dash, html, dcc
from dash import dash_table
from dash_table import DataTable

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# To load the data
names = ["date","world_population","male_population","female_population","birth_year_to_date","birth_today",
         "deaths_year_to_date","deaths_today","population_growth_year_to_date","population_growth_today"]

df = pd.read_csv('data.csv', delimiter=';', names = names)
def preproc(df):
    df["date"] = pd.to_datetime(df["date"])
    df.iloc[:, 1:] = df.iloc[:, 1:].apply(lambda x: x.str.replace(',', '').astype(float)) # convert to float because not possible to convert to int
preproc(df)

# To create Dash application
app = Dash(__name__)

# To create fig1
def figure1():
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
    return fig1

# To create fig2
def figure2():
    df2 = df[['date',"world_population",'population_growth_year_to_date']].copy()
    df2["population_growth"] = df2.population_growth_year_to_date / (df2.world_population - df2.population_growth_year_to_date) * 100 # population growth formula
    df2["world_population"] = df2["world_population"].apply(lambda x:x*10**-11)

    # To create area trace depending on the world population
    area_trace = go.Scatter(x=df2['date'], y=df2['world_population'], 
                            name='World&nbsp;Population', 
                            fill='tozeroy',
                            marker_color = '#146C94')

    # Create a line plot for the population growth rate
    line_trace = go.Scatter(x=df2['date'], y=df2['population_growth'], 
                            name='Population Growth year to date (%)',
                            mode='lines',
                            marker_color = '#E90064')

    # Add an invisible trace for the secondary y-axis
    invisible_trace = go.Scatter(x=df2['date'], y=[0]*len(df2), 
                                mode='markers', 
                                name='invisible', 
                                marker=dict(color='rgba(0,0,0,0)'), 
                                showlegend=False, yaxis='y2', visible=False)

    # Create the figure by combining the two traces
    fig2 = go.Figure(data=[area_trace, line_trace, invisible_trace])

    # Configure the secondary y-axis for the population growth rate axis
    fig2.add_trace(go.Scatter(x=df2['date'], y=df2['population_growth'], visible=False, yaxis='y2', showlegend=False))

    # Configure the appearance of the two y-axes
    fig2.update_layout(title_text = "Population Growth and World Population",
                  xaxis = dict(title = "Date", showgrid = False),
                  yaxis=dict(title='World Population (trillions)'), 
                  yaxis2=dict(title='Pop Growth year to date (%)',
                              overlaying='y', 
                              side='right',
                              showgrid = False),
                  font_family = "Rockwell",
                  )
    return fig2

# To create fig3
def figure3():
    df_last = df.tail(1)[['male_population', 'female_population']]
    total_population = df_last.sum().sum()

    df_last = df_last.T.reset_index()
    df_last.columns = ['gender', 'population']
    df_last['gender'] = ['Male', 'Female']

    df_last['percentage'] = df_last.sum(axis=1)/total_population*100


    # Créer un graphique Treemap avec Plotly Express
    fig = px.treemap(df_last, path=['gender'], values='percentage', 
                    color='gender', 
                    color_discrete_map={'male': 'blue', 'female': 'white'},
                    title='Comparison of the latest male and female population values as a percentage<b>',
        )



    # Configurer les étiquettes de la treemap
    fig.update_traces(texttemplate='%{label}<br>%{value:.2f}%<br>', 
                    textfont_size=50,
                    textposition = 'middle center',
                    marker=dict(colors=['#00235B', '#F7C8E0']))
    fig.update_layout(
        margin=dict(t=60, l=10, r=10, b=1),
        height=300,
        font={'family': 'Rockwell', 'size': 25, 'color': 'black'},
    )
    return fig

app.layout = html.Div(children=[
    dcc.Interval(id='interval-component', interval=1*1000*60, n_intervals=0),
    html.H1(children='World Population Satistics'),

    html.Div(children='''
        This app will be presenting visualizations of population data that includes world population, male and female population, number of births and deaths to date, and population growth to date. These graphs will give us a  clear understanding of the changes in world population  over time and provide insights into demographic trends that shape our societies. By using advanced visualization techniques, we can uncover patterns and relationships that are not always apparent in the raw data. We hope that these graphics will help us to better understand the complex dynamics of global population growth and inform us about the challenges and opportunities that lie ahead.
    '''),

    DataTable(id='table'),

    # Créer le graphique avec plotly express
    dcc.Graph(id='male-female-population-graph'),
    dcc.Graph(id='male-female-treemap-graph'),
    html.Div(children = '''
        population and growth population
    '''),
    dcc.Graph(id='world-growth-population-graph')
])

# Creation of a callback to actualize the table
@app.callback(
    dash.dependencies.Output('table', 'data'),
    [dash.dependencies.Input('interval-component', 'n_intervals')])
def update_table(n):
    global df
    df = pd.read_csv('data.csv', delimiter=';', names = names)
    preproc(df)
    return df.tail().to_dict('records')

@app.callback(
    dash.dependencies.Output('male-female-population-graph', 'figure'),
    [dash.dependencies.Input('interval-component', 'n_intervals')])
def update_fig1(n):
    global df
    df = pd.read_csv('data.csv', delimiter=';', names = names)
    preproc(df)
    fig = figure1()
    return fig

@app.callback(
    dash.dependencies.Output('world-growth-population-graph', 'figure'),
    [dash.dependencies.Input('interval-component', 'n_intervals')])
def update_fig2(n):
    global df
    df = pd.read_csv('data.csv', delimiter=';', names = names)
    preproc(df)
    fig = figure2()
    return fig

@app.callback(
    dash.dependencies.Output('male-female-treemap-graph', 'figure'),
    [dash.dependencies.Input('interval-component', 'n_intervals')])
def update_fig3(n):
    global df
    df = pd.read_csv('data.csv', delimiter=';', names = names)
    preproc(df)
    fig = figure3()
    return fig




if __name__ == '__main__':
    app.run_server(debug=True)
