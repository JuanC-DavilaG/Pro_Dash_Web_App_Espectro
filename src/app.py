from dash import Dash, html, dcc
import dash
import dash_bootstrap_components as dbc

app = Dash(__name__, use_pages=True, title = "Proyecto dash", external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server

app._favicon = "favi.ico"

app.layout = html.Div([    

    html.Div([

        html.Div(
                dcc.Link(
                    
                    f"{page['name']}", href=page["relative_path"],
                ),
        ) for page in dash.page_registry.values()
    ], id='Menu'),

	# html.H1('Proyecto Dash', id='Titulo'),

	dash.page_container
])

if __name__ == '__main__':
	app.run_server(debug=False)