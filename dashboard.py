# # coding: utf-8
import dash_core_components as dcc
import dash_html_components as html
import psycopg2
import pandas as pd
import plotly.express as px
import dash
from sqlalchemy import create_engine
import dash
from dash import dcc, html
from dash.dependencies import Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import pandas_datareader.data as web
import datetime

v_user=111
global ticker_id_prv
url = 'postgresql://postgres:root@localhost:5433/postgres'
engine = create_engine(url, pool_size=50, echo=True)
dbConnection    = engine.connect()
df_orders      = pd.read_sql("SELECT sector, id FROM security", dbConnection)

df_tickers_name = pd.read_sql("SELECT ticker FROM security", dbConnection)
selection_type = pd.DataFrame({'selection': ['open', 'high', 'low', 'close']})

# https://stooq.com/
start = datetime.datetime(2020, 1, 1)
end = datetime.datetime(2020, 12, 3)
df = web.DataReader(['AMZN','GOOGL','FB','PFE','MRNA','BNTX'],
                    'stooq', start=start, end=end)
# df=df.melt(ignore_index=False, value_name="price").reset_index()
df = df.stack().reset_index()
print(df[:15])


# df.to_csv("mystocks.csv", index=False)
# df = pd.read_csv("mystocks.csv")
# print(df[:15])


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

        dbc.Col([
			dcc.DatePickerRange(
				id='my-date-picker-range',
				min_date_allowed=datetime.date(1995, 8, 5),
				max_date_allowed=datetime.date(2017, 9, 19),
				initial_visible_month=datetime.date(2017, 8, 5),
				end_date=datetime.date(2017, 8, 25)
				),
            dcc.Graph(id='line-fig2', figure={})
        ], #width={'size':5, 'offset':0, 'order':2},
           xs=12, sm=12, md=12, lg=5, xl=5
        ),

    ], justify='start'),  # Horizontal:start,center,end,between,around

    dbc.Row([
        dbc.Col([
            html.P("Select Company Stock:",
                   style={"textDecoration": "underline"}),
            # dcc.Checklist(id='my-checklist', value=['FB', 'GOOGL', 'AMZN'],
            #               options=[{'label':x, 'value':x}
            #                        for x in sorted(df['Symbols'].unique())],
            #               labelClassName="mr-3"),
			# dcc.Checklist(id='my-checklist2', value=['FB', 'GOOGL', 'AMZN'],
            #         	  options=[{'label':x, 'value':x}
            #                        for x in sorted(df['Symbols'].unique())],
            #               labelClassName="mr-3"),
            dcc.Graph(id='my-hist', figure={}),
        ], #width={'size':5, 'offset':1},
           xs=12, sm=12, md=12, lg=5, xl=5
        ),

        dbc.Col([
            dbc.Card(
                [
                    dbc.CardBody(
                        html.P(
                            "We're better together. Help each other out!",
                            className="card-text")
                    ),
                    dbc.CardImg(
                        src="https://media.giphy.com/media/Ll0jnPa6IS8eI/giphy.gif",
                        bottom=True),
                ],
                style={"width": "24rem"},
            )
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
	Input('my-date-picker-range', 'end_date')
)
def update_graph(start_date, end_date):
    # dff = df[df['Symbols'].isin(stock_slctd)]
	df_orders2 = pd.read_sql("SELECT date, open FROM price WHERE ticker_id=335 ", dbConnection)
	print(start_date)
    # figln2 = px.line(dff, x='Date', y='Open', color='Symbols')
	figln2 = px.scatter(df_orders2, x="date", y="open", animation_frame="date", size_max=55, range_x=[100,100000], range_y=[25,90])

	return figln2


# Histogram
@app.callback(
    Output('my-hist', 'figure'),
    Input('my-checklist', 'value')
)
def update_graph(stock_slctd):
    dff = df[df['Symbols'].isin(stock_slctd)]
    dff = dff[dff['Date']=='2020-12-03']
    fighist = px.histogram(dff, x='Symbols', y='Close')
    return fighist


if __name__=='__main__':
    app.run_server(debug=True, port=8000)


