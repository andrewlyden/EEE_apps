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
        # html.H4("Budget constraint"),
        dcc.Graph(id="graph9")
    ]),
    
    dbc.Row([
        html.P("Select supply curve intercept:"),
        dcc.Slider(
            id="slider-supply-intercept",
            min=0,
            max=100,
            step=1,
            value=0,
            marks={i: str(i) for i in range(0, 201, 25)}),
    ]),
    dbc.Row([
        html.P("Select supply curve slope:"),
        dcc.Slider(
            id="slider-supply-slope",
            min=0.5,
            max=5,
            step=0.10,
            value=2,
            marks={i: str(i) for i in range(0, 6, 2)})
    ]),
    dbc.Row([
        html.P("Select demand curve intercept:"),
        dcc.Slider(
            id="slider-demand-intercept",
            min=0,
            max=125,
            step=1,
            value=100,
            marks={i: str(i) for i in range(0, 201, 25)},)
    ]),
    dbc.Row([
        html.P("Select demand curve slope:"),
        dcc.Slider(
            id="slider-demand-slope",
            min=-5,
            max=0.1,
            step=0.10,
            value=-3,
            marks={i: str(i) for i in range(-5, 1, 1)})
    ]),
    dbc.Row([
        html.P("Select monopolist quantity:"),
        dcc.Slider(
            id="slider-monopolist-quantity",
            min=0,
            max=100,
            step=1,
            value=12,
            marks={i: str(i) for i in range(0, 101, 20)})
    ])
])

@callback(
    Output("graph9", "figure"),
    Input("slider-supply-intercept", "value"),
    Input("slider-supply-slope", "value"),
    Input("slider-demand-intercept", "value"),
    Input("slider-demand-slope", "value"),
    Input("slider-monopolist-quantity", "value")
)

def plot(supply_intercept, supply_slope, demand_intercept, demand_slope, monopolist_quantity):
    def supply_function(supply_slope, supply_intercept):
        x_ = np.arange(0.1, 100., 0.1)
        y_ = []
        for x in x_:
            y = supply_slope * x + supply_intercept
            y_.append(y)
        df_plot = pd.DataFrame({'Quantity': x_, 'Price': y_})
        return df_plot
    def demand_function(demand_slope, demand_intercept):
        x_ = np.arange(0.1, 100., 0.1)
        y_ = []
        for x in x_:
            y = demand_slope * x + demand_intercept
            y_.append(y)
        df_plot = pd.DataFrame({'Quantity': x_, 'Price': y_})
        return df_plot
    def marginal_revenue(demand_slope, demand_intercept):
        x_ = np.arange(0.1, 100., 0.1)
        y_ = []
        for x in x_:
            y = 2 * demand_slope * x + demand_intercept
            y_.append(y)
        df_plot = pd.DataFrame({'Quantity': x_, 'Price': y_})
        return df_plot
    def producer_price_calc(monopolist_quantity, supply_slope, supply_intercept):
        price = supply_slope * monopolist_quantity + supply_intercept
        return price
    def demand_price_calc(monopolist_quantity, demand_slope, demand_intercept):
        price = demand_slope * monopolist_quantity + demand_intercept
        return price

    df_supply = supply_function(supply_slope, supply_intercept)
    fig1 = px.line(df_supply, x='Quantity', y='Price', range_x=[0,50], range_y=[0,100])
    fig1.update_traces(line_color='blue', name='Supply curve', showlegend=True)
    df_demand = demand_function(demand_slope, demand_intercept)
    fig2 = px.line(df_demand, x='Quantity', y='Price', range_x=[0,50], range_y=[0,100])
    fig2.update_traces(line_color='green', name='Demand curve', showlegend=True)
    df_marginal = marginal_revenue(demand_slope, demand_intercept)
    fig3 = px.line(df_marginal, x='Quantity', y='Price', range_x=[0,50], range_y=[0,100])
    fig3.update_traces(line_color='black', line_dash="dash", name='Marginal revenue', showlegend=True)
    fig = go.Figure(data=fig1.data + fig2.data + fig3.data, layout = fig1.layout)

    quantity = monopolist_quantity
    producer_price = producer_price_calc(monopolist_quantity, supply_slope, supply_intercept)
    demand_price = demand_price_calc(monopolist_quantity, demand_slope, demand_intercept)

    producer_surplus = quantity * (demand_price - producer_price) + (producer_price - supply_intercept) * quantity / 2
    consumer_surplus = (demand_intercept - demand_price) * quantity / 2

    fig_shape1 = go.Figure(go.Scatter(x=[0,0,quantity], y=[demand_intercept,demand_price,demand_price], line=dict(color="LightGreen"), fill="toself"))
    consumer_surplus_text = "Consumer surplus = " + str(round(consumer_surplus, 2))
    fig_shape1.update_traces(name=consumer_surplus_text)

    fig_shape2 = go.Figure(go.Scatter(x=[0,0,quantity,quantity], y=[supply_intercept,demand_price,demand_price,producer_price], line=dict(color="LightBlue"), fill="toself"))
    producer_surplus_text = "Producer surplus = " + str(round(producer_surplus, 2))
    fig_shape2.update_traces(name=producer_surplus_text)

    fig = go.Figure(data=fig.data + fig_shape1.data + fig_shape2.data, layout = fig1.layout)

    # fig.add_shape(type="line", x0=0, y0=price, x1=quantity, y1=price, line=dict(color="red", width=3, dash="dash"))
    fig.add_shape(type="line", x0=quantity, y0=0, x1=quantity, y1=demand_price, line=dict(color="LightGrey", width=3, dash="dash"))

    return fig
