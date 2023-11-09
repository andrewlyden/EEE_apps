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
        dcc.Graph(id="graph3"),
        html.P("Select fuel price coefficient:"),
        dcc.Slider(
            id="slider-fuel",
            min=1,
            max=5,
            step=1,
            value=1,
            marks={i: str(i) for i in range(1, 6, 1)},
        ),
        html.P("Select coefficient for all other factors:"),
        dcc.Slider(
            id="slider-a",
            min=25,
            max=100,
            step=5,
            value=50,
            marks={i: str(i) for i in range(25, 101, 15)},
        )
    ]
)


@callback(
    Output("graph3", "figure"),
    Input("slider-fuel", "value"),
    Input("slider-a", "value")
)

def plot(fuel, a):
    def demand_function(fuel, a):
        x_ = np.arange(0.1, 100., 0.1)
        y_ = []
        for x in x_:
            y = a - fuel * x
            y_.append(y)
        df_plot = pd.DataFrame({'Quantity of fuel': x_, 'Price of fuel': y_})
        return df_plot

    df_plot = demand_function(fuel, a)
    # fig = df_plot.hvplot(kind='line', x='Quantity of fuel', y='Price of fuel', width=800, height=500, xlim=(0, 100), ylim=(0, 100))
    fig = px.line(df_plot, x='Quantity of fuel', y='Price of fuel', range_x=[0,100], range_y=[0,100])
    fig.update_traces(line_color='green')
    return fig
