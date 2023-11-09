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
        dcc.Graph(id="graph14")
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
        html.P("Select externality value:"),
        dcc.Slider(
            id="slider-externality-value",
            min=0,
            max=3,
            step=0.1,
            value=2,
            marks={i: str(i) for i in range(0, 4, 1)})
    ])
])

@callback(
    Output("graph14", "figure"),
    Input("slider-supply-intercept", "value"),
    Input("slider-supply-slope", "value"),
    Input("slider-demand-intercept", "value"),
    Input("slider-demand-slope", "value"),
    Input("slider-externality-value", "value")
)

def plot(supply_intercept, supply_slope, demand_intercept, demand_slope, externality):
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
    def social_cost_function(supply_slope, supply_intercept, externality):
        x_ = np.arange(0.1, 100., 0.1)
        y_ = []
        for x in x_:
            y = supply_slope * x * externality + supply_intercept
            y_.append(y)
        df_plot = pd.DataFrame({'Quantity': x_, 'Price': y_})
        return df_plot
    def private_quantity_calc(supply_slope, supply_intercept, demand_slope, demand_intercept):
        quantity = (demand_intercept - supply_intercept) / (supply_slope - demand_slope)
        return quantity
    def private_price_calc(quantity, supply_slope, supply_intercept):
        price = supply_slope * quantity + supply_intercept
        return price
    def social_quantity_calc(supply_slope, supply_intercept, demand_slope, demand_intercept, externality):
        quantity = (demand_intercept - supply_intercept) / (supply_slope * externality - demand_slope)
        return quantity
    def social_price_calc(quantity, supply_slope, supply_intercept, externality):
        price = supply_slope * quantity * externality + supply_intercept
        return price
    def deadweight_calc(private_quantity, social_quantity, private_price, social_price_at_private_quantity):
        deadweight = (private_quantity - social_quantity) * (social_price_at_private_quantity - private_price) / 2
        return deadweight

    df_supply = supply_function(supply_slope, supply_intercept)
    fig1 = px.line(df_supply, x='Quantity', y='Price', range_x=[0,50], range_y=[0,100])
    fig1.update_traces(line_color='blue', name='Supply curve', showlegend=True)
    df_demand = demand_function(demand_slope, demand_intercept)
    fig2 = px.line(df_demand, x='Quantity', y='Price', range_x=[0,50], range_y=[0,100])
    fig2.update_traces(line_color='green', name='Demand curve', showlegend=True)
    df_social = social_cost_function(supply_slope, supply_intercept, externality)
    fig3 = px.line(df_social, x='Quantity', y='Price', range_x=[0,50], range_y=[0,100])
    fig3.update_traces(line_color='black', line_dash="dash", name='Social cost curve', showlegend=True)
    fig = go.Figure(data=fig1.data + fig2.data + fig3.data, layout = fig1.layout)

    private_quantity = private_quantity_calc(supply_slope, supply_intercept, demand_slope, demand_intercept)
    private_price = private_price_calc(private_quantity, supply_slope, supply_intercept)
    social_quantity = social_quantity_calc(supply_slope, supply_intercept, demand_slope, demand_intercept, externality)
    social_price = social_price_calc(social_quantity, supply_slope, supply_intercept, externality)
    social_price_at_private_quantity = social_price_calc(private_quantity, supply_slope, supply_intercept, externality)
    deadweight_value = deadweight_calc(private_quantity, social_quantity, private_price, social_price_at_private_quantity)

    fig_shape1 = go.Figure(go.Scatter(x=[private_quantity, private_quantity, social_quantity], y=[private_price, social_price_at_private_quantity, social_price], line=dict(color="LightGreen"), fill="toself"))
    deadweight_text = "Deadweight: " + str(round(deadweight_value, 2))
    fig_shape1.update_traces(name=deadweight_text)

    fig = go.Figure(data=fig.data + fig_shape1.data, layout = fig1.layout)

    # fig.add_shape(type="line", x0=0, y0=private_price, x1=private_quantity, y1=private_price, line=dict(color="red", width=3, dash="dash"))
    # fig.add_shape(type="line", x0=private_quantity, y0=0, x1=private_quantity, y1=private_price, line=dict(color="LightGrey", width=3, dash="dash"))

    # fig.add_shape(type="line", x0=0, y0=social_price, x1=social_quantity, y1=social_price, line=dict(color="red", width=3, dash="dash"))
    # fig.add_shape(type="line", x0=social_quantity, y0=0, x1=social_quantity, y1=social_price, line=dict(color="LightGrey", width=3, dash="dash"))

    # fig.add_shape(type="line", x0=0, y0=social_price_at_private_quantity, x1=private_quantity, y1=social_price_at_private_quantity, line=dict(color="red", width=3, dash="dash"))

    return fig
