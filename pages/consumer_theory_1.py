# from jupyter_dash import JupyterDash
import dash
from dash import Dash, dcc, html, Input, Output, callback
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
import dash_bootstrap_components as dbc

dash.register_page(__name__)

layout = html.Div(
    [
        # html.H4("Budget constraint"),
        dcc.Graph(id="graph1"),
        html.P("Select budget:"),
        dcc.Slider(
            id="slider-budget",
            min=10,
            max=100,
            step=5,
            value=100,
            marks={i: str(i) for i in range(10, 101, 10)},
        ),
        html.P("Select fuel price:"),
        dcc.Slider(
            id="slider-fuel",
            min=1,
            max=5,
            step=1,
            value=1,
            marks={i: str(i) for i in range(1, 6, 1)},
        ),
        html.P("Select food price:"),
        dcc.Slider(
            id="slider-food",
            min=1,
            max=5,
            step=1,
            value=1,
            marks={i: str(i) for i in range(1, 6, 1)},
        )
    ]
)


@callback(
    Output("graph1", "figure"),
    Input("slider-budget", "value"),
    Input("slider-fuel", "value"),
    Input("slider-food", "value"),
)

def max(budget, fuel, food):
    df = pd.DataFrame({'Quantity of fuel': [0, budget / fuel], 'Quantity of food': [budget / food, 0]})
    fig = px.line(df, x='Quantity of fuel', y='Quantity of food', range_x=[0,100], range_y=[0,100])
    fig.update_traces(line_color='red')
    return fig
