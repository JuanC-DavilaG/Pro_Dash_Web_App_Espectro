import dash
from dash import dash_table, dcc, html, Input, Output, callback, ctx
from dash.dependencies import State
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import base64
import io
from modules.variables import *
import geopandas as gpd
from bs4 import BeautifulSoup
from shapely import MultiPoint, MultiLineString, MultiPolygon, Polygon

dash.register_page(__name__, path='/Convierte', name='Convertir', order=2, location = "navbar")

layout = html.Div([
        dcc.Store(id='memory'),

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
                ['Puntos', 'Línea', 'Poligono', 'MultiGeo', ETIQUETA_1 + ' bind', ETIQUETA_1 + ' apart'],
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
def convertSHP(df, geo):

    filas = len(df)

    columnas = len(df.columns)

    shpres=[]

    contador = 0

    for i in range(1, int((columnas))):

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

    if geo['puntos']['hayPun']: return [MultiPoint(k) for k in shpres]

        
    elif geo['lineas']['hayLin']: return MultiLineString(shpres)


    elif geo['poligonos']['hayPoli']: 

        if geo['poligonos']['nPoli'] == 1: return Polygon(shpres[0])

        tupMiltiPoly = []
        listPolygons = []

        for i, polySHP in enumerate(shpres):
            if not(i):
                tupMiltiPoly.append(polySHP)
                continue
            listPolygons.append(polySHP)

        tupMiltiPoly.append(listPolygons)

        return MultiPolygon([tuple(tupMiltiPoly)])

# Concatena coordenas en el formato "ETIQUETA_1"
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


# ## 🛑🚧 ❗ TODO: Se realizaran posibles mejoras en futuras versiones. ❗ 🚧🛑 ## #

# KML en tablas
def kmlTablas(datos, offsetHeads, multiGeo):

    # Si hay multi geometrias tomamos los datos especificos
    # Si no hay multi geometras solo iteramos una vez y analizamos 
    # todos los datos en bruto.
    if (multiGeo):

        datos = datos 

    else:
    
        varAux = datos

        datos = "0"

    xyz=[]

    for i in datos:

        # Si hay multi geometrias toma los datos especificos 
        # si no los datos en bruto.
        i = i if (multiGeo) else varAux

        coord=[]
        heads=[]

        coord = [j.contents for j in i.findAll('coordinates')]

        for k in range(len(coord)):
            xyz.append(coord[k][0].strip().split(' '))

        tamaños = [ len(xyz[k]) for k in range(len(xyz)) ]

        n = mayor(tamaños)

        dataDEC=[]
        dataGMS = [ [] for k in range(n) ]

        for k in range(len(xyz)):
            heads.append("LATITUD_"+str(k+offsetHeads))
            heads.append("LONGITUD_"+str(k+offsetHeads))

        for k in range(n):
            
            for l in range(len(xyz)):

                try:

                    dataDEC.append((float(xyz[l][k].split(',')[0]), float(xyz[l][k].split(',')[1])))

                    dataGMS[k].append(dec2dms(float(xyz[l][k].split(',')[1]), "N"))
                    dataGMS[k].append(dec2dms(float(xyz[l][k].split(',')[0]), "W"))

                except:
            
                    dataGMS[k].append(float('nan'))
                    dataGMS[k].append(float('nan'))

    return dataGMS, heads, dataDEC

# ################################################################################ #

#Unir Listas y Hacerlas simetricas
def listasSimetricas(lista1, lista2):

    tamañoLista1=len(lista1)
    tamañoLista2=len(lista2)
    contador = 0

    masGrande = lista1 if tamañoLista1>tamañoLista2 else lista2
    masPequeño = lista2 if tamañoLista2<tamañoLista1 else lista1

    for i in masPequeño:
        masGrande[contador]=masGrande[contador]+i
        contador=contador+1

    for i in range(len(masPequeño), len(masGrande)):
        masGrande[i]=masGrande[i]+[float('nan'), float('nan')]

    return masGrande

def analizar_contenido(contents, filename):

    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)

    if 'csv' in filename:
        TGeo = {'tipo':'CSV'}

        # Supongamos que el usuario cargó un archivo CSV.
        return pd.read_csv(
            io.StringIO(decoded.decode('utf-8'))), TGeo
            
    elif 'xls' in filename:
        TGeo = {'tipo':'XLS'}

        # Supongamos que el usuario cargó un archivo de Excel.
        return pd.read_excel(io.BytesIO(decoded)), TGeo

    elif 'kml' in filename:

        TGeo = {'tipo':'KML', 
        'hayPoli': bool,
        'nPoli': int,
        'hayLin': bool,
        'nLin': int,
        'hayPun': bool,
        'nPun': int,
        }

        soup = BeautifulSoup(decoded, features="lxml")

        allData = soup.findAll('placemark')

        geometrias = tuple(TipeGeo.keys())[1:]

        poligonos = soup.findAll(marcadores[0])
        lineas = soup.findAll(marcadores[1])
        puntos = soup.findAll(marcadores[2])

# ############# Captura los nombres
        for nombre in allData:

            for j, marcador in enumerate(marcadores):

                if nombre.findAll(marcador):
                    try:

                        tam = len(TipeGeo[geometrias[j]]['data']['name'])

                        nombreAnterior = nombre.findAll('name')[0].contents[0] if(not(tam)) else TipeGeo[geometrias[j]]['data']['name'][-1]

                        nombreActual = nombre.findAll('name')[0].contents[0]

                        if not(nombreAnterior == nombreActual) or not(tam):

                            # Busca dentro de la data del placemark el nombre del poligono
                            TipeGeo[geometrias[j]]['data']['name'].append(nombre.findAll('name')[0].contents[0])

                        break
                    except:
                        TipeGeo[geometrias[j]]['data']['name'].append('S/n')

        TipeGeo['poligonos']['nPoli'] = len(poligonos)
        TipeGeo['poligonos']['hayPoli'] = TipeGeo['poligonos']['nPoli']>0

        TipeGeo['lineas']['nLin'] = len(lineas)
        TipeGeo['lineas']['hayLin'] = TipeGeo['lineas']['nLin']>0

        TipeGeo['puntos']['nPun'] = len(puntos)
        TipeGeo['puntos']['hayPun'] = TipeGeo['puntos']['nPun']>0

        TGeo['nPoli'] = len(poligonos)
        TGeo['hayPoli'] = TGeo['nPoli']>0

        TGeo['nLin'] = len(lineas)
        TGeo['hayLin'] = TGeo['nLin']>0

        TGeo['nPun'] = len(puntos)
        TGeo['hayPun'] = TGeo['nPun']>0

        #Busca si hay multigeometrias
        multiGeo = TipeGeo['poligonos']['hayPoli'] and TipeGeo['lineas']['hayLin'] or TipeGeo['lineas']['hayLin'] and TipeGeo['puntos']['hayPun'] or TipeGeo['poligonos']['hayPoli'] and TipeGeo['puntos']['hayPun']

        heads=[]
        dates=[]

####################################################################################

        if(TipeGeo['poligonos']['hayPoli']):
            dates, heads, TipeGeo['poligonos']['data']['geometry'] = kmlTablas(poligonos, 0, multiGeo) if (multiGeo) \
                else kmlTablas(soup, 0, multiGeo)

        if(TipeGeo['lineas']['hayLin']):

            if(TipeGeo['poligonos']['hayPoli']): 
                datosLineas, headsLin, TipeGeo['lineas']['data']['geometry'] = kmlTablas(lineas, TGeo['nPoli'], multiGeo)
                heads=heads+headsLin
                dates = listasSimetricas(dates, datosLineas)
            else:
                dates, heads, TipeGeo['lineas']['data']['geometry'] = kmlTablas(soup, 0, multiGeo)

        if(TipeGeo['puntos']['hayPun']):

            if(TipeGeo['poligonos']['hayPoli'] and TipeGeo['lineas']['hayLin']):
                datosPuntos, headspPun, TipeGeo['puntos']['data']['geometry'] = kmlTablas(puntos, TGeo['nPoli']+TGeo['nLin'], multiGeo)
                heads=heads+headspPun
                dates = listasSimetricas(dates, datosPuntos)
            elif(TipeGeo['poligonos']['hayPoli']):
                datosPuntos, headspPun, TipeGeo['puntos']['data']['geometry'] = kmlTablas(puntos, TGeo['nPoli'], multiGeo)
                heads=heads+headspPun
                dates = listasSimetricas(dates, datosPuntos)
            elif(TipeGeo['lineas']['hayLin']):
                datosPuntos, headspPun, TipeGeo['puntos']['data']['geometry'] = kmlTablas(puntos, TGeo['nLin'], multiGeo)
                heads=heads+headspPun
                dates = listasSimetricas(dates, datosPuntos)
            else:
                dates, heads, TipeGeo['puntos']['data']['geometry'] = kmlTablas(soup, 0, multiGeo)

        # print(TipeGeo) # Reactivar
####################################################################################

        return pd.DataFrame(dates, columns=heads), TipeGeo

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

#Representación de los datos de entrada en tablas.
@callback(
    [Output('CsvData', 'data'),
    Output('CsvData', 'columns')],
    Output('dropEntrada', 'children'),
    Output('memory', 'data'),
    [Input('files', 'contents'),
    State('files', 'filename'),
    State('memory', 'data')],
    prevent_initial_call=False,
)
def update_output(contents, filename, data):

    if contents is None:
        raise PreventUpdate

    data = data or {}

    df, tipoGeo = analizar_contenido(contents, filename)

    df = df.rename_axis('#').reset_index()

    return df.to_dict('records'), [{"name": i, "id": i, 'deletable': True, 'renamable': True} for i in df.columns], tipoGeo['tipo'], tipoGeo

#Representación en TextArea salida
@callback(
    Output('txtOutput', 'value'),
    [Input('dropEntrada', 'children'),
    Input('dropSalida', 'value'),
    Input('dropTipo', 'value'),
    Input("btn-O", "n_clicks")],
    State('CsvData', 'data'),
    State('memory', 'data'),
    prevent_initial_call=True,
)
def guardarPropuesta(tipoE, tipoS, tipoT, n, row, data):

    if (n is None): raise PreventUpdate

    elif (n > 0 and (ctx.triggered_id == "btn-O")):

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

                elif(tipoT == "Línea"):

                    return "En construcción"

                elif(tipoT == "Poligono"):

                    return "En construcción"
                
                elif(tipoT == "MultiGeo"):

                    return "En construcción"
                
                return "En construcción"

            elif tipoS == "shp":

                if (tipoT == "Puntos"):

                    return "No es posible convertir un archivo csv a shp de puntos"

                elif(tipoT == "Línea"):

                    return "En construcción"

                elif(tipoT == "Poligono"):

                    return "En construcción"

                elif(tipoT == "MultiGeo"):

                    return "En construcción"

                return "En construcción"

            elif tipoS == "csv":

                if (tipoT == "Puntos"):

                    return "En construcción"

                elif(tipoT == "Línea"):

                    return "En construcción"

                elif(tipoT == "Poligono"):

                    return "En construcción"

                elif(tipoT == "MultiGeo"):

                    return "En construcción"

                elif(tipoT == ETIQUETA_1 + " bind"):

                    rest = formatET1(df.drop(['#'], axis=1))

                    return rest.to_string(justify="justify-all", index=False)

                elif(tipoT == ETIQUETA_1 + " apart"):

                    return "En construcción"

                return "En construcción"

        elif (tipoE == "kml"):

            if (tipoS == "shp"):

                if (tipoT == "Puntos" and data['puntos']['hayPun'] and not(data['lineas']['hayLin'] or data['poligonos']['hayPoli'])):

                    return "El archivo de " + tipoT.upper() + " esta listo para su descarga con " + str(data['puntos']['nPun']) + " puntos "

                elif(tipoT == "Línea" and (data['lineas']['hayLin'] or data['poligonos']['hayPoli']) and not(data['puntos']['hayPun'])):

                    return "El archivo de " + tipoT.upper() + " esta listo para su descarga con " + str(data['lineas']['nLin']) + " lineas "

                elif(tipoT == "Poligono" and data['poligonos']['hayPoli'] and not(data['lineas']['hayLin'] or data['puntos']['hayPun'])):

                    return "El archivo de " + tipoT.upper() + " esta listo para su descarga con " + str(data['poligonos']['nPoli']) + " poligono "

                elif(tipoT == "MultiGeo"):

                    k = "{'name' : " + str(data['poligonos']['data']['name']+data['lineas']['data']['name']+data['puntos']['data']['name']) + "\n"
                    k += "   'data' : " + str(data['poligonos']['data']['geometry']+data['lineas']['data']['geometry']+data['puntos']['data']['geometry']) + "}"
                    return k

                return "Error en la configuración, favor de revisar"

        elif(tipoE == "SHP"):

            return "En construcción"

        return "Error en la configuración, favor de revisar"

# #Exporta los datos en archivos segun sea su tipo
@callback(
    Output("download-kml", "data"),
    Input("btn-1", "n_clicks"),
    State("txtOutput", "value"),
    State('dropSalida', 'value'),
    State('dropTipo', 'value'),
    State('CsvData', 'data'),
    State('memory', 'data'),
    prevent_initial_call=True,
)
def analizar(n, textKML, TipoS, Tipo, row, TGeo):

    if (n is None): raise PreventUpdate

    if(n > 0 and (ctx.triggered_id == "btn-1")):

        if (TipoS=="kml" and Tipo=="Puntos"):
            return dict(content=textKML, filename="coordenadas.kml")

        elif(TipoS=="shp" and (Tipo=="Puntos" or Tipo=="Línea" or Tipo=="Poligono")):

            df = pd.DataFrame(row)

            d = {'name': [], 'geometry': []}

            if(TGeo['poligonos']['hayPoli']):

                d['name'] = TGeo['poligonos']['data']['name']

                d['geometry'] = convertSHP(df.iloc[:, :TGeo['poligonos']['nPoli']*2+1], TGeo)

            if(TGeo['lineas']['hayLin']):

                d['name'] = TGeo['lineas']['data']['name']

                d['geometry'] = convertSHP(df.iloc[:, TGeo['poligonos']['nPoli']:TGeo['lineas']['nLin']*2+1], TGeo)

            if(TGeo['puntos']['hayPun']):

                d['name'] = TGeo['puntos']['data']['name']

                d['geometry'] = convertSHP(df.iloc[:, TGeo['poligonos']['nPoli'] + TGeo['lineas']['nLin']*2:], TGeo)


            gdf = gpd.GeoDataFrame(d, crs='epsg:4326')

            gdf.to_file("./temp/file.shp.zip", driver='ESRI Shapefile', mode="w")

            return dcc.send_file("./temp/file.shp.zip")

        elif(TipoS == "csv" and Tipo == ETIQUETA_1 + " bind"):

            df = pd.DataFrame(row)

            rest = formatET1(df.drop(['#'], axis=1))

            return dcc.send_data_frame(rest.to_csv, "Formato_" + ETIQUETA_1 + "_"+str(n)+"_.csv", index = False)
