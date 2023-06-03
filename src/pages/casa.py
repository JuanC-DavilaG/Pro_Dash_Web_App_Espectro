import dash
from dash import html, dcc

dash.register_page(__name__, path='/', order=0, location = "navbar")

layout = html.Div(children=[
    html.H1(children='Esta es nuestra pagina de inicio', id='titulo_casa'),

    html.Div(children='''
        Este es el contenido de la pagina de inicio.
    ''', id='contenido_casa'),

])