# # coding: utf-8
import dash_core_components as dcc
import dash_html_components as html
import psycopg2
import pandas as pd
import plotly.express as px
import dash
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import pandas_datareader.data as web
import datetime

from sqlalchemy import create_engine
from dash import dcc, html
from dash.dependencies import Output, Input
from setup_psql_environment import get_database

engine = get_database()
dbConnection = engine.connect()

df_sector = pd.read_sql("SELECT sector, id FROM security", dbConnection)
df_tickers_name = pd.read_sql("SELECT ticker FROM security", dbConnection)
selection_type = pd.DataFrame({'selection': ['open', 'high', 'low', 'close']})

# https://www.bootstrapcdn.com/bootswatch/
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )


# Layout section: Bootstrap (https://hackerthemes.com/bootstrap-cheatsheet/)
# ************************************************************************
app.layout = dbc.Container([
    dbc.Row(
        dbc.Col(html.H1("Stock Market Dashboard",
                        className='text-center text-primary mb-4'),
                width=12)
    ),
    dbc.Row([
		### First plot
        dbc.Col([
			html.Label(['Choose ticker sell letter:'], style={'font-weight': 'bold', "text-align": "center"}),
            dcc.Dropdown(id='my-dpdn1', multi=False, value='A',
                         options=[{'label':x, 'value':x}
                                  for x in sorted(df_tickers_name['ticker'])],
                         ),
			html.Label(['Choose type selection:'], style={'font-weight': 'bold', "text-align": "center"}),
			dcc.Dropdown(id='my-dpdn1_2', multi=False, value='low',
                         options=[{'label':x, 'value':x}
                                  for x in sorted(selection_type['selection'].unique())],
                         ),
            dcc.Graph(id='line-fig', figure={})
        ], # width={'size':5, 'offset':1, 'order':1},
           xs=12, sm=12, md=12, lg=5, xl=5
        ),
		
		### Second plot
        dbc.Col([
			dcc.DatePickerRange(
				id='my-date-picker-range',
				min_date_allowed=datetime.date(1995, 8, 5),
				max_date_allowed=datetime.date(2024, 9, 19),
				initial_visible_month=datetime.date(2022, 8, 1),
				end_date=datetime.date(2022, 8, 22)
				),
			dcc.Checklist(id='my-checklist', value=['Finance'],
                          options=[{'label':x, 'value':x}
                                   for x in sorted(df_sector['sector'].unique())],
                          labelClassName="mr-3"),
            dcc.Graph(id='line-fig2', figure={})
        ], #width={'size':5, 'offset':0, 'order':2},
           xs=12, sm=12, md=12, lg=5, xl=5
        ),

    ], justify='start'),  # Horizontal:start,center,end,between,around

    dbc.Row([
        dbc.Col([
        ], #width={'size':5, 'offset':1},
           xs=12, sm=12, md=12, lg=5, xl=5
        ),

        dbc.Col([
        ], #width={'size':5, 'offset':1},
           xs=12, sm=12, md=12, lg=5, xl=5
        )
    ], align="center")  # Vertical: start, center, end

], fluid=True)


# Callback section: connecting the components
# ************************************************************************
# Line chart - Single
@app.callback(
    Output('my-dpdn1', 'choice1'),
    Input('my-dpdn1', 'value')
)
def set_choice1(value):
	return value

@app.callback(
    Output('my-dpdn1_2', 'choice2'),
    Input('my-dpdn1_2', 'value')
)
def set_choice2(value):
	return value

@app.callback(
	Output('line-fig', 'figure'),
    Input('my-dpdn1', 'choice1'),
    Input('my-dpdn1_2', 'choice2')
)
def update_graph(choice1, choice2):
	df_plot1 = pd.read_sql(f"SELECT date, {choice2} FROM price WHERE ticker_id in (SELECT id FROM security WHERE ticker='{choice1}')", dbConnection)
	fig1 = px.line(df_plot1, x='date', y=choice2)
	return fig1
	
### END: Line chart - Single ###

# Line chart - multiple for specific (randomly choosen) companies 
@app.callback(
    Output('line-fig2', 'figure'),
    Input('my-date-picker-range', 'start_date'),
	Input('my-date-picker-range', 'end_date'),
	Input('my-checklist', 'value')
)
def update_graph(start_date, end_date, value):
	data_tuple = {}
	for val in value:
		data = pd.read_sql(f"SELECT date, low FROM price WHERE (date >= '{start_date}' AND date <= '{end_date}') AND (ticker_id in (SELECT id FROM security WHERE sector='{val}'))", dbConnection)
		data_tuple[f"{val}"] = data
	
	layout = go.Layout(xaxis=dict(
        				title="date"),
    			   		yaxis=dict(
        				title="low")) 
	fig2 = go.Figure(layout=layout)
	for i in data_tuple:
		fig2 = fig2.add_trace(go.Scatter(x = data_tuple[i]["date"],
                              y = data_tuple[i]["low"], 
                              name = i))
	return fig2

### END: Line chart - multiple for specific (randomly choosen) companies ###

if __name__=='__main__':
    app.run_server(debug=True, port=8000)


