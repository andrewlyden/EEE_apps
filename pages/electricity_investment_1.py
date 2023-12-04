import pypsa

# from jupyter_dash import JupyterDash
import dash
from dash import Dash, dcc, html, Input, Output, callback
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
import dash_bootstrap_components as dbc

dash.register_page(__name__)

# Function to calculate optimal dispatch and investment using PyPSA
def calculate_optimal_dispatch_and_investment(nuclear_cost, coal_cost, gas_cost, total_demand):
    # Create a PyPSA network
    network = pypsa.Network()

    # Add a bus and set demand
    network.add("Bus", "Bus 1")
    network.add("Load", "Demand", bus="Bus 1", p_set=total_demand)  # Dummy demand

    # Add specific generators (representing nuclear, coal, and gas)
    network.add("Generator", "Nuclear", bus="Bus 1", p_nom_max=500, p_nom_extendable=True, capital_cost=nuclear_cost)
    network.add("Generator", "Coal", bus="Bus 1", p_nom_max=500, p_nom_extendable=True, capital_cost=coal_cost)
    network.add("Generator", "Gas", bus="Bus 1", p_nom_max=1000, p_nom_extendable=True, capital_cost=gas_cost)

    # Solve the PyPSA network
    network.optimize(solver_name='highs')

    # Extract investment results
    investment_results = pd.DataFrame({
        'Generator': network.generators.index.values,
        'Investment Level (MW)': network.generators.p_nom_opt
    })

    return investment_results

layout = html.Div([
    # html.H1("Electricity Market Investment Analysis"),

    dcc.Graph(id='investment-line-plot'),

    html.Label("Enter capital cost for Nuclear (£/MW):"),
    dcc.Slider(
        id='nuclear-cost-input',
        min=0,
        max=10,
        step=1,
        marks={i: str(i) for i in range(0, 11, 1)},
        value=6,
    ),

    html.Label("Enter capital cost for Coal (£/MW):"),
    dcc.Slider(
        id='coal-cost-input',
        min=0,
        max=10,
        step=1,
        marks={i: str(i) for i in range(0, 11, 1)},
        value=5,
    ),

    html.Label("Enter capital cost for Gas (£/MW):"),
    dcc.Slider(
        id='gas-cost-input',
        min=0,
        max=10,
        step=1,
        marks={i: str(i) for i in range(0, 11, 1)},
        value=4,
    ),

    html.Label("Enter total demand (MW):"),
    dcc.Slider(
        id='demand-input',
        min=0,
        max=2000,
        step=250,
        marks={i: str(i) for i in range(0, 2001, 250)},
        value=1000,
    ),

])

# Callbacks to update the plots and tables based on user input
@callback(
    Output('investment-line-plot', 'figure'),
    Input('nuclear-cost-input', 'value'),
    Input('coal-cost-input', 'value'),
    Input('gas-cost-input', 'value'),
    Input('demand-input', 'value')
)
def update_graph(nuclear_cost, coal_cost, gas_cost, total_demand):
    # Call your function to calculate optimal dispatch and investment using PyPSA
    results_df = calculate_optimal_dispatch_and_investment(nuclear_cost, coal_cost, gas_cost, total_demand)

    # Create line plot
    print(results_df['Generator'])
    print(results_df['Investment Level (MW)'])
    line_plot = px.bar(
        results_df,
        x='Generator',
        y='Investment Level (MW)',
        # labels={'Investment Level (MW)': 'Optimal Investment Level (MW)'},
        title='Optimal Investment Levels for Generators'
    )

    return line_plot
