import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input

# from iexfinance.stocks import get_historical_data
import datetime
from dateutil.relativedelta import relativedelta
import plotly.graph_objects as go
import pandas as pd
import dash_bootstrap_components as dbc

start=datetime.datetime.today() -relativedelta(years=5)
end = datetime.datetime.today()

df = pd.read_csv("stodat/individual_stocks_5yr/individual_stocks_5yr/GE_data.csv")


trace_close = go.Scatter(
    x=list(df.open),
    y=list(df.close),
    name="Close",
    line=dict(color="purple")
)

data=[trace_close]
layout = dict(title="Stock",showlegend=False)

fig = dict(data=data, layout=layout)

app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    html.H1(children="Hello World!"),
    html.Label("Dash Graph"),
    html.Div([
        dcc.Input(
            id='inp',
            placeholder="enter a stock",
            type="text",
            value='GE',
            className='form-control'
        )
    ], 
    ),
    # html.Div(
    #     dcc.Dropdown(
    #         options=[
    #             {'label':'Candelstick','value':'Candlestick'},
    #             {'label':'Bar','value':'Bar'},
    #         ]
    #     )
    # ),
    html.Div([
        dcc.Graph(id="Stock",
        )], className='graph'
    ),
    # html.Div([
    #     html.H2("test image"),
    #     html.Img(src="/assets/a.jpg")
    # ],className="banner")
])

app.css.append_css({
    "external_url":"https://codepen.io/chriddyp/pen/bWLwgP.css"
})

@app.callback(Output("Stock","figure"),
             [Input("inp","value")])
def update(input):
    df = pd.read_csv(f"stodat/individual_stocks_5yr/individual_stocks_5yr/{input}_data.csv")
    trace_close = go.Scatter(
        x=list(df.date),
        y=list(df.close),
        name="Close",
        line=dict(color="purple")
    )
    data = []
    data.append(trace_close)
    layout = {'title':'callback graph'}

    return {
        'data':data,
        'layout':layout
    }

if __name__=="__main__":
    app.run_server()