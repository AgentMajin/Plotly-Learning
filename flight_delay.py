import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
airline_data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud'
                           '/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/airline_data.csv',
                           encoding="ISO-8859-1",
                           dtype={'Div1Airport': str, 'Div1TailNum': str,
                                  'Div2Airport': str, 'Div2TailNum': str})

app = dash.Dash(__name__)

app.layout = html.Div(children=[html.H1('Flight Details Statistics Dashboard', style={'color': '#503D36',
                                                                               'font-size': 30}),
                                html.Div(["Input Year", dcc.Input(id='input-year',
                                                                  value=2010,
                                                                  type='number',
                                                                  style={'height': '35px', 'font-size': 30})],
                                         style={'font-size': 30}),
                                html.Br(),
                                html.Br(),
                                html.Div([
                                    html.Div(dcc.Graph(id='carrier-plot')),
                                    html.Div(dcc.Graph(id='weather-plot'))
                                ], style={'display': 'flex'}),
                                html.Div([
                                    html.Div(dcc.Graph(id='nas-plot')),
                                    html.Div(dcc.Graph(id='security-plot')),
                                ], style={'display': 'flex'}),
                                html.Div(dcc.Graph(id='late-plot'),
                                         style={'width': '65%'})])


def get_graph_data(data, year):
    df = data[data['Year'] == int(year)]

    avg_carrier = df.groupby(['Month', 'Reporting_Airline'])['CarrierDelay'].mean().reset_index()
    avg_weather = df.groupby(['Month', 'Reporting_Airline'])['WeatherDelay'].mean().reset_index()
    avg_nas = df.groupby(['Month', 'Reporting_Airline'])['NASDelay'].mean().reset_index()
    avg_security = df.groupby(['Month', 'Reporting_Airline'])['SecurityDelay'].mean().reset_index()
    avg_late = df.groupby(['Month', 'Reporting_Airline'])['LateAircraftDelay'].mean().reset_index()

    return avg_carrier, avg_weather, avg_nas, avg_security, avg_late


@app.callback([
               Output(component_id='carrier-plot', component_property='figure'),
               Output(component_id='weather-plot', component_property='figure'),
               Output(component_id='nas-plot', component_property='figure'),
               Output(component_id='security-plot', component_property='figure'),
               Output(component_id='late-plot', component_property='figure'),
                Input(component_id='input-year', component_property='value'),
               ])
def return_figures(year):
    avg_carrier,avg_weather,avg_nas,avg_security,avg_late = get_graph_data(airline_data,year)

    # Create figures
    carrier_fig = px.line(avg_carrier, x='Month',y='CarrierDelay',color='Reporting_Airline',
                          title='Average carrrier delay time (minutes) by airline')

    weather_fig = px.line(avg_weather, x='Month', y='WeatherDelay', color='Reporting_Airline',
                          title='Average weather delay time (minutes) by airline')

    nas_fig = px.line(avg_nas, x='Month', y='NASDelay', color='Reporting_Airline',
                      title='Average NAS delay time (minutes) by airline')

    security_fig = px.line(avg_security, x='Month', y='SecurityDelay', color='Reporting_Airline',
                           title='Average security delay time (minutes) by airline')

    late_fig = px.line(avg_late, x='Month', y='LateAircraftDelay', color='Reporting_Airline',
                       title='Average late aircraft delay time (minutes) by airline')


    return [carrier_fig,weather_fig,nas_fig,security_fig,late_fig]

if __name__=='__main__':
    app.run_server()