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

layout = html.Div(
    [
        # html.H4("Budget constraint"),
        dcc.Graph(id="graph17"),
        html.P("Select wind capacity:"),
        dcc.Slider(
            id="slider-wind-capacity",
            min=0,
            max=2000,
            step=1,
            value=500,
            marks={i: str(i) for i in range(0, 2001, 250)},
        ),
        html.P("Select wind availability:"),
        dcc.Slider(
            id="slider-wind-availability",
            min=0,
            max=1,
            step=0.01,
            value=0.75,
            marks={i: str(i) for i in range(0, 2, 1)},
        ),
        html.P("Select gas capacity:"),
        dcc.Slider(
            id="slider-gas-capacity",
            min=500,
            max=2000,
            step=1,
            value=500,
            marks={i: str(i) for i in range(500, 2001, 250)},
        ),
        html.P("Select coal capacity:"),
        dcc.Slider(
            id="slider-coal-capacity",
            min=500,
            max=2000,
            step=1,
            value=500,
            marks={i: str(i) for i in range(500, 2001, 250)},
        ),
        html.P("Select electricity demand:"),
        dcc.Slider(
            id="slider-electricity-demand",
            min=1000,
            max=4000,
            step=100,
            value=1000,
            marks={i: str(i) for i in range(0, 4001, 500)},
        )
    ]
)

@callback(
    Output("graph17", "figure"),
    Input("slider-wind-capacity", "value"),
    Input("slider-wind-availability", "value"),
    Input("slider-gas-capacity", "value"),
    Input("slider-coal-capacity", "value"),
    Input("slider-electricity-demand", "value"),
)

def calc(wind_capacity, wind_availability, gas_capacity, coal_capacity, electricity_demand):

    # carbon emissions in tCO2/MWh
    carbon_emissions = {"Wind": 0, "Coal": 0.1, "Gas": 0.05}
    # operational costs in £/MWh
    operational_costs = {"Wind": 0, "Coal": 8, "Gas": 10}
    # marginal costs in £/MWh
    carbon_price = 1
    marginal_costs = {"Wind": carbon_emissions['Wind'] * carbon_price + operational_costs['Wind'],
                    "Coal": carbon_emissions['Coal'] * carbon_price + operational_costs['Coal'],
                    "Gas": carbon_emissions['Gas'] * carbon_price + operational_costs['Gas']}
    # power plant capacities (nominal powers in MW)
    power_plant_p_nom = {'Bus': {"Coal": coal_capacity, "Wind": wind_capacity, "Gas": gas_capacity}}
    # country electrical loads in MW (not necessarily realistic)
    loads = {"Bus": [electricity_demand]}

    network = pypsa.Network()
    # snapshots labelled by [0,1,2,3]
    country = "Bus"
    network.set_snapshots(range(1))
    network.add("Bus", country)

    # p_max_pu is variable for wind
    for tech in power_plant_p_nom[country]:
        network.add(
            "Generator",
            "{} {}".format(country, tech),
            bus=country,
            p_nom=power_plant_p_nom[country][tech],
            marginal_cost=marginal_costs[tech],
            p_max_pu=([wind_availability] if tech == "Wind" else 1),
        )

    # load which varies over the snapshots
    network.add(
        "Load",
        "{} load".format(country),
        bus=country,
        p_set=np.array([electricity_demand]),
    )

    network.optimize(solver_name='highs')

    def demand_supply_diagram(period):

        # minimum marginal cost unit between gas and coal
        marginal_costs_ = marginal_costs
        del marginal_costs_['Wind']
        min_type = min(marginal_costs_, key=marginal_costs_.get)
        max_type = max(marginal_costs_, key=marginal_costs_.get)

        x0 = 0
        y0 = 0

        x1 = wind_capacity * network.generators_t.p_max_pu['Bus Wind'][period]
        y1 = 0

        x2 = x1
        y2 = marginal_costs[min_type]

        x3 = x2 + power_plant_p_nom['Bus'][min_type]
        y3 = y2

        x4 = x3
        y4 = marginal_costs[max_type]

        x5 = x4 + power_plant_p_nom['Bus'][max_type]
        y5 = y4

        fig = go.Figure()

        # Add shapes
        fig.add_shape(type="line",
            x0=x0, y0=y0, x1=x1, y1=y1,
            line=dict(color="RoyalBlue",width=3),
            label=dict(text="Wind")
        )
        fig.add_shape(type="line",
            x0=x1, y0=y1, x1=x2, y1=y2,
            line=dict(color="RoyalBlue",width=3)
        )
        fig.add_shape(type="line",
            x0=x2, y0=y2, x1=x3, y1=y3,
            line=dict(color="RoyalBlue",width=3),
            label=dict(text=min_type)
        )
        fig.add_shape(type="line",
            x0=x3, y0=y3, x1=x4, y1=y4,
            line=dict(color="RoyalBlue",width=3)
        )
        fig.add_shape(type="line",
            x0=x4, y0=y4, x1=x5, y1=y5,
            line=dict(color="RoyalBlue",width=3),
            label=dict(text=max_type)
        )
        fig.update_shapes(dict(xref='x', yref='y'))

        fig.add_vline(x=network.loads_t.p['Bus load'][period], line_color="green", annotation_text="Load", annotation_position="bottom right")

        fig.update_xaxes(range=[0, network.generators.p_nom.sum() + 10], title_text='Quantity')
        fig.update_yaxes(range=[0, y5 + 10], title_text='Price')
        fig.update_layout(showlegend=False, margin=dict(t=20, b=20))

        return fig

    fig = demand_supply_diagram(0)

    return fig
