import dash
from dash import html, dcc

dash.register_page(__name__, path='/')

layout = html.Div([
    html.H1('Energy and Environmental Economics Apps'),
    html.Div([
        html.Div(
            dcc.Link(f"{page['name']} - {page['path']}", href=page["relative_path"])
        ) for page in dash.page_registry.values()
    ]),
])
