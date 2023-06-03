import dash
from dash import html, dcc, Input, Output, callback

dash.register_page(__name__, path='/tablas', name="Bases", order=3, location = "navbar")

layout = html.Div(children=[
    html.H1(children='Esta es nuestra pagina de Bases', id='titulo_tablas'),

    html.Div(children='''
        Este es el contenido de la pagina de Bases.
    ''', id='contenido_tablas'),

])