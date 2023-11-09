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
        dcc.Graph(id="graph7"),
        html.P("Select supply curve intercept:"),
        dcc.Slider(
            id="slider-intercept",
            min=0,
            max=200,
            step=1,
            value=20,
            marks={i: str(i) for i in range(0, 201, 25)},
        ),
        html.P("Select supply curve slope:"),
        dcc.Slider(
            id="slider-slope",
            min=0.5,
            max=5,
            step=0.10,
            value=2,
            marks={i: str(i) for i in range(0, 6, 2)},
        ),
        html.P("Select market price:"),
        dcc.Slider(
            id="slider-price",
            min=0,
            max=200,
            step=1,
            value=50,
            marks={i: str(i) for i in range(0, 201, 25)},
        )
    ]
)

@callback(
    Output("graph7", "figure"),
    Input("slider-intercept", "value"),
    Input("slider-slope", "value"),
    Input("slider-price", "value")
)

def plot(intercept, slope, price):
    def supply_function(slope, intercept):
        x_ = np.arange(0.1, 100., 0.1)
        y_ = []
        for x in x_:
            y = slope * x + intercept
            y_.append(y)
        df_plot = pd.DataFrame({'Quantity': x_, 'Price': y_})
        return df_plot

    df_plot = supply_function(slope, intercept)
    # fig = df_plot.hvplot(kind='line', x='Quantity of fuel', y='Price of fuel', width=800, height=500, xlim=(0, 100), ylim=(0, 100))
    fig = px.line(df_plot, x='Quantity', y='Price', range_x=[0,50], range_y=[0,100])
    fig.update_traces(name='Supply curve', showlegend=True)
    quantity = (price - intercept) / slope
    producer_surplus = (price - intercept) * quantity / 2

    fig_shape = go.Figure(go.Scatter(x=[0,0,quantity], y=[intercept,price,price], line=dict(color="LightBlue"), fill="toself"))
    producer_surplus_text = "Producer surplus = " + str(round(producer_surplus, 2))
    fig_shape.update_traces(name=producer_surplus_text)

    fig = go.Figure(data=fig.data + fig_shape.data, layout = fig.layout)

    fig.add_shape(type="line", x0=0, y0=price, x1=quantity, y1=price, line=dict(color="red", width=3, dash="dash"))
    fig.add_shape(type="line", x0=quantity, y0=0, x1=quantity, y1=price, line=dict(color="grey", width=3, dash="dash"))

    return fig
