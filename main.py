import dash
from dash import Dash, html, dcc
from dash import dash_table
from dash_table import DataTable

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import time

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

# To create male female istogram comparison
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

# To create world population and population growth
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

# To create male female treemap comparison
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
        font={'family': 'Rockwell', 'size': 16, 'color': 'black'},
    )
    return fig

# To create birth and death graph
def figure4():
    # Birth graph
    trace1 = go.Scatter(
        x=df["date"],
        y=df["birth_today"],
        name="Naissances"
    )

    # Death graph
    trace2 = go.Scatter(
        x=df["date"],
        y=df["deaths_today"],
        name="Deaths"
    )

    # Growth graph
    trace3 = go.Scatter(
        x=df["date"],
        y=df["population_growth_today"],
        name="Population growth"
    )

    # Create figure
    fig = go.Figure(data=[trace1, trace2, trace3])

    fig.update_layout(
        title="Comparison of births and deaths over time",
        xaxis=dict(title="Date",showgrid = False),
        yaxis=dict(title="Body count"),
        barmode="group",
        font_family = "Rockwell"
    )
    return fig

app.layout = html.Div(children=[
    dcc.Interval(id='interval-component', interval=1*1000*60, n_intervals=0),
    html.H1(children='World Population Statistics'),

    html.Div(children='''
        This app will be presenting visualizations of population data that includes world population, male and female population, 
        number of births and deaths to date, and population growth to date. These graphs will give us a  clear understanding of 
        the changes in world population  over time and provide insights into demographic trends that shape our societies. 
        By using advanced visualization techniques, we can uncover patterns and relationships that are not always apparent 
        in the raw data. We hope that these graphics will help us to better understand the complex dynamics of global 
        population growth and inform us about the challenges and opportunities that lie ahead.

    '''),

    html.Br(),

    html.H2(children = 'Last datas fetched'),
    DataTable(id='table'),

    # dcc.Graph(id='male-female-population-graph'),

    html.Br(),

    dcc.Graph(id='male-female-treemap-graph',
              figure = figure3()),
    html.Div(children = '''
        The population of men and women is equal, with an approximately 50-50 split between the two genders. 
        This balance is an important indicator of gender equality and is often used as a measure of social 
        progress. A balanced gender ratio ensures that both men and women have equal access to resources and
          opportunities, which is essential for building a fair and just society. It also promotes a diverse 
          and inclusive community that values the contributions of all individuals, regardless of their gender.
    '''),
    dcc.Graph(id='world-growth-population-graph'),

    html.Div(children = """
    Here is a comment on the population growth chart. As we know, the population has been steadily increasing over the years,
      with a significant spike in growth rate in the past few decades. This is largely due to advancements in medical technology 
      and increased access to healthcare, which has resulted in lower infant mortality rates and increased life expectancy. 
      While this growth in population can have positive economic and social impacts, it also puts a strain on resources and can 
      lead to environmental challenges. It is important for policymakers to take this into consideration and develop sustainable solutions 
      to accommodate the growing population while also preserving the planet's natural resources.
    """),

    html.Br(),
    dcc.Graph(id='birth-death-graph'),
    html.Div(children = """
    We can see that the number of births has been consistently higher than the number of deaths over the years, indicating an overall 
    increase in population. However, there are some periods where the difference between births and deaths is smaller, or even negative,
      which could be due to various factors such as economic downturns, natural disasters, or health epidemics. It is important to note 
      that the balance between births and deaths can have significant implications for a country's demographic and economic profile, and
        policymakers need to carefully consider this when developing policies related to healthcare, education, and social welfare. Overall, 
        this graph highlights the importance of understanding the dynamics of population growth and the factors that contribute to it, in order 
        to make informed decisions for the future.
    """)
])


# Callback table
@app.callback(
    dash.dependencies.Output('table', 'data'),
    dash.dependencies.Input('interval-component', 'n_intervals'))
def update_table(n):
    global df
    df = pd.read_csv('data.csv', delimiter=';', names = names)
    preproc(df)
    return df.tail().to_dict('records')

# @app.callback(
#     dash.dependencies.Output('male-female-population-graph', 'figure'),
#     [dash.dependencies.Input('interval-component', 'n_intervals')])
# def update_fig1(n):
#     global df
#     df = pd.read_csv('data.csv', delimiter=';', names = names)
#     preproc(df)
#     fig = figure1()
#     return fig

# Callback world population
@app.callback(
    dash.dependencies.Output('world-growth-population-graph', 'figure'),
    dash.dependencies.Input('interval-component', 'n_intervals'))
def update_fig2(n):
    global df
    df = pd.read_csv('data.csv', delimiter=';', names = names)
    preproc(df)
    fig = figure2()
    return fig

# Callback treemap
# @app.callback(
#     dash.dependencies.Output('male-female-treemap-graph', 'figure'),
#     dash.dependencies.Input('interval-component', 'n_intervals'))
# def update_fig3(n):
#     global df
#     df = pd.read_csv('data.csv', delimiter=';', names = names)
#     preproc(df)
#     fig = figure3()
#     return fig

# Callback birth/death
@app.callback(
    dash.dependencies.Output('birth-death-graph', 'figure'),
    dash.dependencies.Input('interval-component', 'n_intervals'))
def update_fig4(n):
    global df
    df = pd.read_csv('data.csv', delimiter=';', names = names)
    preproc(df)
    fig = figure4()
    return fig


if __name__ == '__main__':
    app.run_server(debug=True, host = '0.0.0.0')
