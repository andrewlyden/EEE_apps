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
    # html.H1("Supplier Marginal Abatement Cost Curve Carbon Abatement Analysis"),
    dcc.Graph(id='macc-chart'),    
    html.Label("Select carbon tax:"),
    dcc.Slider(
        id='carbon-tax-slider-1',
        min=0,
        max=30,
        step=1,
        value=10,
        marks={i: str(i) for i in range(0, 31, 10)}
    ),
    
    html.Label("Select carbon emissions:"),
    dcc.Slider(
        id='carbon-emissions-slider-2',
        min=0,
        max=30,
        step=1,
        value=20,
        marks={i: str(i) for i in range(0, 31, 10)}
    ),

])

# Define callback to update the MACC based on the selected abatement options
@callback(
    Output('macc-chart', 'figure'),
    [Input('carbon-tax-slider-1', 'value'),
     Input('carbon-emissions-slider-2', 'value')]
)
def update_macc(carbon_tax, carbon_emissions):
    # Sample data (you may replace this with your own dataset)
    quantity = [10, 20, 30, 40, 50]
    marginal_cost = [5, 8, 12, 18, 25]
    option = ['Repair', 'Optimise', 'Replace', 'Upgrade', 'New']
    df = pd.DataFrame({'Quantity': quantity, 'Marginal_Cost': marginal_cost, 'Carbon Reduction Option': option})

    df['Total_Cost'] = (df['Marginal_Cost'] + df['Quantity'] + df['Quantity']) * 4

    # Create MACC plot
    fig = px.bar(df, x='Carbon Reduction Option', y='Total_Cost', labels={'Total_Cost': 'Total Cost'})
    fig.update_layout(
        # xaxis_title='Quantity',
        yaxis_title='Total Cost (£/tonne CO2e)',
    )
    carbon_cost = carbon_tax * carbon_emissions
    fig.add_hline(y=carbon_cost)

    return fig
