import dash
import dash_core_components as dcc
import dash_html_components as html
from iexfinance.stocks import get_historical_data
import datetime
from dateutil.relativedelta import relativedelta
import plotly.graph_objects as go
import pandas as pd

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

app = dash.Dash()

app.layout = html.Div([
    html.H1(children="Hello World!"),
    html.Label("Dash Graph"),
    html.Div(
        dcc.Graph(id="Stock",
        figure=fig)
    )
])

if __name__=="__main__":
    app.run_server()