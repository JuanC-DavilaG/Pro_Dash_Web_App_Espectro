import dash
from dash import html, dcc, Input, Output, callback

dash.register_page(__name__, path='/tablas')

layout = html.Div(children=[
    html.H1(children='Esta es nuestra pagina de Tablas', id='titulo_tablas'),

    html.Div(children='''
        Este es el contenido de la pagina de Tablas.
    ''', id='contenido_tablas'),

])


# import dash
# from dash import html, dcc, Input, Output, ctx, callback

# dash.register_page(__name__, path='/tablas')

# layout = html.Div([
#     dcc.Dropdown([
#             {
#                 "label": html.Div(
#                     [
#                         html.Img(src="https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/Python.svg/1200px-Python.svg.png", height=20),
#                         html.Div("Python", style={'font-size': 15, 'padding-left': 10}),
#                     ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}
#                 ),
#                 "value": "Python",
#             },
#             {
#                 "label": html.Div(
#                     [
#                         html.Img(src="https://upload.wikimedia.org/wikipedia/commons/thumb/1/1f/Julia_Programming_Language_Logo.svg/1200px-Julia_Programming_Language_Logo.svg.png", height=20),
#                         html.Div("Julia", style={'font-size': 15, 'padding-left': 10}),
#                     ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}
#                 ),
#                 "value": "Julia",
#             },
#             {
#                 "label": html.Div(
#                     [
#                         html.Img(src="https://stat.ethz.ch/R-manual/R-devel/doc/html/Rlogo.svg", height=20),
#                         html.Div("R", style={'font-size': 15, 'padding-left': 10}),
#                     ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}
#                 ),
#                 "value": "R",
#             },
#         ]
#     ),
#     html.Div([
#     html.Button('Button 1', id='btn-1-ctx-example'),
#     html.Button('Button 2', id='btn-2-ctx-example'),
#     html.Button('Button 3', id='btn-3-ctx-example'),
#     html.Div(id='container-ctx-example')
# ])
# ])

# # layout = html.Div([
# #     html.Button('Button 1', id='btn-1-ctx-example'),
# #     html.Button('Button 2', id='btn-2-ctx-example'),
# #     html.Button('Button 3', id='btn-3-ctx-example'),
# #     html.Div(id='container-ctx-example')
# # ])


# @callback(Output('container-ctx-example','children'),
#               Input('btn-1-ctx-example', 'n_clicks'),
#               Input('btn-2-ctx-example', 'n_clicks'),
#               Input('btn-3-ctx-example', 'n_clicks'))
# def display(btn1, btn2, btn3):
#     button_clicked = ctx.triggered_id
#     return html.Div([
#         dcc.Markdown(
#             f'''You last clicked button with ID {button_clicked}
#             ''' if button_clicked else '''You haven't clicked any button yet''')
#     ], style={'color':'white'})





# from dash import Dash, html, dcc, Input, Output, dash_table, callback  # pip install dash
# import dash
# import dash_bootstrap_components as dbc
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt             # pip install matplotlib
# import mpld3                                # pip install mpld3


# df = pd.read_csv("https://raw.githubusercontent.com/Coding-with-Adam/Dash-by-Plotly/master/Bootstrap/Berlin_crimes.csv")
# # print(df.head())

# dash.register_page(__name__, path='/tablas')

# layout = dbc.Container([
#     html.H1("Interactive Matplotlib with Dash", className='mb-2', style={'textAlign':'center'}),

#     dbc.Row([
#         dbc.Col([
#             html.Iframe(
#                 id='scatter-plot',
#                 srcDoc=None,  # here is where we will put the graph we make
#                 style={'border-width': '5', 'width': '100%',
#                        'height': '10000px'}),


#         ]),
#     ]),

# ])

# # Create interactivity between components and graph
# @callback(
#     Output('scatter-plot', 'srcDoc'),
#     Input()
# )
# def plot_data():

#     # filter data based on user selection
#     # dff = df[df.Year == selected_year]
#     # dff = dff[dff.District == selected_district]



#     # build CNAF plot
    
#     # %matplotlib inline

#     # reference: https://mentalitch.com/key-events-in-rock-and-roll-history/
#     dates = [29.7, 30.005, 30.01, 37.5, 38.25, 39]

#     # min_date = date(np.min(dates).year - 2, np.min(dates).month, np.min(dates).day)
#     # max_date = date(np.max(dates).year + 2, np.max(dates).month, np.max(dates).day)

#     min_date = (np.min(dates))
#     max_date = (np.max(dates))
        
#     labels = ['Fijo - Movil', 'Radiodifusión', 'Investigación Espacial', 'Operaciones espaciales \n(Identificación de Satélites)',
#             'Radioastronomía', 'Radiolocalización']

#     # labels with associated dates
#     labels = ['{0}\n{1}'.format(d, l) for l, d in zip (labels, dates)]

#     # print(labels)

#     # ####################################################################### #

#     fig, ax = plt.subplots(figsize=(10, 30), constrained_layout=True) #width and height graph
#     _ = ax.set_xlim(-100, 100) # Limits in axis X
#     # _ = ax.set_ylim(min_date-3, max_date+3)
#     _ = ax.set_ylim(max_date+3, min_date-3)
#     _ = ax.axvline(-0.93, ymin=0.05, ymax=0.95, c='#5c9132', zorder=0) # Line Vertical
#     # -3.93
#     _ = ax.scatter(np.zeros(len(dates)), dates, s=120, c='#c8c8c890', zorder=1)# Border circul
#     _ = ax.scatter(np.zeros(len(dates)), dates, s=30, c='#5d913290', zorder=3)# Center circul

#     label_offsets = np.repeat(2.0, len(dates))
#     label_offsets[1::2] = -2.0

#     # ###################################################################### #

#     # # Background

#     # plt.style.use('seaborn-dark')

#     for param in ['figure.facecolor', 'axes.facecolor', 'savefig.facecolor']:
#         plt.rcParams[param] = '#161A1D'  # bluish dark grey
#     for param in ['text.color', 'axes.labelcolor', 'xtick.color', 'ytick.color']:
#         plt.rcParams[param] = '0.9'  # very light grey
#     ax.grid(color='#2A3459')  # bluish dark grey, but slightly lighter than background

#     # ####################################################################### #

#     j=len(dates)-1

#     for i, (l, d) in enumerate(zip(labels, dates)):
#         d = d
#     #     - timedelta(days=90)
#         align = 'right'
#         if i % 2 == 0:
#             align = 'left'
#         _ = ax.text(label_offsets[i], d, l, ha=align, fontfamily='serif', fontweight='bold', color='#A0AABA',fontsize=20) # Lables

#     stems = np.repeat(2.0, len(dates))
#     stems[1::2] *= -1.0   
#     x = ax.hlines(dates, 0, stems, color='#5c9132') #Line horizon

#     # hide lines around chart
#     for spine in ["left", "top", "right", "bottom"]:
#         _ = ax.spines[spine].set_visible(False)
    
#     # hide tick labels
#     _ = ax.set_xticks([])
#     _ = ax.set_yticks([])
    
#     _ = ax.set_title('Cuadro Nacional de Atribución de Frecuencias', fontweight="bold", fontfamily='serif', fontsize=40, 
#                     color='#A0AABA') # Title

#     # fig, ax = plt.subplots()
#     # ax.scatter(x=dff.Damage, y=dff.Graffiti, s=dff.Drugs)
#     # ax.set_xlabel("Damage")
#     # ax.set_ylabel("Graffiti")
#     # ax.grid(color='lightgray', alpha=0.7)
#     html_CNAF = mpld3.fig_to_html(fig)


#     return html_CNAF