import dash
from dash import html, dcc, html, Input, Output, callback
from dash.dependencies import State
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from openpyxl import Workbook, load_workbook
from openpyxl.utils import get_column_letter
import csv
import base64
import io
import matplotlib.pyplot as plt

dash.register_page(__name__, path='/CsvToKml', name='Coordenadas', order=2)

layout = html.Div(
    [
        html.Div([
            html.Label(id="chkHeader", children='La primera línea es un encabezado:'),
            dcc.Checklist(
                            [''],
                            [''],
                            id="check1"
                        )
        ], id="checkEncabezado"),

        html.Div([
            html.P(id="paso1", children=html.Div([html.Strong(children="Paso 1:"),' Cargue su archivo CSV'])),
            dcc.Upload(
                id='files',
                accept=".CSV",
                children=html.Div([
                    html.A('Seleccionar un archivo')
                ]),
            )
        ], id="paso_1"),

        html.Div([
            html.Label(children="Datos CSV:"),
            dcc.Textarea(
                id='txtCsvData',
                value='',
                wrap='off',
            )
        ], id="datos_csv"),
        
        html.Div([
            html.P(children=html.Div([html.Strong(children="Paso 2:"),' Convierta los datos CSV a KML.'])),
            dbc.Button("Convertir los datos CSV a KML.", active=True, id="btn-O", n_clicks=0, disabled=False)
        ], id="paso_2"),
        
        html.Div([
            html.Label(children="Datos KML:"),
            dcc.Textarea(
                id='txtOutput',
                value='',
                wrap='off',
            )
        ], id="datos_kml"),

        html.Div([
            html.P(children=html.Div([html.Strong(children="Paso 3:"),' Descarga los datos KML en un archivo KML.'])),
            dbc.Button("Descarga archivo KML.", active=True, id="btn-1", n_clicks=0, disabled=False),
            dcc.Download(id="download-kml"),
        ], id="paso_3"),
        
        html.Div([
            html.P(children=html.Div([html.Strong(children="Paso 4:"),' Abre el archivo KML en ', html.A(children="Google Earth" ,href="https://earth.google.com/web/"), " o ", html.A(children="Google Maps" ,href="https://www.google.com/maps")]))
        ], id="paso_4"),

    ], id="contenedor")

def dms2dec(coordenada):
    degrees = int(float(coordenada) / 10000)
    minutes = int(abs(float(coordenada)) / 100)%100
    seconds = float(coordenada) % 100
    dms2dec = degrees + (float(minutes) / 60) + (float(seconds) / 3600)
    return dms2dec

@callback(
    Output('txtCsvData', 'value'),
    Input('files', 'contents'),
    State('files', 'filename')
)
def update_output(contents, filename):

    if contents is None:
        return ""

    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)

    if 'csv' in filename:

        # Supongamos que el usuario cargó un archivo CSV.
        return (decoded.decode('utf-8'))

@callback(
    Output('txtOutput', 'value'),
    Input("btn-O", "n_clicks"),
    State('txtCsvData', 'value'),
    prevent_initial_call=True,
)
def guardarPropuesta(n, content):

    if n is None:
        
        return ""

    elif (n > 0):

        k = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
        k += "<kml xmlns=\"http://www.opengis.net/kml/2.2\" xmlns:gx=\"http://www.google.com/kml/ext/2.2\">\n"
        k += " <Document id=\"feat_21\">\n"
        k += " <name>Sitios de Analisis Prueba</name>\n"

        conta = 0

        for sitio in content.split('\n'):


            if(conta == 0 or len(sitio) < 3 ): 
                
                conta += 1
                
                continue

            nombre = str(sitio.split(',')[0])

            latitud  = str(dms2dec(sitio.split(',')[1]))

            longitud = str(-1*dms2dec(sitio.split(',')[2]))

            k += "	<Placemark id=\"feat_24\">\n"
            k += "		<name>" + nombre + "</name>\n"
            k += "		<Point id=\"geom_17\">\n"
            k += "			<coordinates>" + longitud + "," + latitud + ",0.0</coordinates>\n"
            k += "		</Point>\n"
            k += "	</Placemark>\n"
            
        k += " </Document>\n</kml>"

        return k

@callback(
    Output("download-kml", "data"),
    Input("btn-1", "n_clicks"),
    State("txtOutput", "value"),
    prevent_initial_call=True,
)
def analizar(n, textKML):

    # if n is None:
        
    #     return ""

    # elif (n > 0):

        return dict(content=textKML, filename="coordenadas.kml")