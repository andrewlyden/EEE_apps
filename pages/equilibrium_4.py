# from jupyter_dash import JupyterDash
import dash
from dash import Dash, dcc, html, Input, Output, callback
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
import dash_bootstrap_components as dbc

dash.register_page(__name__)

layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dcc.Graph(id="graph11"),
        ]),
        dbc.Col([
            dcc.Graph(id="graph12"),
        ]),
        dbc.Col([
            dcc.Graph(id="graph13"),
        ]),
    ]),
    dbc.Row([
        html.P("Select demand intercept:"),
        dcc.Slider(
            id="slider-demand-intercept",
            min=0,
            max=200,
            step=1,
            value=200,
            marks={i: str(i) for i in range(0, 201, 25)},
        ),
    ]),
    dbc.Row([
        html.P("Select demand slope:"),
        dcc.Slider(
            id="slider-demand-slope",
            min=-5,
            max=0.1,
            step=0.10,
            value=-0.2,
            marks={i: str(i) for i in range(-5, 1, 1)},
        ),
    ]),
    dbc.Row([
        html.P("Select cost intercept 1:"),
        dcc.Slider(
            id="slider-cost-intercept-1",
            min=0,
            max=100,
            step=0.5,
            value=2.5,
            marks={i: str(i) for i in range(0, 101, 25)},
        ),
    ]),
    dbc.Row([
        html.P("Select cost intercept 2:"),
        dcc.Slider(
            id="slider-cost-intercept-2",
            min=0,
            max=100,
            step=0.5,
            value=2.5,
            marks={i: str(i) for i in range(0, 101, 25)},
        ),
    ]),
    dbc.Row([
        html.P("Select cost slope 1:"),
        dcc.Slider(
            id="slider-cost-slope-1",
            min=0,
            max=100,
            step=0.5,
            value=0.5,
            marks={i: str(i) for i in range(0, 101, 25)},
        ),
    ]),
    dbc.Row([
        html.P("Select cost slope 2:"),
        dcc.Slider(
            id="slider-cost-slope-2",
            min=0,
            max=100,
            step=0.5,
            value=0.5,
            marks={i: str(i) for i in range(0, 101, 25)},
        ),
    ]),
    ]
)

@callback(
    Output("graph11", "figure"),
    Output("graph12", "figure"),
    Output("graph13", "figure"),
    Input("slider-demand-intercept", "value"),
    Input("slider-demand-slope", "value"),
    Input("slider-cost-intercept-1", "value"),
    Input("slider-cost-intercept-2", "value"),
    Input("slider-cost-slope-1", "value"),
    Input("slider-cost-slope-2", "value"),
)

def plot(demand_intercept, demand_slope, cost_intercept_1, cost_intercept_2, cost_slope_1, cost_slope_2):
    def stack_quantity_1(cost_slope_1, cost_slope_2, demand_intercept, demand_slope):
        q1 = (2 * cost_slope_1 - demand_intercept - cost_slope_2) / (2 * demand_slope)
        return q1
    def stack_quantity_2(cost_slope_2, demand_intercept, demand_slope, q1):
        q2 = (cost_slope_2 - demand_intercept - demand_slope * q1) / (2 * demand_slope)
        return q2
    def stack_profit_1(demand_intercept, demand_slope, stack_q1, stack_q2, cost_intercept_1, cost_slope_1):
        profit1 = demand_intercept * stack_q1 + demand_slope * stack_q1 * stack_q2 + demand_slope * stack_q1 ** 2 - cost_intercept_1 - cost_slope_1 * stack_q1
        return profit1
    def stack_profit_2(demand_intercept, demand_slope, stack_q1, stack_q2, cost_intercept_2, cost_slope_2):
        profit2 = demand_intercept * stack_q2 + demand_slope * stack_q2 * stack_q1 + demand_slope * stack_q2 ** 2 - cost_intercept_2 - cost_slope_2 * stack_q2
        return profit2
    def stack_price(demand_intercept, demand_slope, stack_q1, stack_q2):
        price1 = demand_intercept + demand_slope * (stack_q1 + stack_q2)
        return price1

    def cournot_quantity_1(cost_slope_1, cost_slope_2, demand_slope):
        q1 = (2 * cost_slope_1 - cost_slope_2 - demand_intercept) / (3 * demand_slope)
        return q1
    def cournot_quantity_2(cost_slope_2, demand_slope, demand_intercept, q1):
        q2 = (cost_slope_2 - demand_intercept - demand_slope * q1) / (2 * demand_slope)
        return q2
    def cournot_profit_1(demand_intercept, demand_slope, cournot_q1, cournot_q2, cost_intercept_1, cost_slope_1):
        profit1 = demand_intercept * cournot_q1 + demand_slope * cournot_q1 * cournot_q2 + demand_slope * cournot_q1 ** 2 - cost_intercept_1 - cost_slope_1 * cournot_q1
        return profit1
    def cournot_profit_2(demand_intercept, demand_slope, cournot_q1, cournot_q2, cost_intercept_2, cost_slope_2):
        profit2 = demand_intercept * cournot_q2 + demand_slope * cournot_q2 * cournot_q1 + demand_slope * cournot_q2 ** 2 - cost_intercept_2 - cost_slope_2 * cournot_q2
        return profit2
    def cournot_price(demand_intercept, demand_slope, cournot_q1, cournot_q2):
        price1 = demand_intercept + demand_slope * (cournot_q1 + cournot_q2)
        return price1
    
    stack_q1 = stack_quantity_1(cost_slope_1, cost_slope_2, demand_intercept, demand_slope)
    stack_q2 = stack_quantity_2(cost_slope_2, demand_intercept, demand_slope, stack_q1)
    stack_profit1 = stack_profit_1(demand_intercept, demand_slope, stack_q1, stack_q2, cost_intercept_1, cost_slope_1)
    stack_profit2 = stack_profit_2(demand_intercept, demand_slope, stack_q1, stack_q2, cost_intercept_2, cost_slope_2)
    stack_pri = stack_price(demand_intercept, demand_slope, stack_q1, stack_q2)

    cournot_q1 = cournot_quantity_1(cost_slope_1, cost_slope_2, demand_slope)
    cournot_q2 = cournot_quantity_2(cost_slope_2, demand_slope, demand_intercept, cournot_q1)
    cournot_profit1 = cournot_profit_1(demand_intercept, demand_slope, cournot_q1, cournot_q2, cost_intercept_1, cost_slope_1)
    cournot_profit2 = cournot_profit_2(demand_intercept, demand_slope, cournot_q1, cournot_q2, cost_intercept_2, cost_slope_2)
    cournot_pri = cournot_price(demand_intercept, demand_slope, cournot_q1, cournot_q2)
    
    game = ['Stackelberg', 'Cournot']

    fig1 = go.Figure(data=[
        go.Bar(name='Q1', x=game, y=[stack_q1, cournot_q1]),
        go.Bar(name='Q2', x=game, y=[stack_q2, cournot_q2])
    ])
    fig1.update_layout(title_text='Quantity', showlegend=False, margin=dict(l=20, r=20))

    fig2 = go.Figure(data=[
        go.Bar(name='Price', x=game, y=[stack_pri, cournot_pri])
    ])
    fig2.update_layout(title_text='Price', margin=dict(l=20, r=20))

    fig3 = go.Figure(data=[
        go.Bar(name='Profit 1', x=game, y=[stack_profit1, cournot_profit1]),
        go.Bar(name='Profit 2', x=game, y=[stack_profit2, cournot_profit2])
    ])
    fig3.update_layout(title_text='Profit', showlegend=False, margin=dict(l=20, r=20))

    return fig1, fig2, fig3
