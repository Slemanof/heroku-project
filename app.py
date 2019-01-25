import os
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import numpy as np
import pandas as pd
import plotly.graph_objs as go
#Declaring Dataset from CVS file uploaded on my Github Python
data_ica = pd.read_csv('https://raw.githubusercontent.com/Slemanof/Python1/master/SPIndex.csv')
#Having the firt Column as the Index
index_col=0
#Extracting dates from Dateset
def extract_year(column):
    return column.split('/')[2]
def extract_month(column):
    return column.split('/')[0]
data_ica['year'] = data_ica['Date'].apply(extract_year)
data_ica['month'] = data_ica['Date'].apply(extract_month)
#Calling Dash app HTML
app = dash.Dash(__name__)
server = app.server
server.secret_key = os.environ.get('SECRET_KEY', 'my-secret-key')
#Defining the layout of the output
app.layout = html.Div(children=[
    html.H1(
        children='S&P 500 Historical Data'
    ),
    dcc.Markdown('''
The Data and the Graphs shows the historical data of S&P 500 Index which is for the American stocks from dates
1/3/2000 to 12/5/2017.
The Data are Historical data of S&P Index from 2000 to 2017 downloaded from Yahoo Finance API.
Dataset could be found here:[Link](https://www.kaggle.com/adityarajuladevi/sp-index-historical-data)
Project for Programmin Fundamentals done by [*Sulieman Al Rustom*](https://github.com/Slemanof/heroku-project) (Prague College).
Dataset info:
Number of Columns: *7*
Number of Raws: *4511*
    '''
#Setting up a dropdown list containing the 4 types of charts.
    ),
    html.Div(children=[
        dcc.Dropdown(
            id='dropinput',
            options=[
                {'label': 'S&P OHLC of the Value', 'value': 'ohlc'},
                {'label': 'S&P Scatter Volume Data', 'value': 'scatter'},
                {'label': 'S&P Volume Heatmap', 'value': 'heatmap'},
				{'label': 'S&P CandelStick Historical Data', 'value': 'candlestick'}
            ],
            value='scatter'
    ),
        dcc.Graph(id= 'graph')
    ])
])

@app.callback(
    Output(component_id='graph', component_property='figure'),
    [Input(component_id='dropinput', component_property='value')]
)
#OHLC Chart
def update_graph(input_value):
    if input_value == 'ohlc':
        trace = go.Ohlc(x=data_ica['Date'],
                        open=data_ica['open'],
                        high=data_ica['high'],
                        low=data_ica['low'],
                        close=data_ica['close'])
        layout = go.Layout(
            title='S&P OHLC of the Value',
            showlegend=False,
            xaxis=dict(
                title="Date"),
            yaxis=dict(
                title="Value"),
                height = 800,
                width = 1500
        )
        data = [trace]
        fig = go.Figure(data=data, layout=layout)
#Scatter Chart
    elif input_value == 'scatter':
        trace1 = go.Scatter(
            y=data_ica.volume,
            x=data_ica.Date,
            name='Volume',
            mode='markers'

        )
        layout = go.Layout(
            title='S&P Scatter Volume Data',
            showlegend=False,
            xaxis=dict(
                title="Date"),
            yaxis=dict(
                title="Volume")
        )
        data = [trace1]
        fig = dict(data=data, layout=layout)
#Heatmap Chart
    elif input_value == 'heatmap':
        trace = go.Heatmap(
                z = data_ica.volume,
                x = data_ica.year,
                y = data_ica.month,

                hoverinfo = 'x+y+z',



        )
        layout = go.Layout(
            title= 'S&P Volume Heatmap',
            xaxis = {'title': 'Year'},
            yaxis = {'title': 'Month'},
        )

        data=[trace]
        fig= dict(data =data, layout=layout)
#Candlestick Chart
    else:

        trace = go.Candlestick(x=data_ica['Date'],
                            open=data_ica['open'],
                            high=data_ica['high'],
                            low=data_ica['low'],
                            close=data_ica['close'])
        layout = go.Layout(
                title='S&P CandelStick Historical Data',
                showlegend=False,
                xaxis=dict(
                    title="Date"),
                yaxis=dict(
                    title="Value"),
                    height = 800,
                    width = 1500
            )
        data = [trace]
        fig = go.Figure(data=data, layout=layout)


    return fig
 #       _
 #       .__(.)< (MEOW)
 #        \___)
 # ~~~~~~~~~~~~~~~~~~

if __name__ == '__main__':
    app.run_server()
