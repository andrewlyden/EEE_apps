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
        dcc.Graph(id="graph6"),
        html.P("Select cost level:"),
        dcc.Slider(
            id="slider-cost",
            min=30,
            max=100,
            step=1,
            value=60,
            marks={i: str(i) for i in range(30, 101, 10)},
        ),
        html.P("Select machine price:"),
        dcc.Slider(
            id="slider-machine",
            min=1,
            max=5,
            step=1,
            value=1,
            marks={i: str(i) for i in range(1, 6, 1)},
        ),
        html.P("Select fuel price:"),
        dcc.Slider(
            id="slider-fuel",
            min=1,
            max=5,
            step=1,
            value=1,
            marks={i: str(i) for i in range(1, 6, 1)},
        )
    ]
)


@callback(
    Output("graph6", "figure"),
    Input("slider-cost", "value"),
    Input("slider-machine", "value"),
    Input("slider-fuel", "value"),
)

def plot(cost, machine, fuel):

    def isoquant(production):
        x_ = np.arange(0.1, 100., 0.1)
        alpha = 0.5
        const = 0.5
        y_ = []
        for x in x_:
            y = const * (production / (x ** alpha)) ** (1 / (1 - alpha))
            y_.append(y)
        df_plot = pd.DataFrame({'Quantity of machine': x_, 'Quantity of fuel': y_})
        return df_plot

    df_plot = isoquant(55)
    fig1 = px.line(df_plot, x='Quantity of machine', y='Quantity of fuel', width=800, height=500, range_x=[0,100], range_y=[0,100])
    fig1.update_traces(line_color='blue')

    # Create the indifference curves using Plotly Express
    # fig1 = px.line(df, x='Quantity of fuel', y='Quantity of food', color='Budget', labels={'Quantity of food': 'Quantity of food'}, title='Indifference Curves')

    def isocost(cost, machine, fuel):
        x_ = np.arange(0.1, 100., 0.1)
        y_ = []
        slope = -machine / fuel
        intercept = cost / fuel
        for x in x_:
            y = slope * x + intercept
            y_.append(y)
        df_plot = pd.DataFrame({'Quantity of machine': x_, 'Quantity of fuel': y_})
        return df_plot

    df_plot = isocost(cost, machine, fuel)
    # fig = df_plot.hvplot(kind='line', x='Quantity of fuel', y='Price of fuel', width=800, height=500, xlim=(0, 100), ylim=(0, 100))
    fig2 = px.line(df_plot, x='Quantity of machine', y='Quantity of fuel', range_x=[0,200], range_y=[0,200])
    fig2.update_traces(line_color='red')

    fig3 = go.Figure(data=fig1.data + fig2.data, layout = fig1.layout)

    return fig3
