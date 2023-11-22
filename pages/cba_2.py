# from jupyter_dash import JupyterDash
import dash
from dash import Dash, dcc, html, Input, Output, callback
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
import dash_bootstrap_components as dbc

dash.register_page(__name__)

layout = html.Div([
    # html.H1("LCOE Calculator"),
    
    html.Div([
        html.Label("Enter Total Project Cost (in £):"),
        dcc.Input(id="total-cost", type="number", value=1000000),
    ]),
    
    html.Div([
        html.Label("Enter Annual Energy Production (in MWh):"),
        dcc.Input(id="annual-production", type="number", value=5000),
    ]),
    
    html.Div([
        html.Label("Enter Project Lifetime (in years):"),
        dcc.Input(id="project-lifetime", type="number", value=20),
    ]),

    html.Div([
        html.Label("Enter Discount Rate (%):"),
        dcc.Input(id="discount-rate", type="number", value=5),
    ]),
    
    html.Div(id="lcoe-output", style={'marginTop': 20})
])

# Define callback to update LCOE output
@callback(
    Output("lcoe-output", "children"),
    [Input("total-cost", "value"),
     Input("annual-production", "value"),
     Input("project-lifetime", "value"),
     Input("discount-rate", "value")]
)
def update_lcoe(total_cost, annual_production, project_lifetime, discount_rate):
    # Calculate LCOE using the formula
    lcoe = (total_cost / (annual_production * project_lifetime)) * (
        (1 - (1 + discount_rate / 100) ** -project_lifetime) / (discount_rate / 100)
    )
    
    # Display the result
    return f"LCOE: {lcoe:.2f} £/kWh"
