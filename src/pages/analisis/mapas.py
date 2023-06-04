import dash
from dash import dcc
import dash_bootstrap_components as dbc
from dash import Input, Output, State, html, callback
from dash.exceptions import PreventUpdate
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import plotly.graph_objects as go
import numpy as np
import geopandas as gpd
import shapely
import shapely.geometry
import datetime
import base64
import io
import zipfile
from os import mkdir
from shutil import rmtree
import sys
from queue import Queue
import threading
from modules.variables import capaMap

dash.register_page(
	__name__,
    path_template="/analisis/mapas",
    title='Analisis en mapas',
    description='Muestra una representación grafica de archivos en diversos formatos en mapas a seleccionar.', 
    order=1,
    location = "analisis"
)

progress_queue = Queue(1)
progress_memeory = 0


# Etiquetas de contenido
offcanvas = html.Div(
    [

        html.Div(
            [
                dcc.Graph(id="graficaMapa")
            ]
        ),

        dmc.Group(
            [
                dmc.ActionIcon(
                    DashIconify(icon="clarity:settings-line"), 
                    color="red", 
                    variant="filled",
                    id="open-offcanvas-scrollable",
                    n_clicks=0,
                )
            ],
            id='container-button_canvas'
        ),

        dbc.Offcanvas(
            html.Div(
                [
                    # dmc.Select(
                    #     label="Seleciona el mapa",
                    #     placeholder="Seleciona uno",
                    #     id="framework-select",
                    #     value=capaMap[0]["value"],
                    #     data=capaMap,
                    #     style={"width": 200, "marginBottom": 10},
                    # )
                    dcc.Dropdown(options=capaMap, 
                                 value=capaMap[0]["value"], 
                                 id="framework-select",),

                    dcc.Upload(
                        id='files',
                        children=html.Div([
                            html.A('Cargar archivo')
                        ]),
                    ),
                    dcc.Interval(id='clock', n_intervals=0, interval=500),
                    dbc.Progress(label='0%', value=0, max=100, id="progress_bar", striped=True, animated=True, style={"height": "13px"}),
                ]
            ),

            id="offcanvas-scrollable",
            scrollable=True,
            title="Configuaración del mapa",
            is_open=False,
            style={'background-color': 'rgb(14, 16, 18)', 'color':'#A0AABA'},
        ),
    ]
)

# Contenido de la pagina
layout = html.Div(children=offcanvas)

# ************************ Funcional **************************** #

def extraerCoordenadas(path, fig):

    geodf = gpd.read_file(path)

    fig = go.Figure(fig)
    
    try:
        geometrias = geodf.geometry

        if(hasattr(geodf, 'name')):
            nombres = geodf.name
        elif(hasattr(geodf, 'Callsign')):
            nombres = geodf.Callsign
        else:
            nombres = ["Geometria"]

    except:
        print("Oops! ", sys.exc_info()[0], "Occurend")

    lats = []
    lons = []
    names = []

    for feature, name in zip(geometrias, nombres):
        
        if isinstance(feature, shapely.geometry.linestring.LineString):

            name = name if name!="Geometria" else "Geo Linea"

            linestrings = [feature]

            # Determina en tamaño de la/las geometrias
            tam = len(linestrings)

            for i, linestring in enumerate(linestrings):

                # Calcula el valor del poligono en progreso como un porcentaje
                progreso = i*101/tam

                # Inicia un nuevo progreso en otro hilo, ejecutando la funcion start_work en cada poligono
                threading.Thread(target=start_work, args=(progress_queue, progreso,)).start()

                x, y = linestring.xy
                lats = np.append(lats, y)
                lons = np.append(lons, x)
                names = np.append(names, [name]*len(y))
                lats = np.append(lats, None)
                lons = np.append(lons, None)
                names = np.append(names, None)

            data=go.Scattermapbox(
                                mode = "lines",
                                lat = lats,
                                lon = lons,
                                marker = {'size': 10},
                                hoverinfo='text',
                                hovertext=names
                                )

        elif isinstance(feature, shapely.geometry.multilinestring.MultiLineString):

            name = name if name!="Geometria" else "Geo MiltiLinea"

            linestrings = feature.geoms
        
            # Determina en tamaño de la/las geometrias
            tam = len(linestrings)

            for i, linestring in enumerate(linestrings):

                # Calcula el valor del poligono en progreso como un porcentaje
                progreso = i*101/tam

                # Inicia un nuevo progreso en otro hilo, ejecutando la funcion start_work en cada poligono
                threading.Thread(target=start_work, args=(progress_queue, progreso,)).start()


                x, y = linestring.xy
                lats = np.append(lats, y)
                lons = np.append(lons, x)
                names = np.append(names, [name]*len(y))
                lats = np.append(lats, None)
                lons = np.append(lons, None)
                names = np.append(names, None)

            data=go.Scattermapbox(
                                mode = "lines",
                                lat = lats,
                                lon = lons,
                                marker = {'size': 10},
                                hoverinfo='text',
                                hovertext=names
                                )

        elif isinstance(feature, shapely.geometry.multipoint.MultiPoint):

            name = name if name!="Geometria" else "Geo Punto"

            linestrings = feature.geoms

            # Determina en tamaño de la/las geometrias
            tam = len(linestrings)

            for i, linestring in enumerate(linestrings):

                # Calcula el valor del poligono en progreso como un porcentaje
                progreso = i*101/tam

                # Inicia un nuevo progreso en otro hilo, ejecutando la funcion start_work en cada poligono
                threading.Thread(target=start_work, args=(progress_queue, progreso,)).start()

                x, y = linestring.xy
                lats = np.append(lats, y)
                lons = np.append(lons, x)
                names = np.append(names, [name]*len(y))
                lats = np.append(lats, None)
                lons = np.append(lons, None)
                names = np.append(names, None)

            data=go.Scattermapbox(
                                mode='markers',
                                lat=lats,
                                lon=lons,
                                marker={
                                    'size':7,
                                    'color':'rgb(255, 0, 0)',
                                    'opacity':0.7
                                },
                                hoverinfo='text+name',
                                hovertext=names
                                )

        elif isinstance(feature, shapely.geometry.polygon.Polygon):

            name = name if name!="Geometria" else "Geo Poligono"

            linestrings = [feature]
            poligonStrings = list(linestrings[0].exterior.coords)

            # Determina en tamaño de la/las geometrias
            tam = len(poligonStrings)

            for i, poligonString in enumerate(poligonStrings):
                # print('Coordenadas poligono: ', poligonString)

                # Calcula el valor del poligono en progreso como un porcentaje
                progreso = i*101/tam

                # Inicia un nuevo progreso en otro hilo, ejecutando la funcion start_work en cada poligono
                threading.Thread(target=start_work, args=(progress_queue, progreso,)).start()

                x, y = poligonString
                lats = np.append(lats, y)
                lons = np.append(lons, x)
                names = np.append(names, [name]*1)

            data=go.Scattermapbox(mode = "lines", 
                                fill = "toself",
                                lat = lats,
                                lon = lons,
                                hoverinfo='text',
                                hovertext=names)

        elif isinstance(feature, shapely.geometry.multipolygon.MultiPolygon):
                
            name = name if name!="Geometria" else "Geo MultiPoligono"
            linestrings = feature.geoms

            # Determina en tamaño de la/las geometrias
            tam = len(linestrings)

            for i, linestring in enumerate(linestrings):

                # Calcula el valor del poligono en progreso como un porcentaje
                progreso = i*101/tam

                # Inicia un nuevo progreso en otro hilo, ejecutando la funcion start_work en cada poligono
                threading.Thread(target=start_work, args=(progress_queue, progreso,)).start()

                poligonStrings = list(linestring.exterior.coords)

                for poligonString in poligonStrings:

                    x, y = poligonString
                    lats = np.append(lats, y)
                    lons = np.append(lons, x)
                    names = np.append(names, [name]*1)

                # Organizamos los poligonos como [|x0, y0|, None, |x1, y1|, None ...]
                lats = np.append(lats, None)
                lons = np.append(lons, None)
                names = np.append(names, None)

            # Traza Multipoligonos
            data=go.Scattermapbox(mode = "lines", 
                                    lat = lats,
                                    lon = lons,
                                    fill = "toself",
                                    hoverinfo='text',
                                    hovertext=names
                                )

        else:
            data=go.Scattermapbox()
            continue
    
    return fig.add_trace(data)

# Inicializa una figura con su layout, si la figura ya existe la actualiza.
@callback(
    Output("offcanvas-scrollable", "is_open"),
    Input("open-offcanvas-scrollable", "n_clicks"),
    State("offcanvas-scrollable", "is_open"),
)
def toggle_offcanvas_scrollable(n1, is_open):
    if n1:
        return not is_open
    return is_open

# Inicializa la capa grafica con mapas
@callback(
        Output("graficaMapa", "figure"), 
        [Input("framework-select", "value"),
        State("open-offcanvas-scrollable", "n_clicks"),
        State('graficaMapa', 'figure'),],
        )
def select_value(value, n, fig):
    if(fig is None):

        fig = go.Figure(go.Scattermapbox())

        fig.update_layout(mapbox_style="white-bg",
                            mapbox_center={'lon': -102, 'lat': 24},
                            mapbox_zoom=4.5,
                            mapbox_layers=[
                                {
                                    "below": 'traces',
                                    "sourcetype": "raster",
                                    "source": [value],
                                }
                            ],
                            showlegend = False,
                            margin={"r":0,"t":0,"l":0,"b":0}, 
                            clickmode='event+select',)
        
    else:
        fig = go.Figure(fig)

        fig.update_layout(mapbox_layers=[
                            {
                                "source": [value],
                            }
                        ]
                    )

    return fig

# Agrega los trazos
@callback(
    Output("graficaMapa", "figure", allow_duplicate=True),
    [Input('files', 'contents'),
    State('files', 'filename'),
    State('files', 'last_modified'),
    State("framework-select", "value"),
    State('graficaMapa', 'figure'),],
    prevent_initial_call=True,
)
def update_output(contents, filename, last_modified, value, fig):

    if(last_modified is None): raise PreventUpdate

    # El contenido necesita ser dividido. Contiene el tipo y el contenido real.
    content_type, content_string = contents.split(',')

    if(content_type == "data:application/x-zip-compressed;base64"):
        # Determina el elemento SHP
        is_shape = lambda string: string.endswith('shp')

        # Extrae el date time actual
        x = datetime.datetime.now()

        # construye el nombre del directorio badaso en la trama de tiempo
        nameFolder = "./temp/" + str(x.hour) + '.' + str(x.minute) + '.' + str(x.second) + '.' + str(x.microsecond)

        # Crea el directorio
        mkdir(nameFolder)

        # Decodificar la cadena base64
        content_decoded = base64.b64decode(content_string)
        # Usar BytesIO para manejar el contenido decodificado
        zip_str = io.BytesIO(content_decoded)
        # Usar ZipFile para tomar la salida de BytesIO
        zip_obj = zipfile.ZipFile(zip_str, 'r')
        # Extrae todos los archivos del comprimido en una carpeta temporal
        zip_obj.extractall(nameFolder)

        try:
            # Agrega un nuevo trazo apartir del archivo ingresado
            figureAdd = extraerCoordenadas(nameFolder, fig)
        finally:
            # Elimina carpetas y contenida
            rmtree(nameFolder)

            # Reiniciamos la barra de progreso a 0
            start_work(progress_queue, 0,)

    # return nuevaTazo
    return figureAdd

# Retorna el progreso a la barrar de progreso para actualizar su valor
@callback(
    [dash.Output("progress_bar", "value"),
     dash.Output("progress_bar", "label")],
    [dash.Input("clock", "n_intervals")])
def progress_bar_update(n):
    global progress_memeory
    if not progress_queue.empty():
        progress_bar_val = progress_queue.get()
        progress_memeory = progress_bar_val
    else:
        progress_bar_val = progress_memeory
    return(progress_bar_val, "{0:.2f}%".format(progress_bar_val))

# Inicia la operación de carga
def start_work(output_queue, i): 
    if output_queue.empty(): 
        output_queue.put(i)
