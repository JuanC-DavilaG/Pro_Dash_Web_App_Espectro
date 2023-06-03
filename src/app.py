from dash import Dash, html, dcc
import dash
import dash_bootstrap_components as dbc

app = Dash(__name__, use_pages=True, title = "Proyecto dash", external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server

app._favicon = "favi.ico"

# Construye el contenido para el menú desplegable de Analisis.
contenidoAnalisis = [dbc.DropdownMenuItem(f"{page['name']}", href=page["relative_path"]) for page in dash.page_registry.values() if(page["location"] == "analisis")]
contenidoAnalisis.insert(0, dbc.DropdownMenuItem("Analisis", header=True))

# Construye el contenido general para el menú de navegación.
contenido = []
for page in dash.page_registry.values():
    if(page["location"] == "navbar"):
        if(page['name'] == 'Analisis'):
            contenido.append(dbc.DropdownMenu(
                                children=contenidoAnalisis,
                                nav=True,
                                in_navbar=True,
                                label="Analisis",
                            ))
        else:
            contenido.append(dbc.NavItem(dbc.NavLink(f"{page['name']}", href=page["relative_path"])))

# Cargamos el menu de navegación y los contenidos en la pagina.
app.layout = html.Div([    
    dbc.NavbarSimple(
                children=contenido,
                brand="SAR",
                brand_href="/",
                color="rgb(64, 64, 64)",
                dark=True,
                id='barra_navegacion'
            ),
    dash.page_container
])

if __name__ == '__main__':
	app.run_server(debug=True)