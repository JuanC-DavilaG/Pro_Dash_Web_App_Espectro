import dash
from dash import Dash, dash_table, dcc, html, Input, Output, callback, ctx, callback_context
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
from modules.variables import *
import matplotlib.pyplot as plt
import geopandas as gpd
from bs4 import BeautifulSoup
from shapely import MultiLineString
from shapely import LineString
from shapely.geometry.polygon import Polygon
import zipfile

dash.register_page(__name__, path='/Convierte', name='Convertir', order=2)

layout = html.Div(
    [
        html.Div([
            html.P(id="DE", children=html.Div([html.Label(children="De: "), " ", html.Strong(id="dropEntrada", children="Sin archivo")])),
            html.Label(id="A", children='A: '),
            dcc.Dropdown(
                ['kml', 'shp', 'csv'],
                'kml',
                clearable=False,
                id="dropSalida"
            ),
            html.Label(id="TIPO", children='Tipo: '),
            dcc.Dropdown(
                ['Puntos', 'Lineas', 'Multilineas', 'Poligono', ETIQUETA_1 + ' bind', ETIQUETA_1 + ' apart'],
                'Puntos',
                clearable=False,
                id="dropTipo"
            ),
            html.Label(id="chkHeader", children=' La primera línea es un encabezado:'),
            dcc.Checklist(
                            [''],
                            [''],
                            id="check1"
                        ),
                ], id="checkEncabezado"),

        html.Div([
            html.P(id="paso1", children=html.Div([html.Strong(children="Paso 1:"),' Cargue su archivo '])),
            dcc.Upload(
                id='files',
                children=html.Div([
                    html.A('Seleccionar un archivo')
                ]),
            )
        ], id="paso_1"),

        html.Div([
            html.P(children=html.Div([html.Strong(children="Datos: "), html.Label(children="CSV:", id="tipoEntrada2")])),

            html.Div([
                dash_table.DataTable(id='CsvData',
                    style_table = style_tabla,
                    style_header = header_tablas,
                    style_cell = cell_tablas,
                    style_data_conditional=[style_data_condition],
                    editable=True, 
                    row_deletable=True,
                ),
                
            ]),
        ], id="datos_csv"),
        
        html.Div([
            html.P(children=html.Div([html.Strong(children="Paso 2:"),' Convierta los datos  ', html.Label(children="CSV", id="tipoEntrada3"), ' a ', html.Label(children="KML", id="tipoSalida1"), '.'])),
            dbc.Button("Convertir los datos CSV a KML.", active=True, id="btn-O", n_clicks=0, disabled=False)
        ], id="paso_2"),
        
        html.Div([
            html.P(children=html.Div([html.Strong(children="Datos: "), html.Label(children="KML:", id="tipoSalida2")])),
            dcc.Textarea(
                id='txtOutput',
                value='',
                wrap='off',
            )
        ], id="datos_kml"),

        html.Div([
            html.P(children=html.Div([html.Strong(children="Paso 3:"),' Descarga los datos  ', html.Label(children="KML", id="tipoSalida3"), ' en un archivo ', html.Label(children="KML", id="tipoSalida4"), '.'])),
            dbc.Button("Descarga archivo KML.", active=True, id="btn-1", n_clicks=0, disabled=False),
            dcc.Download(id="download-kml"),
        ], id="paso_3"),
        
        html.Div([
            html.P(children=html.Div([html.Strong(children="Paso 4:"),' Abre el archivo KML en ', html.A(children="Google Earth" ,href="https://earth.google.com/web/"), " o ", html.A(children="Google Maps" ,href="https://www.google.com/maps")]))
        ], id="paso_4"),

    ], id="contenedor")

# ************************ Funcional **************************** #

#Separar coordenadas
def bindCoordenadas(coordinates):

    degrees = int(float(coordinates) / 10000)

    minutes = int(abs(float(coordinates)) / 100)%100

    seconds = float(coordinates) % 100

    return degrees, minutes, seconds

# Convertir GMS a DEC
def dms2dec(coordenadas):

    grados, minutos, segundos = bindCoordenadas(coordenadas)
    dms2dec = grados + (float(minutos) / 60) + (float(segundos) / 3600)

    return dms2dec

# Convertir DEC a GMS
def dec2dms(coordenada, cardinal):

    if (cardinal.upper() == "N") or (cardinal.upper() == "E"):

        degrees = int(coordenada)
        minutes = int((coordenada - degrees)*60)
        seconds = int(((coordenada - degrees)*60 - minutes)*60)

    elif (cardinal.upper() == "S") or (cardinal.upper() == "W"):

        degrees = int(-1*coordenada)
        minutes = int((-1*coordenada - degrees)*60)
        seconds = int(((-1*coordenada - degrees)*60 - minutes)*60)

    dec2dms = str(degrees)

    if(int(minutes/10) == 0):
        minutos = "0" + str(minutes)

        dec2dms = dec2dms + minutos

    else:
        dec2dms = dec2dms + str(minutes)

    if(int(seconds/10) == 0):
        segundos = "0" + str(seconds)

        dec2dms = dec2dms + segundos

    else:
        dec2dms = dec2dms + str(seconds)
    
    return dec2dms

# Convierte dataframe a estructura multilineas
def convertSHP(df):

    filas = len(df)

    columnas = len(df.columns)

    shpres=[]

    contador = 0

    for i in range(1, int((columnas-1))):

        finalres=[]

        for j in range(filas):

            latitud = df[df.columns[i + contador]][j]

            longitud = df[df.columns[i + contador + 1]][j]

            if pd.isna(latitud) or pd.isna(longitud): break

            latlon=[]

            latlon.append(-1*float(dms2dec(float(longitud))))

            latlon.append(float(dms2dec(float(latitud))))

            finalres.append(tuple(latlon))

        shpres.append(tuple(finalres))

        contador+=1

        if ((i + contador + 1) == columnas): break


    return MultiLineString(shpres)

# Concatenta coordenas en el formato "ETIQUETA_1"
def formatET1(df):

    nElementos = int((len(df.columns)-1)/3)

    conta = 0

    listaResultante = []

    listaColumnas = []


    for i in range(1,nElementos+1):

        listaSalida = []

        for j in range(len(df)):

            grados = df[df.columns[i+conta]][j]
            minutos = df[df.columns[i+conta+1]][j]
            segundos = df[df.columns[i+conta+2]][j]

            salida = str(grados)

            salida = salida + "0" + str(minutos) if (minutos<10) else salida + str(minutos)

            salida = salida + "0" + str(segundos) if (segundos<10) else salida + str(segundos)

            listaSalida.append(salida)

        if i<nElementos:
            listaColumnas.append("Latitud."+str(i-1))
            listaColumnas.append("Longitud."+str(i-1))        

        listaResultante.append(listaSalida)


        if conta > 2: break

        conta+=2

    df1 = pd.DataFrame(np.array(list(zip(listaResultante[0], listaResultante[1]))), 
                        columns=listaColumnas)

    dfRest = pd.concat([df[df.columns[0]], df1], axis=1)

    return dfRest

    

# Encuentra el mayor numero de una lista
def mayor(lista):

    max = lista[0]

    for x in lista:

        if x > max:

            max = x

    return max 

def analizar_contenido(contents, filename):

    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)

    if 'csv' in filename:

        # Supongamos que el usuario cargó un archivo CSV.
        return pd.read_csv(
            io.StringIO(decoded.decode('utf-8'))), 'CSV'
            
    elif 'xls' in filename:

        # Supongamos que el usuario cargó un archivo de Excel.
        return pd.read_excel(io.BytesIO(decoded)), 'XLS'

    elif 'kml' in filename:

        soup = BeautifulSoup(decoded, features="lxml")

        coord=[]
        heads=[]
        xyz=[]
        for i in soup.findAll('coordinates'):
            coord.append(i.contents)

        for i in range(len(coord)):
            xyz.append(coord[i][0].strip().split(' '))

        tamaños = [ len(xyz[i]) for i in range(len(xyz)) ]

        n = mayor(tamaños)

        dates = [ [] for i in range(n) ]

        for i in range(len(xyz)):
            heads.append("LATITUD_"+str(i))
            heads.append("LONGITUD_"+str(i))

        for i in range(n):
            
            for j in range(len(xyz)):

                try:
                    dates[i].append(dec2dms(float(xyz[j][i].split(',')[1]), "N"))
                    dates[i].append(dec2dms(float(xyz[j][i].split(',')[0]), "W"))

                except:
            
                    dates[i].append(float('nan'))
                    dates[i].append(float('nan'))
            
        return pd.DataFrame(dates, columns=heads), 'KML'

@callback(
    [Output('tipoEntrada2', 'children'),
    Output('tipoEntrada3', 'children'),
    Output('tipoSalida1', 'children'),
    Output('tipoSalida2', 'children'),
    Output('tipoSalida3', 'children'),
    Output('tipoSalida4', 'children'),
    Output('btn-O', 'children'),
    Output('btn-1', 'children'),
    ],
    [Input('dropEntrada', 'children'),
    Input('dropSalida', 'value'),
    ],
)
def tipo_entradas(typeInput, typeOuput):

    tipoE = [typeInput.upper() for i in range(2)]
    
    tipoS = [typeOuput.upper() for i in range(4)]

    tipos = tipoE + tipoS

    tipos.append("Convertir los datos " + typeInput.upper() + " a " + typeOuput.upper() + ".")
    tipos.append("Descarga archivo " + typeOuput.upper() + ".")

    return tipos

#Representación en tabla entrada
@callback(
    [Output('CsvData', 'data'),
    Output('CsvData', 'columns')],
    Output('dropEntrada', 'children'),
    [Input('files', 'contents'),
    State('files', 'filename')],
    prevent_initial_call=False,
)
def update_output(contents, filename):

    if contents is None:
        return [], [], dash.no_update

    df, tipo = analizar_contenido(contents, filename)

    df = df.rename_axis('#').reset_index()

    return df.to_dict('records'), [{"name": i, "id": i, 'deletable': True, 'renamable': True} for i in df.columns], tipo

#Representación en TextArea salida
@callback(
    Output('txtOutput', 'value'),
    [Input('dropEntrada', 'children'),
    Input('dropSalida', 'value'),
    Input('dropTipo', 'value'),
    Input("btn-O", "n_clicks")],
    State('CsvData', 'data'),
    prevent_initial_call=True,
)
def guardarPropuesta(tipoE, tipoS, tipoT, n, row):

    if (n is None or n == 0):
        
        return ""

    elif (n > 0):
        
        tipoE = tipoE.lower()

        df = pd.DataFrame(row)

        if (tipoE == tipoS and tipoT != ETIQUETA_1 + " bind" and tipoT != ETIQUETA_1 + " apart"): 
            return "No es posible convertir archivos del tipo " + tipoE + " a archivos de tipo " + tipoS

        if (tipoE == "csv"):
            
            if (tipoS == "kml"):

                if (tipoT == "Puntos"):

                    k = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
                    k += "<kml xmlns=\"http://www.opengis.net/kml/2.2\" xmlns:gx=\"http://www.google.com/kml/ext/2.2\">\n"
                    k += " <Document id=\"feat_21\">\n"
                    k += " <name>Nombres de sitio por ubicación.</name>\n"

                    conta = 0

                    for i in range(len(df)):

                        nombre = str(df[df.columns[1]][i])

                        latitud  = str(dms2dec(df[df.columns[2]][i]))

                        longitud = str(-1*dms2dec(df[df.columns[3]][i]))

                        k += "	<Placemark id=\"feat_24\">\n"
                        k += "		<name>" + nombre + "</name>\n"
                        k += "		<Point id=\"geom_17\">\n"
                        k += "			<coordinates>" + longitud + "," + latitud + ",0.0</coordinates>\n"
                        k += "		</Point>\n"
                        k += "	</Placemark>\n"
                        
                    k += " </Document>\n</kml>"

                    return k

                elif(tipoT == "Lineas"):

                    return "En construcción"

                elif(tipoT == "Multilineas"):

                    return "En construcción"

                elif(tipoT == "Poligono"):

                    return "En construcción"

            elif tipoS == "shp":

                if (tipoT == "Puntos"):

                    return "No es posible convertir un archivo csv a shp de puntos"

                elif(tipoT == "Lineas"):

                    return "En construcción"

                elif(tipoT == "Multilineas"):

                    return "En construcción"

                elif(tipoT == "Poligono"):

                    return "En construcción"

                return "En construcción"

            elif tipoS == "csv":

                if (tipoT == "Puntos"):

                    return "En construcción"

                elif(tipoT == "Lineas"):

                    return "En construcción"

                elif(tipoT == "Multilineas"):

                    return "En construcción"

                elif(tipoT == "Poligono"):

                    return "En construcción"

                elif(tipoT == ETIQUETA_1 + " bind"):

                    rest = formatET1(df.drop(['#'], axis=1))

                    return rest.to_string(justify="justify-all", index=False)

                elif(tipoT == ETIQUETA_1 + " apart"):

                    return "En construcción"

                return "En construcción"

        elif (tipoE == "kml"):

            if (tipoS == "shp"):

                if (tipoT == "Puntos"):

                    return "No es posible convertir un archivo kml a shp de puntos"

                elif(tipoT == "Lineas"):

                    return "En construcción"

                elif(tipoT == "Multilineas"):

                    return "El archivo " + tipoT + " esta listo para su descargado "

                elif(tipoT == "Poligono"):

                    return "En construcción"

                return "En construcción"

        elif(tipoE == "SHP"):

            return "En construcción"

        return ""

# #Exporta los datos en archivos segun sea su tipo
@callback(
    Output("download-kml", "data"),
    Input("btn-1", "n_clicks"),
    State("txtOutput", "value"),
    State('dropSalida', 'value'),
    State('dropTipo', 'value'),
    State('CsvData', 'data'),
    prevent_initial_call=True,
)
def analizar(n, textKML, TipoS, Tipo, row):

    if (TipoS=="kml" and Tipo=="Puntos"):
        return dict(content=textKML, filename="coordenadas.kml")

    elif(TipoS=="shp" and Tipo=="Multilineas"):

        df = pd.DataFrame(row)

        poly = convertSHP(df)

        gdf = gpd.GeoDataFrame(index=[0], crs='epsg:4326', geometry=[poly])

        gdf.to_file("./temp/file.shp.zip", driver='ESRI Shapefile', mode="w")

        return dcc.send_file("./temp/file.shp.zip")

    elif(TipoS == "csv" and Tipo == ETIQUETA_1 + " bind"):

        df = pd.DataFrame(row)

        rest = formatET1(df.drop(['#'], axis=1))

        return dcc.send_data_frame(rest.to_csv, "Formato_" + ETIQUETA_1 + "_"+str(n)+"_.csv", index = False)
