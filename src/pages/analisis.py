import dash
from dash import html

# Construye la entrada a las paginas de portadora y mapas
dash.register_page(__name__, 
                path="/analisis",
                order=1, 
                location = "navbar"
                )

layout = html.Div([])