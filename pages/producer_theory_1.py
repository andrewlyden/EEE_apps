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
        dcc.Graph(id="graph5"),
        html.P("Select machine price per unit:"),
        dcc.Slider(
            id="slider-machine",
            min=1,
            max=10,
            step=1,
            value=1,
            marks={i: str(i) for i in range(1, 11, 2)},
        ),
        html.P("Select fuel price:"),
        dcc.Slider(
            id="slider-fuel",
            min=1,
            max=10,
            step=1,
            value=1,
            marks={i: str(i) for i in range(1, 11, 2)},
        )
    ]
)


@callback(
    Output("graph5", "figure"),
    Input("slider-machine", "value"),
    Input("slider-fuel", "value"),
)

def plot(machine, fuel):
    def df_(budget):
        return pd.DataFrame({'Quantity of machines': [0, budget / machine], 'Quantity of fuel': [budget / fuel, 0]})
    df = df_(200)
    fig1 = px.line(df, x='Quantity of machines', y='Quantity of fuel', range_x=[0,200], range_y=[0,200])
    df = df_(180)
    fig2 = px.line(df, x='Quantity of machines', y='Quantity of fuel', range_x=[0,200], range_y=[0,200])
    df = df_(160)
    fig3 = px.line(df, x='Quantity of machines', y='Quantity of fuel', range_x=[0,200], range_y=[0,200])
    df = df_(140)
    fig4 = px.line(df, x='Quantity of machines', y='Quantity of fuel', range_x=[0,200], range_y=[0,200])
    df = df_(120)
    fig5 = px.line(df, x='Quantity of machines', y='Quantity of fuel', range_x=[0,200], range_y=[0,200])
    df = df_(100)
    fig6 = px.line(df, x='Quantity of machines', y='Quantity of fuel', range_x=[0,200], range_y=[0,200])
    df = df_(80)
    fig7 = px.line(df, x='Quantity of machines', y='Quantity of fuel', range_x=[0,200], range_y=[0,200])
    df = df_(60)
    fig8 = px.line(df, x='Quantity of machines', y='Quantity of fuel', range_x=[0,200], range_y=[0,200])
    df = df_(40)
    fig9 = px.line(df, x='Quantity of machines', y='Quantity of fuel', range_x=[0,200], range_y=[0,200])
    df = df_(20)
    fig10 = px.line(df, x='Quantity of machines', y='Quantity of fuel', range_x=[0,200], range_y=[0,200])

    fig = go.Figure(data = fig1.data + fig2.data + fig3.data + fig4.data + fig5.data + fig6.data + fig7.data + fig8.data + fig9.data + fig10.data, layout=fig1.layout)
    return fig
