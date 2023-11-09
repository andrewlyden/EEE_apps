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
        dcc.Graph(id="graph2"),
        html.P("Select budget:"),
        dcc.Slider(
            id="slider-budget",
            min=10,
            max=100,
            step=1,
            value=60,
            marks={i: str(i) for i in range(10, 101, 5)},
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
    Output("graph2", "figure"),
    Input("slider-budget", "value"),
    Input("slider-fuel", "value"),
    Input("slider-food", "value"),
)

def plot(budget, fuel, food):

    def plot(multiplier):
        x_ = np.arange(0.1, 100., 0.1)
        y_ = []
        for x in x_:
            y = 100 / x # + math.cos(x**2)
            y_.append(y)
        df_plot = pd.DataFrame({'Quantity of fuel': x_, 'Quantity of food': y_}) + multiplier
        return df_plot

    df_plot = plot(1)
    fig1 = px.line(df_plot, x='Quantity of fuel', y='Quantity of food', width=800, height=500, range_x=[0,100], range_y=[0,100])
    fig1.update_traces(line_color='blue')
    df_plot = plot(20)
    fig3 = px.line(df_plot, x='Quantity of fuel', y='Quantity of food', range_x=[0,100], range_y=[0,100])
    fig3.update_traces(line_color='green')
    df_plot = plot(40)
    fig5 = px.line(df_plot, x='Quantity of fuel', y='Quantity of food', range_x=[0,100], range_y=[0,100])
    fig5.update_traces(line_color='lightgoldenrodyellow')
    df_plot = plot(60)
    fig7 = px.line(df_plot, x='Quantity of fuel', y='Quantity of food', range_x=[0,100], range_y=[0,100])
    fig7.update_traces(line_color='lightblue')
    df_plot = plot(80)
    fig9 = px.line(df_plot, x='Quantity of fuel', y='Quantity of food', range_x=[0,100], range_y=[0,100])
    fig9.update_traces(line_color='palegreen')
    fig1 = go.Figure(data=fig1.data + fig3.data + fig5.data + fig7.data + fig9.data, layout = fig1.layout)

    # Create the indifference curves using Plotly Express
    # fig1 = px.line(df, x='Quantity of fuel', y='Quantity of food', color='Budget', labels={'Quantity of food': 'Quantity of food'}, title='Indifference Curves')

    df = pd.DataFrame({'Quantity of fuel': [0, budget / fuel], 'Quantity of food': [budget / food, 0]})
    fig2 = px.line(df, x='Quantity of fuel', y='Quantity of food', range_x=[0,100], range_y=[0,100])
    fig2.update_traces(line_color='red', line_dash="dash")

    fig3 = go.Figure(data=fig1.data + fig2.data, layout = fig2.layout)

    return fig3
