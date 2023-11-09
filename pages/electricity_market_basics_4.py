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

wind_profile = np.random.uniform(low=0, high=1, size=(24,))
# load_profile = np.random.uniform(low=1000, high=1500, size=(24,))
layout = html.Div(
    [
        # html.H4("Budget constraint"),
        dcc.Graph(id="graph20"),
        dcc.Graph(id="graph21"),
        html.P("Select period:"),
        dcc.Slider(
            id="slider-period",
            min=0,
            max=23,
            step=1,
            value=0,
            marks={i: str(i) for i in range(0, 24, 1)},
        ),
    ]
)

@callback(
    Output("graph20", "figure"),
    Output("graph21", "figure"),
    Input("slider-period", "value")
)

def calc(period):

    # carbon emissions in tCO2/MWh
    carbon_emissions = {"Wind": 0, "Coal": 0.1, "Gas": 0.05}
    # operational costs in £/MWh
    operational_costs = {"Wind": 0, "Coal": 7, "Gas": 10}
    # marginal costs in £/MWh
    carbon_price = 80
    marginal_costs = {"Wind": carbon_emissions['Wind'] * carbon_price + operational_costs['Wind'],
                    "Coal": carbon_emissions['Coal'] * carbon_price + operational_costs['Coal'],
                    "Gas": carbon_emissions['Gas'] * carbon_price + operational_costs['Gas']}
    # power plant capacities (nominal powers in MW)
    wind_capacity = 2000
    power_plant_p_nom = {'Bus': {"Wind": wind_capacity, "Gas": 1000, "Coal": 4000}}

    network = pypsa.Network()
    # snapshots labelled by [0,1,2,3]
    country = "Bus"
    network.set_snapshots(range(24))
    network.add("Bus", country)

    # p_max_pu is variable for wind
    for tech in power_plant_p_nom[country]:
        network.add(
            "Generator",
            tech,
            bus=country,
            p_nom=power_plant_p_nom[country][tech],
            marginal_cost=marginal_costs[tech],
            p_max_pu=(wind_profile) if tech == "Wind" else 1)

    # load which varies over the snapshots
    network.add(
        "Load",
        "{} load".format(country),
        bus=country,
        p_set=[1000] * 24,
    )

    network.add(
        "StorageUnit",
        "Storage",
        bus="Bus",
        marginal_cost=0,
        inflow=0,
        p_nom_extendable=False,
        capital_cost=10,
        p_nom=2000,
        efficiency_dispatch=0.5,
        cyclic_state_of_charge=False,
        state_of_charge_initial=0,
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

        x1 = wind_capacity * network.generators_t.p_max_pu['Wind'][period]
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
        fig.update_traces(name='consumer_surplus_text')
        fig.update_shapes(dict(xref='x', yref='y'))


        fig.add_vline(x=network.loads_t.p['Bus load'][period], line_color="green", annotation_text="Load", annotation_position="bottom right")

        fig.update_xaxes(range=[0, network.generators.p_nom.sum() + 10], title_text='Quantity')
        fig.update_yaxes(range=[0, y5 + 10], title_text='Price')
        fig.update_layout(showlegend=False, margin=dict(t=20, b=20))
        

        return fig
    
    def generation_fig():
            
            fig = px.area(network.generators_t.p)#, facet_col=['Bus Coal', 'Bus Wind', 'Bus Gas'], facet_col_wrap=3, facet_row_spacing=0.05, facet_col_spacing=0.05)
            fig.update_yaxes(matches=None)
            fig.update_yaxes(title_text="Power (MW)")
            fig.update_xaxes(title_text="Period")
            fig.update_layout(showlegend=False, margin=dict(t=20, b=5))

            fig_storage = px.line(network.storage_units_t.p)
            fig_storage.update_traces(line_color='black', line_dash="dash")
            fig_storage.update_layout(showlegend=False, margin=dict(t=5, b=5))
            fig = go.Figure(data=fig.data + fig_storage.data, layout = fig.layout)
    
            return fig

    fig = demand_supply_diagram(period)
    fig2 = generation_fig()

    return fig, fig2
