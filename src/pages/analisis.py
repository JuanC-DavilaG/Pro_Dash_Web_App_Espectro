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

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# app = Dash(__name__, title = "Proyecto dash", external_stylesheets=external_stylesheets)
# app = Dash(__name__, use_pages=True, title = "Proyecto dash", external_stylesheets=[dbc.themes.BOOTSTRAP])

opcionesCEs_0 = [
                {"label": "E. Libre", "value": "L"}, 
                {"label": "E. Protegido", "value": "P"}, 
                {"label": "S.M.M", "value": "S"},
            ]

opcionesCEs_1 = [
                {"label": "E. Fronteras", "value": "F"}, 
                {"label": "CNAF", "value": "C"},
                {"label": "Otros", "value": "O"},
            ]

dash.register_page(__name__)
# app.title = "Dashboard"

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
                        ' SIAER'
                    ]),
                )
            ], id='entrada_siaer')
        ),
        dbc.Col(
            html.Div([
                dcc.Upload(
                    id='datatable-upload-1',
                    accept=".CSV",
                    children=html.Div([
                        'Arrastrar y soltar o ',
                        html.A('Seleccionar archivo'),
                        ' Propuesta'
                    ]),
                )
            ], id='entrada_propuesta')

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
                    # filter_action='native',
                    style_table = style_tabla,
                    style_header = header_tablas,
                    style_cell = cell_tablas,
                    style_data = data_table,
                    editable=True, 
                    row_deletable=True, 
                    page_size=12,
                    # fixed_rows={'headers': True},
                ),
            ]), style={"width": "33.33%"}
            # id='tabla_1'
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
                                # style={'color': '#A0AABA', 'padding': '0% 0%  0% 1%'}
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
                        # dbc.Col(html.P(""), width="auto", style={'color': '#A0AABA'}),
                    ], style={'padding':'0 0 0 0%'}),

                    dbc.Row([
                        # dbc.Col(
                            dbc.Input(id="seg_bajo", placeholder="Bajo", type="text", style={'width': "48%", 'color': '#A0AABA', 'backgroundColor': '#555', 'borderColor': 'rgb(63,63,63)', 'margin': '0 5px 0 0'}),
                        # ),
                        # dbc.Col(
                            dbc.Input(id="seg_alto", placeholder="Alto", type="text", style={'width': "48%", 'color': '#A0AABA', 'backgroundColor': '#555', 'borderColor': 'rgb(63,63,63)'}),
                        # ),
                        # MIC2022-000040
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
                    # html.Div(id='estado',children='', style={"color": "white"})
                ]),
                dbc.Col([
                    dbc.Button("Reporte", active=True, id="btn-R", n_clicks=0, disabled=False),
                    dcc.Download(id="download-reporte"),
                    # html.Div(id='estado',children='', style={"color": "white"})
                ]),
                dbc.Col([
                    dbc.Button("Ocupación", active=True, id="btn-O", n_clicks=0, disabled=False),
                    # download-ocupacion
                    dcc.Download(id="download-ocupacion"),
                    # html.Div(id='estado',children='', style={"color": "white"})
                ]),
                dbc.Col([
                    dbc.Button("Iniciar", active=True, id="btn-I", n_clicks=0, disabled=True),
                    # html.Div(id='estado',children='', style={"color": "white"})
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
                    editable=True, 
                    row_deletable=True, 
                    page_size=12,
                    # fixed_rows={'headers': True},
                ),
                    
                # html.Button('Más Filas', id='editing-rows-button', n_clicks=0)
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
# @callback(
#     Output("OpCEs", "value"),
#     Output("CEs", "value"),
#     Input("OpCEs", "value"),
#     Input("CEs", "value"),
# )
# def sync_checklists(cities_selected, all_selected):
#     ctx_l = callback_context
#     input_id = ctx_l.triggered[0]["prop_id"].split(".")[0]
#     if input_id == "OpCEs":
#         all_selected = ["Todo"] if set(cities_selected) == set(opcionesCEs) else []
#     else:
#         cities_selected = opcionesCEs if all_selected else []
#     return cities_selected, all_selected


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

# @app.callback(Output('datatable-upload-1-container', 'data'),
#               Input('editing-rows-button', 'n_clicks'),
#               State('datatable-upload-1-container', 'data'),
#               State('datatable-upload-1-container', 'columns'))
# def add_row(n_clicks, rows, columns):
#     if n_clicks > 0:
#         rows.append({c['id']: '' for c in columns})
#     return rows

@callback(
    Output('datatable-upload-container', 'data'),
    Output('datatable-upload-container', 'columns'),
    Input('datatable-upload', 'contents'),
    State('datatable-upload', 'filename')
)
def update_output(contents, filename):
    if contents is None:
        return [{}], []
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
        return [{}], [], True
    df_P = analizar_contenido(contents, filename)

    df_P = df_P.rename_axis('#').reset_index()

    return df_P.to_dict('records'), [{"name": i, "id": i, 'deletable': True, 'renamable': True} for i in df_P.columns], False

# @callback(
#     Output('datatable-upload-graph', 'figure'),
#     Input('datatable-upload-container', 'data'),
#     Input('datatable-upload-1-container', 'data'),
#     State('datatable-upload-graph', 'figure'),
# )
# def update_figure(rows_0, rows_1, fig):

#     if(len(fig['data'])>1): 
#         nombre = fig['data'][1]['name']

#         if(len(fig['data'])>2):
#             pass
#     # else:
#     #     nombre = ''

#     df_S = pd.DataFrame(rows_0)
#     df_P = pd.DataFrame(rows_1)
#     fig = go.Figure(fig)

#     # print((df_S.empty),  df_P.empty)

#     # print('siaer: ', ((df_P.empty) and not(df_S.empty)))

#     # print('propuesta: ', ((df_S.empty) and not(df_P.empty)))

#     # print()

#     # if (df_S.empty and df_P.empty or len(df_S.columns) < 1 and len(df_P.columns) < 1):
#     if(df_S.empty and df_P.empty):

#         fig.add_trace(
#             go.Scatter(
#                 x=[], 
#                 y=[],
#                 mode='markers',
#                 # marker=dict(borderColor = rgb(63,63,63))
#             )
#         )
        
#     elif((df_P.empty) and not(df_S.empty)):

#         fig.add_trace(
#             go.Scatter(
#                 x=df_S[df_S.columns[0]], 
#                 y=df_S[df_S.columns[1]],
#                 name='Siaer',
#                 mode='markers',
#                 marker=dict(color='rgba(33,134,244,0.5)')
#                 # style={
#                 #     plot_bgcolor: #161A1D
#                 #     },
#             )
#         )

#     elif((df_S.empty) and not(df_P.empty)):

#         fig.add_trace(
#             go.Scatter(
#                 x=df_P[df_P.columns[0]], 
#                 y=df_P[df_P.columns[3]],
#                 name='Propuesta',
#                 mode='markers',
#                 marker=dict(color='rgba(244, 33, 33, 0.5)')
#                 # style={
#                 #     plot_bgcolor: #161A1D
#                 #     },
#             )
#         )

#     elif(not(df_S.empty) and not(df_P.empty)):

#         if(nombre == 'Siaer'):

#             fig.add_trace(
#                 go.Scatter(
#                     x=df_P[df_P.columns[0]], 
#                     y=df_P[df_P.columns[3]],
#                     name='Propuesta',
#                     mode='markers',
#                     marker=dict(color='rgba(244, 33, 33, 0.5)')
#                     # style={
#                     #     plot_bgcolor: #161A1D
#                     #     },
#                 )
#             )
#         elif(nombre == 'Propuesta'):

#             fig.add_trace(
#                 go.Scatter(
#                     x=df_S[df_S.columns[0]], 
#                     y=df_S[df_S.columns[1]],
#                     name='Siaer',
#                     mode='markers',
#                     marker=dict(color='rgba(33,134,244,0.5)')
#                     # style={
#                     #     plot_bgcolor: #161A1D
#                     #     },
#                 )
#             )



#     fig.update_layout(style_graf)

    # fig.update_layout(
    #     xaxis_showgrid=True,
    #     yaxis_showgrid=True,
    #     xaxis_zeroline=True, 
    #     yaxis_zeroline=True,
    #     xaxis_gridcolor='rgba(63, 63, 63, 0.060)',
    #     yaxis_gridcolor='rgba(63, 63, 63, 0.060)',
    #     xaxis_zerolinecolor='rgb(63,63,63)',
    #     yaxis_zerolinecolor='rgb(63,63,63)',
    #     xaxis=dict(
    #         linecolor='rgba(0,0,0, 0)',
    #         # linecolor='rgb(63,63,63)',

    #     ),
    #     yaxis=dict(
    #         linecolor='rgba(0,0,0, 0)',
    #         # linecolor='rgb(63,63,63)',
    #     ),
    # )

#     return fig

######### Inicio graficar y actualizar Portadoras ***********************************

# @callback(
#     Output('datatable-upload-graph', 'figure'),
#     Input('datatable-upload-container', 'data'),
#     Input('datatable-upload-1-container', 'data'),
#     Input("check-rangeslider", "value"),
#     State('datatable-upload-graph', 'figure'),
# )
# def display_graph(rowsS, rowsP, value, fig):
#     df_S = pd.DataFrame(rowsS)
#     df_P = pd.DataFrame(rowsP)

#     datos=[]

#     if (fig==None):

#         fig = dict({
#                     'data': [{
#                         'x': [],
#                         'y': [],
#                         'type': 'markers'
#                     }],'layout': style_graf
#                 })

#         return fig

#         # return 
#         # {
#         #     'data': [{
#         #         'x': [],
#         #         'y': [],
#         #         'type': 'markers'
#         #     }],'layout': style_graf
#         # }

#     if(not(df_S.empty) or len(df_S.columns) >= 1):

#         objeto={

#             'x': df_S[df_S.columns[1]],
#             'y': df_S[df_S.columns[2]],
#             'name': 'SIAER',
#             'mode': 'markers',
#             'opacity': 0.9,
#             'marker': {
#                 'color': 'rgba(33,134,244,0.5)',
#                 'size': 6,
#                 'line': {
#                     'width': 0.5, 
#                     'color': 'rgba(255, 255, 255, 0)'
#                 }
#             }
#         }

#         if(len(datos)==0): 
#             datos.insert(0, objeto)

#         else:
#             datos.insert(1, objeto)
    
#     if(not(df_P.empty) or len(df_P.columns) >= 1):

#         framesXP = [df_P[df_P.columns[1]], df_P[df_P.columns[2]]]
#         framesYP = [df_P[df_P.columns[4]], df_P[df_P.columns[4]]]

#         resultXP = pd.concat(framesXP)
#         resultYP = pd.concat(framesYP)

#         objeto={

#             'x': resultXP,
#             'y': resultYP,
#             'name': 'Propuesta',
#             'mode': 'markers',
#             'opacity': 0.9,
#             'marker': {
#                 'color': 'rgba(244, 33, 33, 0.5)',
#                 'size': 6,
#                 'line': {
#                     'width': 0.5, 
#                     'color': 'rgba(255, 255, 255, 0)'
#                 }
#             }
#         }

#         if(len(datos)==0): 
#             datos.insert(0, objeto)
#         else:
#             datos.insert(1, objeto)

#     dict_of_fig = dict({
#                 'data': datos, 
#                 'layout': style_graf_S
#                 })

#     fig = go.Figure(dict_of_fig)

#     fig.update_layout(
#         xaxis_showgrid=True,
#         yaxis_showgrid=True,
#         xaxis_zeroline=True, 
#         yaxis_zeroline=True,
#         xaxis_gridcolor='rgba(63, 63, 63, 0.060)',
#         yaxis_gridcolor='rgba(63, 63, 63, 0.060)',
#         xaxis_zerolinecolor='rgb(63,63,63)',
#         yaxis_zerolinecolor='rgb(63,63,63)',
#         xaxis=dict(
#             linecolor='rgba(0,0,0, 0)',
#             rangeslider=dict(
#             visible=True
#         )

#         ),
#         yaxis=dict(
#             linecolor='rgba(0,0,0, 0)',
#         ),
#     # xaxis=dict(
#     #     rangeslider=dict(
#     #         visible=True
#     #     )
#     # ),
# )
#     fig.update_layout( xaxis_rangeslider_visible='slider' in value )

#     # return {'data': datos, 'layout': style_graf_S}
#     return fig

######### Fin graficar y actualizar Portadoras ***********************************

######### Inicio graficar y actualizar Espectro ***********************************

@callback(
    Output('datatable-upload-graph', 'figure'),
    Input('datatable-upload-container', 'data'),
    Input('datatable-upload-1-container', 'data'),
    Input("check-rangeslider", "value"),
    State('datatable-upload-graph', 'figure'),
)
def display_graph(rowsS, rowsP, value, fig):
    # df_S = pd.DataFrame(rowsS, dtype = 'float64')
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
                'name': 'SIAER',
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
                'name': 'Propuesta',
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


# @callback(
#     Output("datatable-upload-graph", "figure"), 
#     Input("toggle-rangeslider", "value"),
#     State("datatable-upload-graph", "figure"),
#     )
# def display_candlestick(value, fig):
    
#     fig = go.Figure()

#     fig.add_trace(
#         go.Scatter(
#             x=[], 
#             y=[],
#             mode='markers',
#             # marker=dict(borderColor = rgb(63,63,63))
#         )
#     )

#     fig.update_layout(
#         xaxis_rangeslider_visible='slider' in value
#     )

#     return fig

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

        return dcc.send_data_frame(df_P.set_index('#').to_csv, "propuesta_"+str(n)+"_.csv")

@callback(
    Output("download-ocupacion", "data"),
    # Input("btn-I", "n_clicks"),
    # State("btn-R", "disabled"),
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
    #  AcR, AcO,
    # SerPer = ['Móvil']

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
    # prevent_initial_call=True,
    # State("int-can", "value"),
    # State("select_band", "value"),
    # State("seg_bajo", "value"),
    # State("seg_alto", "value"),
    # State("OpCEs_0", "value"),
    # State("OpCEs_1", "value"),
    # State('Servis-dropdown', 'value'),
    State('datatable-upload-container', 'data'),
    State('datatable-upload-1-container', 'data'),
)
def analizar(n, rowS, rowP):
# , can, ban, bajo, alto, OpCEs_0, OpCEs_1, SerPer, rowO):

    if n is None:
        
        return []

    elif (n > 0):

        now = datetime.now()
        format = now.strftime('%d%m%y_%H-%M-%S')

        dfS = pd.DataFrame(rowS)
        dfP = pd.DataFrame(rowP)

        # df = RepoAnalisis()

        df = EstudioDeInvacion(dfS, dfP)


        return dcc.send_data_frame(df.to_excel, "Reporte_"+format+".xlsx", index = False, sheet_name="Reporte de disponibilidad")
        # return dcc.send_file(
        #         excel_stream,
        #         "Reporte_"+format+".xlsx"
                # mimetype = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                # attachment_filename="reporte_test.xlsx",
                # as_attachment=True,
                # cache_timeout=0
                # )
# ********************* Fin Funcional **************************** #
