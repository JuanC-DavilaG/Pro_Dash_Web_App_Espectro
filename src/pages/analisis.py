from datetime import date
from datetime import datetime
import base64
import io
import dash
from dash import Dash, dash_table, dcc, html, Input, Output, callback, ctx, callback_context
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import csv
from modules.leer_csv import *
from modules.disponible import *
from modules.variables import *
from modules.generar_portadoras import *
from modules.reporte_analisis import *
from flask import send_file

import os

opcionesCEs_0 = [
                {"label": "Libre", "value": "L"}, 
                {"label": "Protegido", "value": "P"}, 
                {"label": "S.M.M", "value": "S"},
            ]

opcionesCEs_1 = [
                {"label": "Fronteras", "value": "F"}, 
                {"label": "Determinado", "value": "C"},
                {"label": "Otros", "value": "O"},
            ]

dash.register_page(__name__, path='/analisis', name='Analizar', order=1)

layout = html.Div([

    dbc.Row([
        
        dbc.Col(
            html.Div([
                dcc.Upload(
                    id='datatable-upload',
                    accept=".CSV",
                    children=html.Div([
                        'Arrastrar y soltar o ',
                        html.A('Seleccionar archivo'),
                        ' ' + ETIQUETA_1
                    ]),
                )
            ], id='entrada_ET1')
        ),

        dbc.Col(
            html.Div([
                dcc.Upload(
                    id='datatable-upload-1',
                    accept=".CSV",
                    children=html.Div([
                        'Arrastrar y soltar o ',
                        html.A('Seleccionar archivo'),
                        ' ' + ETIQUETA_2
                    ]),
                )
            ], id='entrada_ET2')
        ),
        
    ],
    className="botones_SP",),

    dcc.Graph(id='datatable-upload-graph',
        figure=go.Figure(),style=style_graf_init,
    ),

    dbc.Row([
        dbc.Col(
            html.Div([
                dash_table.DataTable(id='datatable-upload-container',
                    page_action='none',
                    style_table = style_tabla,
                    style_header = header_tablas,
                    style_cell = cell_tablas,
                    style_data_conditional=[style_data_condition],
                    editable=True, 
                    row_deletable=True, 
                    page_size=12,
                ),
            ]), style={"width": "33.33%"}
        ),

        dbc.Col([
            dbc.Row([
                dbc.Col(
                    dbc.Row([
                        dbc.Col(
                            dbc.Checklist(
                                id='check-rangeslider',
                                options=[{'label': 'Deslizador', 
                                        'value': 'slider'}],
                                input_checked_style={
                                "backgroundColor": "rgba(33,134,244,0.5)",
                                "borderColor": "#555",
                                },
                                label_checked_style={"color": "rgba(33,134,244,0.5)"},
                                value=[''],
                            ),
                        ),
                        dbc.Col(
                            dbc.Input(id="int-can", placeholder="Canalización", type="text", style={'padding': '1px','width': "90%", 'color': '#A0AABA', 'backgroundColor': '#555', 'borderColor': 'rgb(63,63,63)', 'margin': '0 5px 0 0'}),
                        ),
                    ])

                ),
                dbc.Col(
                    dbc.Select(
                        id="select_band", placeholder="Bandas...",
                        options=[
                            {"label": "HF", "value": "HF"},
                            {"label": "VHF", "value": "VHF"},
                            {"label": "UHF", "value": "UHF"},
                            {"label": "SHF", "value": "SHF"},
                            {"label": "EHF", "value": "EHF", "disabled": True},
                        ],
                    )
                ),

            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Row([
                        dbc.Col(html.P("Segmento", style={'margin': '10px'}), width="auto", style={'color': '#A0AABA', 'padding': '0 0 0 38%'}),
                    ], style={'padding':'0 0 0 0%'}),
                    dbc.Row([
                            dbc.Input(id="seg_bajo", placeholder="Bajo", type="text", style={'width': "48%", 'color': '#A0AABA', 'backgroundColor': '#555', 'borderColor': 'rgb(63,63,63)', 'margin': '0 5px 0 0'}),
                            dbc.Input(id="seg_alto", placeholder="Alto", type="text", style={'width': "48%", 'color': '#A0AABA', 'backgroundColor': '#555', 'borderColor': 'rgb(63,63,63)'}),
                    ], style={"padding": "0px 0 0 15px"}),
                    dbc.Row([
                        dcc.Dropdown(
                                    ['Móvil', 
                                    'Móvil por satélite (Tierra-Espacio)', 
                                    'Móvil salvo móvil aeronáutico', 
                                    'Móvil marítimo (socorro y llamada por LLSD)',
                                    'Móvil marítimo',
                                    'Móvil Aeronáutico ®',
                                    ],
                                    ['Móvil'],
                                    id='Servis-dropdown',
                                    multi=True, 
                                    style=servis_dropdown),
                                    
                    ]),
                ]),

                dbc.Col(
                    dbc.Row([
                        dbc.Col([
                            dbc.Checklist(options = [{"label": "Todo", "value": "T", "disabled": True}], value = [], id="CEs",
                                                    input_checked_style={
                                                            "backgroundColor": "rgba(33,134,244,0.5)",
                                                            "borderColor": "#555",
                                                        },
                                                        label_checked_style={"color": "rgba(33,134,244,0.5)"},
                                                        inline=True),
                            dbc.Checklist(options = opcionesCEs_0, value=[], id="OpCEs_0",
                                                    input_checked_style={
                                                            "backgroundColor": "rgba(33,134,244,0.5)",
                                                            "borderColor": "#555",
                                                        },
                                                        label_checked_style={"color": "rgba(33,134,244,0.5)"}, 
                                                        inline=True),
                        ], style={"padding": "0 0 0 10px"}),
                        dbc.Col([
                            dbc.Checklist(options = opcionesCEs_1, value=[], id="OpCEs_1",
                                input_checked_style={
                                    "backgroundColor": "rgba(33,134,244,0.5)",
                                    "borderColor": "#555",
                                },
                                label_checked_style={"color": "rgba(33,134,244,0.5)"}, 
                                inline=True),
                        ], style={"padding": "27px 0 0 0"}),

                    ]), style={"padding-top": "10px"}
                )
            ]),

            dbc.Row([
                dbc.Col([
                    dbc.Button( "Guardar", active=True, id="btn-G", n_clicks=0, disabled=True),
                    dcc.Download(id="download-proposal"),
                ]),

                dbc.Col([
                    dbc.Button("Reporte", active=True, id="btn-R", n_clicks=0, disabled=False),
                    dcc.Download(id="download-reporte"),
                ]),

                dbc.Col([
                    dbc.Button("Ocupación", active=True, id="btn-O", n_clicks=0, disabled=False),
                    dcc.Download(id="download-ocupacion"),
                ]),

                dbc.Col([
                    dbc.Button("Iniciar", active=True, id="btn-I", n_clicks=0, disabled=True),
                ]),

            ], style={"padding": "20px 0 0 0"}),
        ], style={"width": "33.33%", "padding": "6px 6px 6px 6px"}),

        dbc.Col(
            html.Div([
                dash_table.DataTable(id='datatable-upload-1-container',
                    page_action='none',
                    style_table = style_tabla,
                    style_header = header_tablas,
                    style_cell = cell_tablas, 
                    style_data = data_table,
                    style_data_conditional=[style_data_condition],
                    editable=True, 
                    row_deletable=True, 
                    page_size=12,
                ),
            ]), style={"width": "33.33%"}
        ),
    ],

    className="tables_SP",),
    dbc.Row( # Tabla de resultados 
        dbc.Col(
            html.Div(id='tab_r')
        ),

    className="table_result")
])


# ************************ Funcional **************************** #

def parse_contents(contents, filename):
    
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)

    if 'csv' in filename:
        contenido = io.StringIO(decoded.decode('latin-1'))

        # Supongamos que el usuario cargó un archivo CSV.
        csv_reader = list(csv.reader(contenido, delimiter=','))

        return pd.DataFrame(leer_csv(csv_reader))

    elif 'xls' in filename:
        # Supongamos que el usuario cargó un archivo de Excel.
        return pd.read_excel(io.BytesIO(decoded))

def analizar_contenido(contents, filename):
    
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)

    if 'csv' in filename:
        # Supongamos que el usuario cargó un archivo CSV.
        return pd.read_csv(
            io.StringIO(decoded.decode('utf-8')))
            
    elif 'xls' in filename:
        # Supongamos que el usuario cargó un archivo de Excel.
        return pd.read_excel(io.BytesIO(decoded))

@callback(
    Output('datatable-upload-container', 'data'),
    Output('datatable-upload-container', 'columns'),
    Input('datatable-upload', 'contents'),
    State('datatable-upload', 'filename')
)
def update_output(contents, filename):
    if contents is None:
        return [], []
    df_S = parse_contents(contents, filename)

    df_S = df_S.rename_axis('#').reset_index()

    return df_S.to_dict('records'), [{"name": i, "id": i, 'deletable':True, 'renamable': True} for i in df_S.columns]

@callback(
    [Output('datatable-upload-1-container', 'data'),
    Output('datatable-upload-1-container', 'columns'),
    Output('btn-G',"disabled"),],
    [Input('datatable-upload-1', 'contents'),
    State('datatable-upload-1', 'filename'),
    State('btn-G', 'disabled')],
)
def update_output(contents, filename, btnG):

    lista = []
    diccionario = {}

    if contents is None:
        return [], [], True
    df_P = analizar_contenido(contents, filename)

    df_P = df_P.rename_axis('#').reset_index()

    return df_P.to_dict('records'), [{"name": i, "id": i, 'deletable': True, 'renamable': True} for i in df_P.columns], False

######### Inicio graficar y actualizar Espectro ***********************************

@callback(
    Output('datatable-upload-graph', 'figure'),
    Input('datatable-upload-container', 'data'),
    Input('datatable-upload-1-container', 'data'),
    Input("check-rangeslider", "value"),
    State('datatable-upload-graph', 'figure'),
)
def display_graph(rowsS, rowsP, value, fig):

    df_S = pd.DataFrame(rowsS)
    df_P = pd.DataFrame(rowsP, dtype = 'float64')

    datos=[]

    if (fig==None):

        fig = dict({
                    'data': [{
                        'x': [],
                        'y': [],
                        'type': 'markers'
                    }],'layout': style_graf
                })

        return fig


    if(not(df_S.empty) or len(df_S.columns) >= 1):

        df_S[["Frecuencias", 
            "P.I.R.E (dBW)", 
            "Anchos de banda"]] = df_S[["Frecuencias", 
                                    "P.I.R.E (dBW)", 
                                    "Anchos de banda"]].apply(pd.to_numeric)

        dS = genPor(df_S[df_S.columns[1]], 
                    df_S[df_S.columns[2]], 
                    df_S[df_S.columns[3]]
                    )

        df_GS = pd.DataFrame(data=dS)

        for i in range(len(df_GS)):
            objeto={

                'x': df_GS[df_GS.columns[0]][i],
                'y': df_GS[df_GS.columns[1]][i],
                'name': ETIQUETA_1,
                'showlegend': False,
                'mode': 'lines',
                'opacity': 0.9,
                'marker': {
                    'color': 'rgba(33,134,244,0.5)',
                    'size': 6,
                    'line': {
                        'width': 0.5, 
                        'color': 'rgba(255, 255, 255, 0)'
                    }
                }
            }

            datos.insert(i+1, objeto)


            if(len(datos)==0): 
                datos.insert(len(datos), objeto)

            else:
                datos.insert(len(datos)+i+1, objeto)
    
    if(not(df_P.empty) or len(df_P.columns) >= 1):

        framesXP = [df_P[df_P.columns[1]], df_P[df_P.columns[2]]]
        framesAP = [df_P[df_P.columns[3]], df_P[df_P.columns[3]]]
        framesYP = [df_P[df_P.columns[4]], df_P[df_P.columns[4]]]

        frecuencias = pd.concat(framesXP, ignore_index=True)
        Potencias = pd.concat(framesYP, ignore_index=True)
        Anchos_de_banda = pd.concat(framesAP, ignore_index=True)
        
        dP = genPor(frecuencias, 
                    Potencias, 
                    Anchos_de_banda)

        df_GP = pd.DataFrame(data=dP)

        for i in range(len(df_GP)):

            objeto={

                'x': df_GP[df_GP.columns[0]][i],
                'y': df_GP[df_GP.columns[1]][i],
                'name': ETIQUETA_2,
                'showlegend': False,
                'mode': 'lines',
                'opacity': 0.9,
                'marker': {
                    'color': 'rgba(244, 33, 33, 0.5)',
                    'size': 6,
                    'line': {
                        'width': 0.5, 
                        'color': 'rgba(255, 255, 255, 0)'
                    }
                }
            }

            if(len(datos)==0): 
                datos.insert(len(datos), objeto)

            else:
                datos.insert(len(datos)+i+1, objeto)

    dict_of_fig = dict({
                'data': datos, 
                'layout': style_graf_S
                })

    fig = go.Figure(dict_of_fig)

    fig.update_layout(
        xaxis_showgrid=True,
        yaxis_showgrid=True,
        xaxis_zeroline=True, 
        yaxis_zeroline=True,
        xaxis_gridcolor='rgba(63, 63, 63, 0.060)',
        yaxis_gridcolor='rgba(63, 63, 63, 0.060)',
        xaxis_zerolinecolor='rgb(63,63,63)',
        yaxis_zerolinecolor='rgb(63,63,63)',
        xaxis=dict(
            linecolor='rgba(0,0,0, 0)',
            rangeslider=dict(
            visible=True
        )

        ),
        yaxis=dict(
            linecolor='rgba(0,0,0, 0)',
        ),
)
    fig.update_layout( xaxis_rangeslider_visible='slider' in value )

    return fig

######### Fin graficar y actualizar Espectro ***********************************

@callback(
    Output("download-proposal", "data"),
    Input("btn-G", "n_clicks"),
    State('datatable-upload-1-container', 'data'),
    prevent_initial_call=True,
)
def guardarPropuesta(n, rowsP):

    df_P = pd.DataFrame(rowsP)

    if n is None:
        
        return []

    elif (n > 0):

        return dcc.send_data_frame(df_P.set_index('#').to_csv, ETIQUETA_2 + "_"+str(n)+"_.csv")

@callback(
    Output("download-ocupacion", "data"),
    Input("btn-O", "n_clicks"),
    State("int-can", "value"),
    State("select_band", "value"),
    State("seg_bajo", "value"),
    State("seg_alto", "value"),
    State("OpCEs_0", "value"),
    State("OpCEs_1", "value"),
    State('Servis-dropdown', 'value'),
    State('datatable-upload-container', 'data'),
)
def analizar(n, can, ban, bajo, alto, OpCEs_0, OpCEs_1, SerPer, rowO):

    if n is None:
        
        return []

    elif (n > 0):

        now = datetime.now()
        format = now.strftime('%d%m%y_%H-%M-%S')

        con = pd.DataFrame(rowO)['Frecuencias'].drop_duplicates().reset_index()

        df_O = Ocupacion(ban, float(can), float(bajo), float(alto), OpCEs_0+OpCEs_1, SerPer, con)

        return dcc.send_data_frame(df_O.to_excel, "Ocupación_"+format+".xlsx", index = False, sheet_name='Reporte de Ocupación')


@callback(
    Output("download-reporte", "data"),
    Input("btn-R", "n_clicks"),
    State('datatable-upload-container', 'data'),
    State('datatable-upload-1-container', 'data'),
)
def analizar(n, rowS, rowP):

    if n is None:

        return []

    elif (n > 0):

        now = datetime.now()
        format = now.strftime('%d%m%y_%H-%M-%S')

        dfS = pd.DataFrame(rowS)
        dfP = pd.DataFrame(rowP)

        df = EstudioDeInvacion(dfS, dfP)

        return dcc.send_data_frame(df.to_excel, "Reporte_"+format+".xlsx", index = False, sheet_name="Reporte de disponibilidad")

# ********************* Fin Funcional **************************** #
