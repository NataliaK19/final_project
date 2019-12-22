#!/usr/bin/env python
# coding: utf-8

# In[2]:


import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import numpy as np


# In[5]:


#Step 1: Upload and clean data

df=pd.read_csv('nama_10_gdp_1_Data.csv')
df['Indicators']=df['NA_ITEM'].astype(str) + ' ('+df['UNIT'].astype(str)+')'
def value(i):
    if i==':':
        return np.nan
    else:
        i=i.replace('.', '')
        new=i.replace(',','.')
        return new 
df['Value']=df['Value'].apply(value)

#Step 2: Exercise 1
    
app = dash.Dash(__name__)
server = app.server
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})


available_indicators = df['Indicators'].unique()
available_years = df['TIME'].unique()
available_countries = df['GEO'].unique()
    
app.layout = html.Div(style={'backgroundColor': '#f2eaec'}, children=[
    html.Div([
        
        html.Div([   
            html.H1('Final Project'),
            html.P('Dashboard for GDP and main components (output, expenditure and income)'),
            html.P('Student: Natalia Korchagina'),
            html.Br(),
            html.H4('Exercise 1: Scatterplot with two DropDown boxes for the different indicators')
        ],
        style={'textAlign': 'center'}),
        
        html.Div([
            html.Div('''Select indicator for X-axis'''),
            dcc.Dropdown(
                id='xaxis-column-1',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Gross domestic product at market prices (Chain linked volumes, index 2010=100)'
            ),
            dcc.RadioItems(
                id='xaxis-type-1',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],
        style={'width': '48%', 'display': 'inline-block', 'marginLeft':10}),

        html.Div([
            html.Div('''Select indicator for Y-axis'''),
            dcc.Dropdown(
                id='yaxis-column-1',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Actual individual consumption (Chain linked volumes, index 2010=100)'
            ),
            dcc.RadioItems(
                id='yaxis-type-1',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],style={'width': '48%', 'float': 'right', 'display': 'inline-block', 'marginRight':10}),

        html.Div([
            dcc.Graph(id='gdp-per-capita'),
        ], style={'marginLeft':10, 'marginRight':10, 'marginTop':10, 'marginBottom':10}),

        html.Div([
            dcc.Slider(
                id='year--slider',
                min=df['TIME'].min(),
                max=df['TIME'].max(),
                value=df['TIME'].max(),
                step=None,
                marks={str(year): str(year) for year in df['TIME'].unique()}
            )
        ], style={'marginLeft':15, 'marginRight':15, 'marginTop':10, 'marginBottom':10})
    
    ]),
    
    html.Br(), html.Br(), html.Br(),
    
    html.Div([
        
        html.Div([
            html.H4('Exercise 2: A line chart with two DropDown boxes')
        ],
        style={'textAlign': 'center'}),            
            
        html.Div([    
            html.Div('''Select country'''),
            dcc.Dropdown(
                id='countries',
                options=[{'label': i, 'value': i} for i in available_countries],
                value='European Union - 28 countries'
            )
        ],
        style={'width': '48%', 'display': 'inline-block', 'marginLeft':10}),

        html.Div([
            html.Div('''Select indicator for Y-axis'''),
            dcc.Dropdown(
                id='yaxis-column-2',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Gross domestic product at market prices (Chain linked volumes, index 2010=100)'
            )
        ],style={'width': '48%', 'float': 'right', 'display': 'inline-block', 'marginRight':10}),

        html.Div([
            dcc.Graph(id='gdp-per-capita2')
        ], style={'marginLeft':10, 'marginRight':10, 'marginTop':10, 'marginBottom':10})        
        
    ]),
    html.Br()
])

@app.callback(
    dash.dependencies.Output('gdp-per-capita', 'figure'),
    [dash.dependencies.Input('xaxis-column-1', 'value'),
     dash.dependencies.Input('yaxis-column-1', 'value'),
     dash.dependencies.Input('xaxis-type-1', 'value'),
     dash.dependencies.Input('yaxis-type-1', 'value'),
     dash.dependencies.Input('year--slider', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type,
                 year_value):
    dff = df[df['TIME'] == year_value]
    
    return {
        'data': [go.Scatter(
            x=dff[dff['Indicators'] == xaxis_column_name]['Value'],
            y=dff[dff['Indicators'] == yaxis_column_name]['Value'],
            text=dff[dff['Indicators'] == yaxis_column_name]['GEO'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name.split(' (')[0],
                'type': 'linear' if xaxis_type == 'Linear' else 'log',
                'autorange':True
            },
            yaxis={
                'title': yaxis_column_name.split(' (')[0],
                'type': 'linear' if yaxis_type == 'Linear' else 'log',
                'autorange':True
            },
            margin={'l': 65, 'b': 65, 't': 45, 'r': 0},
            hovermode='closest'
        )
    }

@app.callback(
    dash.dependencies.Output('gdp-per-capita2', 'figure'),
    [dash.dependencies.Input('countries', 'value'),
     dash.dependencies.Input('yaxis-column-2', 'value')])
def update_graph(country_value, yaxis_column_name):
    dff = df[df['GEO'] == country_value]
    
    return {
        'data': [go.Scatter(
            x=available_years,
            y=dff[dff['Indicators'] == yaxis_column_name]['Value'],
            text=dff[dff['Indicators'] == yaxis_column_name]['Value'],
            mode='lines',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': 'Years',
                'autorange':True
            },
            yaxis={
                'title': yaxis_column_name.split(' (')[0],
                'autorange':True
            },
            margin={'l': 65, 'b': 65, 't': 45, 'r': 15},
            hovermode='closest'
        )
    }

if __name__ == '__main__':
    app.run_server()


# In[ ]:




