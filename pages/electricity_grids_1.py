import pypsa, numpy as np
from pypsa.descriptors import get_switchable_as_dense as as_dense

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
        html.P("Stage 1: Wholesale market without network constraints"),
        html.Div(id='unified-costs'),
        dcc.Graph(id="graph22"),
        html.P("Stage 2: Redispatch with network constraints"),
        html.Div(id='redispatch-costs'),
        dcc.Graph(id="graph23"),
        html.P("Select wind capacity in Scotland:"),
        dcc.Slider(
            id="slider-wind-scotland",
            min=0,
            max=4000,
            step=1,
            value=4000,
            marks={i: str(i) for i in range(0, 4001, 250)},
        ),
        html.P("Select wind capacity in England:"),
        dcc.Slider(
            id="slider-wind-england",
            min=0,
            max=4000,
            step=1,
            value=4000,
            marks={i: str(i) for i in range(0, 4001, 250)},
        ),
        html.P("Select wind capacity in Wales:"),
        dcc.Slider(
            id="slider-wind-wales",
            min=0,
            max=4000,
            step=1,
            value=4000,
            marks={i: str(i) for i in range(0, 4001, 250)},
        ),
        html.P("Select gas capacity in Scotland:"),
        dcc.Slider(
            id="slider-gas-scotland",
            min=0,
            max=4000,
            step=1,
            value=2000,
            marks={i: str(i) for i in range(0, 4001, 250)},
        ),
        html.P("Select gas capacity in England:"),
        dcc.Slider(
            id="slider-gas-england",
            min=0,
            max=4000,
            step=1,
            value=4000,
            marks={i: str(i) for i in range(0, 4001, 250)},
        ),
        html.P("Select gas capacity in Wales:"),
        dcc.Slider(
            id="slider-gas-wales",
            min=0,
            max=4000,
            step=1,
            value=1000,
            marks={i: str(i) for i in range(0, 4001, 250)},
        ),
        html.P("Select tranmission capacity between Scotland and England:"),
        dcc.Slider(
            id="slider-transmission-SE",
            min=0,
            max=4000,
            step=1,
            value=1000,
            marks={i: str(i) for i in range(0, 4001, 250)},
        ),
        html.P("Select tranmission capacity between Wales and Scotland:"),
        dcc.Slider(
            id="slider-transmission-WS",
            min=0,
            max=4000,
            step=1,
            value=1000,
            marks={i: str(i) for i in range(0, 4001, 250)},
        ),
        html.P("Select tranmission capacity between England and Wales:"),
        dcc.Slider(
            id="slider-transmission-EW",
            min=0,
            max=4000,
            step=1,
            value=1000,
            marks={i: str(i) for i in range(0, 4001, 250)},
        ),
    ]
)

@callback(
    Output("graph22", "figure"),
    Output("graph23", "figure"),
    Output("unified-costs", "children"),
    Output("redispatch-costs", "children"),
    Input("slider-wind-scotland", "value"),
    Input("slider-wind-england", "value"),
    Input("slider-wind-wales", "value"),
    Input("slider-gas-scotland", "value"),
    Input("slider-gas-england", "value"),
    Input("slider-gas-wales", "value"),
    Input("slider-transmission-SE", "value"),
    Input("slider-transmission-WS", "value"),
    Input("slider-transmission-EW", "value"),

)

def calc(wind_capacity_scotland, wind_capacity_england, wind_capacity_wales,
         gas_capacity_scotland, gas_capacity_england, gas_capacity_wales,
         transmission_SE, transmission_WS, transmission_EW):

    # carbon emissions in tCO2/MWh
    carbon_emissions = {"Wind": 0, "Gas": 0.05}
    # operational costs in £/MWh
    operational_costs = {"Wind": 0, "Gas": 10}
    # marginal costs in £/MWh
    carbon_price = 1
    marginal_costs = {"Wind": carbon_emissions['Wind'] * carbon_price + operational_costs['Wind'],
                      "Gas": carbon_emissions['Gas'] * carbon_price + operational_costs['Gas']}
    # power plant capacities (nominal powers in MW)
    power_plant_p_nom = {'Scotland': {"Wind": wind_capacity_scotland, "Gas": gas_capacity_scotland},
                         'England': {"Wind": wind_capacity_england, "Gas": gas_capacity_england},
                         'Wales': {"Wind": wind_capacity_wales, "Gas": gas_capacity_wales}}
    # country electrical loads in MW (not necessarily realistic)
    loads = {"Scotland": 2000, 'England': 4000, 'Wales': 1000}
    # transmission capacities in MW (not necessarily realistic)
    transmission = {
        "Scotland": {"England": transmission_SE, "Wales": transmission_WS},
        "Wales": {"England": transmission_EW},
    }

    network = pypsa.Network()

    # snapshots labelled by [0,1,2,3]
    country = ["Scotland", 'England', 'Wales']
    coordinates = {'Scotland': {'y': 57., 'x': -4.2}, 'England': {'y': 52.1, 'x': 0.17}, 'Wales': {'y': 52.0, 'x': -3.8}}
    network.set_snapshots(range(1))
    for c in country:
        network.add("Bus", c, x=coordinates[c]['x'], y=coordinates[c]['y'])

    # p_max_pu is variable for wind
    for c in country:
        if c == 'Scotland':
            wind_availability = 0.8
        elif c == 'England':
            wind_availability = 0.4
        elif c == 'Wales':
            wind_availability = 0.6
        for tech in power_plant_p_nom[c]:
            network.add(
                "Generator",
                "{} {}".format(c, tech),
                bus=c,
                p_nom=power_plant_p_nom[c][tech],
                marginal_cost=marginal_costs[tech],
                p_max_pu=([wind_availability] if tech == "Wind" else 1),
            )

    # load which varies over the snapshots
    for c in country:
        network.add(
            "Load",
            "{} load".format(c),
            bus=c,
            p_set=np.array([loads[c]]),
        )

    network.add(
        "Line",
        "Scotland to England line",
        bus0='Scotland',
        bus1='England',
        s_nom=transmission['Scotland']['England'],
        x=0.1,
        r=0.01,
    )
    network.add(
        "Line",
        "Wales to Scotland line",
        bus0='Wales',
        bus1='Scotland',
        s_nom=transmission['Scotland']['Wales'],
        x=0.1,
        r=0.01,
    )
    network.add(
        "Line",
        "England to Wales line",
        bus0='England',
        bus1='Wales',
        s_nom=transmission['Wales']['England'],
        x=0.1,
        r=0.01,
    )

    network_unified = network.copy()
    network_redispatch = network.copy()

    network.optimize(solver_name='highs')
    nodal_costs = network.statistics().dropna()['Operational Expenditure'].values[0]
    nodal_costs = 'Nodal costs: £' + str(round(nodal_costs, 2))


    # print(network.buses_t.marginal_price.values[0])

    # remap to single bus
    network_unified.mremove("Bus", network_unified.buses.index)
    network_unified.add("Bus", "Unified", x=-1.67, y=54.01)
    network_unified.mremove("Line", network_unified.lines.index)
    network_unified.generators.bus = ["Unified"] * 6
    network_unified.loads.bus = "Unified"

    # network_unified.consistency_check()

    # Now, we can solve the coupled market with single bidding zone.
    network_unified.optimize(solver_name='highs')
    unified_costs = network_unified.statistics().dropna()['Operational Expenditure'].values[0]
    unified_costs = 'Unified costs: £' + str(round(unified_costs, 2))

    # next can build a redispatch model
    p = network_unified.generators_t.p / network_unified.generators.p_nom
    network_redispatch.generators_t.p_min_pu = p
    network_redispatch.generators_t.p_max_pu = p

    # set rules to generators
    g_up = network_redispatch.generators.copy()
    g_down = network_redispatch.generators.copy()

    g_up.index = g_up.index.map(lambda x: x + " ramp up")
    g_down.index = g_down.index.map(lambda x: x + " ramp down")

    up = (
        as_dense(network_unified, "Generator", "p_max_pu") * network_unified.generators.p_nom - network_unified.generators_t.p
    ).clip(0) / network_unified.generators.p_nom
    down = -network_unified.generators_t.p / network_unified.generators.p_nom

    up.columns = up.columns.map(lambda x: x + " ramp up")
    down.columns = down.columns.map(lambda x: x + " ramp down")

    network_redispatch.madd("Generator", g_up.index, p_max_pu=up, **g_up.drop("p_max_pu", axis=1))

    network_redispatch.madd(
        "Generator",
        g_down.index,
        p_min_pu=down,
        p_max_pu=0,
        **g_down.drop(["p_max_pu", "p_min_pu"], axis=1)
    )

    # then solve
    network_redispatch.optimize(solver_name='highs')
    redispatch_costs = network_redispatch.statistics().dropna()['Operational Expenditure'].values[0]
    redispatch_costs = 'Redispatch costs: £' + str(round(redispatch_costs, 2))

    def network_figure():

        # plot the network
        df1 = network_unified.buses.reset_index()
        df1['Gas'] = gas_capacity_scotland + gas_capacity_england + gas_capacity_wales
        df1['Wind'] = wind_capacity_scotland + wind_capacity_england + wind_capacity_wales
        df1['Price'] = network_unified.buses_t.marginal_price.values[0]

        fig1 = go.Figure(go.Scattermapbox(mode="markers",
                                          lon=[df1['x'][0]],
                                          lat=[df1['y'][0]],
                                          line_color='blue',
                                          marker = {'size': 10},
                                          customdata=df1[['Bus', 'Gas', 'Wind', 'Price']],
                                          hovertemplate ="%{customdata[0]}: <br>Gas: %{customdata[1]} </br>Wind: %{customdata[2]} <br>Price: %{customdata[3]} </br>",
                                          name="",
                                          showlegend=False,
                                          )
                        )
        fig1.update_layout(
            margin ={'l':0,'t':0,'b':0,'r':0},
            mapbox={'center': {'lon': -2, 'lat': 54},
                    'style': "carto-positron",
                    'zoom': 4.5},
            height=500, width=500)

        # plot the network
        # gen2 = network_redispatch.generators.assign(g=network_redispatch.generators_t.p.mean()).groupby(["bus"]).g.sum()
        # fig = network.iplot(
        #     size=(500, 500), mapbox=True, mapbox_style='carto-positron', mapbox_parameters={'zoom': 5, 'hover_data': [network.generators.p_nom]}, iplot=False,
        #     bus_sizes=gen / 1e2,
        #     # bus_colors={"gas": "indianred", "wind": "midnightblue"},
        #     line_widths=4,)

        df2 = network_redispatch.buses.reset_index()
        df2['Gas'] = [gas_capacity_scotland, gas_capacity_england, gas_capacity_wales]
        df2['Wind'] = [wind_capacity_scotland, wind_capacity_england, wind_capacity_wales]
        df2['Price'] = network_redispatch.buses_t.marginal_price.values[0]

        fig2 = go.Figure(go.Scattermapbox(mode="markers+lines",
                                        lon=[df2['x'][0], df2['x'][1], df2['x'][2]],#, df1['x'][0]],
                                        lat=[df2['y'][0], df2['y'][1], df2['y'][2]],#, df1['y'][0]],
                                        line_color='blue',
                                        marker = {'size': 10},
                                        customdata=df2[['Bus', 'Gas', 'Wind', 'Price']],
                                        hovertemplate ="%{customdata[0]}: <br>Gas: %{customdata[1]} </br>Wind: %{customdata[2]} <br>Price: %{customdata[3]} </br>",
                                        name="",
                                        showlegend=False,
                                        )
                        )
        fig2.update_layout(
            margin ={'l':0,'t':0,'b':0,'r':0},
            mapbox={'center': {'lon': -2, 'lat': 54},
                    'style': "carto-positron",
                    'zoom': 4.5},
            height=500, width=500)

        fig3 = go.Figure(go.Scattermapbox(mode="lines",
                                        lon=[df2['x'][2], df2['x'][0]],
                                        lat=[df2['y'][2], df2['y'][0]],
                                        line_color='blue',
                                        # marker = {'size': 10},
                                        # text=df1['Bus'],
                                        # customdata=df1[['Bus', 'Gas', 'Wind']],
                                        # hovertemplate ="%{customdata[0]}: <br>Gas: %{customdata[1]} </br>Wind: %{customdata[2]}",
                                        name="",
                                        showlegend=False
                                        )
                        )

        fig2 = go.Figure(data=fig3.data + fig2.data, layout=fig2.layout)

        # output1 = network.lines_t.p0.columns[0] + ' = ' + network.lines_t.p0.iloc[0, 0].round(0).astype(str)
        # output2 = network.lines_t.p0.columns[1] + ' = ' + network.lines_t.p0.iloc[0, 1].round(0).astype(str)
        # output3 = network.lines_t.p0.columns[2] + ' = ' + network.lines_t.p0.iloc[0, 2].round(0).astype(str)
        # output4 = 'Unified price = ' + network_unified.buses_t.marginal_price.values[0][0].astype(str)

        return fig1, fig2

    fig1, fig2 = network_figure()

    return fig1, fig2, unified_costs, redispatch_costs
