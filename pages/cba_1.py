# from jupyter_dash import JupyterDash
import dash
from dash import Dash, dcc, html, Input, Output, callback
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
import dash_bootstrap_components as dbc

import numpy_financial as npf

dash.register_page(__name__)

layout = html.Div([
    # html.H1("Wind Farm NPV Calculator"),

    html.Div([
        html.Label("Initial Investment (£):"),
        dcc.Input(id="initial-investment", type="number", value=1000000, placeholder="Initial Investment ($)"),
    ]),
    html.Div([
        html.Label("Annual Cash Inflow (£):"),
        dcc.Input(id="annual-cash-inflow", type="number", value=150000, placeholder="Annual Cash Inflow ($)"),
    ]),
    html.Div([
        html.Label("Discount Rate (%):"),
        dcc.Input(id="discount-rate", type="number", value=10, placeholder="Discount Rate (%)"),
    ]),
    html.Div([
        html.Label("Number of Years:"),
        dcc.Input(id="num-years", type="number", value=20, placeholder="Number of Years"),
    ]),
    
    html.Br(),
    
    dcc.Graph(id="npv-chart"),
    html.Br(),
    
    html.Div(id="npv-output")
])

# Callback function to update NPV output and table
@callback(
    [Output("npv-chart", "figure"),
     Output("npv-output", "children")],
    [Input("initial-investment", "value"),
     Input("annual-cash-inflow", "value"),
     Input("discount-rate", "value"),
     Input("num-years", "value")]
)
def update_npv(initial_investment, annual_cash_inflow, discount_rate, num_years):
    cash_flows = [-initial_investment] + [annual_cash_inflow] * num_years
    discount_factors = [(1 + discount_rate/100)**n for n in range(num_years + 1)]
    
    npv_results = [round(npf.npv(discount_rate/100, cash_flows[:n+1]), 2) for n in range(num_years + 1)]
    
    # Create a DataFrame for visualization
    df = pd.DataFrame({
        'Year': range(num_years + 1),
        'NPV': npv_results
    })
    
    # Create a line chart
    fig = {
        'data': [
            {'x': df['Year'], 'y': df['NPV'], 'type': 'line', 'name': 'NPV'},
        ],
        'layout': {
            'title': 'NPV Over Years',
            'xaxis': {'title': 'Year'},
            'yaxis': {'title': 'Net Present Value ($)', 'hoverformat': ',.2f'}
        }
    }
    
    # Display NPV result
    npv_output = f"Net Present Value for {num_years} years: ${npv_results[-1]:,.2f}"
    
    return fig, npv_output
