import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input, State

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
    # html.H1(children="Practice"),
    # html.Label("Dash Graph"),
    html.Div([
        dcc.Input(
            id='inp',
            placeholder="enter a stock",
            type="text",
            value='GE',
            className='form-control ast'
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
def update(inpu):
    df = pd.read_csv(f"stodat/individual_stocks_5yr/individual_stocks_5yr/{inpu}_data.csv")
    trace_line = go.Scatter(x=list(df.date),
                                y=list(df.close),
                                #visible=False,
                                name="Close",
                                showlegend=False)

    trace_candle = go.Candlestick(x=df.index,
                           open=df.open,
                           high=df.high,
                           low=df.low,
                           close=df.close,
                           #increasing=dict(line=dict(color="#00ff00")),
                           #decreasing=dict(line=dict(color="white")),
                           visible=False,
                           showlegend=False)

    trace_bar = go.Ohlc(x=df.index,
                           open=df.open,
                           high=df.high,
                           low=df.low,
                           close=df.close,
                           #increasing=dict(line=dict(color="#888888")),
                           #decreasing=dict(line=dict(color="#888888")),
                           visible=False,
                           showlegend=False)

    data = [trace_line, trace_candle, trace_bar]

    updatemenus = list([
        dict(
            buttons=list([
                dict(
                    args=[{'visible': [True, False, False]}],
                    label='Line',
                    method='update'
                ),
                dict(
                    args=[{'visible': [False, True, False]}],
                    label='Candle',
                    method='update'
                ),
                dict(
                    args=[{'visible': [False, False, True]}],
                    label='Bar',
                    method='update'
                ),
            ]),
            direction='down',
            pad={'r': 10, 't': 10},
            showactive=True,
            x=0,
            xanchor='left',
            y=1.05,
            yanchor='top'
        ),
    ])
    layout = dict(
        title=inpu,
        updatemenus=updatemenus,
        autosize=False,
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                         label='1m',
                         step='month',
                         stepmode='backward'),
                    dict(count=6,
                         label='6m',
                         step='month',
                         stepmode='backward'),
                    dict(count=1,
                         label='YTD',
                         step='year',
                         stepmode='todate'),
                    dict(count=1,
                         label='1y',
                         step='year',
                         stepmode='backward'),
                    dict(step='all')
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type='date'
        )
    )

    return {
        'data':data,
        'layout':layout
    }

if __name__=="__main__":
    app.run_server()