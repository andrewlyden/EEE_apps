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
        dcc.Graph(id="graph10"),
        html.P("Select demand intercept:"),
        dcc.Slider(
            id="slider-demand-intercept",
            min=0,
            max=200,
            step=1,
            value=200,
            marks={i: str(i) for i in range(0, 201, 25)},
        ),
        html.P("Select demand slope:"),
        dcc.Slider(
            id="slider-demand-slope",
            min=-5,
            max=0.1,
            step=0.10,
            value=-0.2,
            marks={i: str(i) for i in range(-5, 1, 1)},
        ),
        # html.P("Select cost intercept 1:"),
        # dcc.Slider(
        #     id="slider-cost-intercept-1",
        #     min=0,
        #     max=100,
        #     step=0.5,
        #     value=2.5,
        #     marks={i: str(i) for i in range(0, 101, 25)},
        # ),
        # html.P("Select cost intercept 2:"),
        # dcc.Slider(
        #     id="slider-cost-intercept-2",
        #     min=0,
        #     max=100,
        #     step=0.5,
        #     value=2.5,
        #     marks={i: str(i) for i in range(0, 101, 25)},
        # ),
        html.P("Select cost slope 1:"),
        dcc.Slider(
            id="slider-cost-slope-1",
            min=0,
            max=100,
            step=0.5,
            value=0.5,
            marks={i: str(i) for i in range(0, 101, 25)},
        ),
        html.P("Select cost slope 2:"),
        dcc.Slider(
            id="slider-cost-slope-2",
            min=0,
            max=100,
            step=0.5,
            value=0.5,
            marks={i: str(i) for i in range(0, 101, 25)},
        ),
    ]
)

@callback(
    Output("graph10", "figure"),
    Input("slider-demand-intercept", "value"),
    Input("slider-demand-slope", "value"),
    # Input("slider-cost-intercept-1", "value"),
    # Input("slider-cost-intercept-2", "value"),
    Input("slider-cost-slope-1", "value"),
    Input("slider-cost-slope-2", "value"),
)

def plot(demand_intercept, demand_slope, cost_slope_1, cost_slope_2):
    def optimal_response_function_1(cost_slope, demand_intercept, demand_slope):
        x_ = np.arange(0.1, 1000., 0.1)
        y_ = []
        for x in x_:
            y = (cost_slope - demand_intercept - demand_slope * x) / (2 * demand_slope)
            y_.append(y)
        df_plot = pd.DataFrame({'Quantity 2': x_, 'Quantity 1': y_})
        return df_plot
    def optimal_response_function_2(cost_slope, demand_intercept, demand_slope):
        y_ = np.arange(0.1, 1000., 0.1)
        x_ = []
        for y in y_:
            x = (cost_slope - demand_intercept - demand_slope * y) / (2 * demand_slope)
            x_.append(x)
        df_plot = pd.DataFrame({'Quantity 2': x_, 'Quantity 1': y_})
        return df_plot

    df_optimal_response_function_1 = optimal_response_function_1(cost_slope_1, demand_intercept, demand_slope)
    fig1 = px.line(df_optimal_response_function_1, x='Quantity 2', y='Quantity 1', range_x=[0,500], range_y=[0,1000])
    fig1.update_traces(line_color='blue', name='Optimal response function 1', showlegend=True)

    df_optimal_response_function_2 = optimal_response_function_2(cost_slope_2, demand_intercept, demand_slope)
    fig2 = px.line(df_optimal_response_function_2, x='Quantity 2', y='Quantity 1', range_x=[0,500], range_y=[0,1000])
    fig2.update_traces(line_color='green', name='Optimal response function 2', showlegend=True)
    
    fig = go.Figure(data=fig1.data + fig2.data, layout = fig1.layout)

    return fig
