import pandas as pd
import dash
import plotly
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

airline_data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/'
                            'IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/airline_data.csv',
                            encoding = 'ISO-8859-1',
                            dtype={'Div1Airport': str, 'Div1TailNum': str,
                                   'Div2Airport': str, 'Div2TailNum': str})

app = dash.Dash(__name__)

app.layout = html.Div(children= [html.H1('Airline Performance Dashboard', style={'textAlign': 'center',
                                                                                 'color': '#503D36',
                                                                                 'font-size': 40}),
                                 html.Div(['Input Years',dcc.Input(id = 'input-year', value = '2010',
                                                                   type = 'number',
                                                                   style = {'height': '50px', 'font-size':35})],
                                          style={'font-size': 40}),
                                 html.Br(),
                                 html.Br(),
                                 html.Div(dcc.Graph(id = 'line-plot')),
                                 ])
if __name__ == '__main__':
    app.run_server()
