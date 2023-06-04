ETIQUETA_1 = "SIAER"
ETIQUETA_2 = "Solicitud"

header_tablas = { 
    'border': '1px solid rgb(63,63,63)', 
    'background-color': 'rgb(14, 16, 18)', 
    'color':'#A0AABA'
}

cell_tablas = { 
    'border': '1px solid rgb(63,63,63)', 
    'background-color': '#161A1D', 
    'color':'#A0AABA'
}

style_graf_init = {
    'plot_bgcolor': '#161A1D',
    'paper_bgcolor': '#161A1D',
    'font': {
        'color': '#A0AABA'
    }, 
}

style_graf = {
    'plot_bgcolor': '#161A1D',
    'paper_bgcolor': '#161A1D',
    'font': {
        'color': '#A0AABA'
    },
}

style_graf_S = {

    'plot_bgcolor': '#161A1D',
    'paper_bgcolor': '#161A1D',
    'font': {
        'color': '#A0AABA'
    },
}

style_graf_P = {

    'plot_bgcolor': '#161A1D',
    'paper_bgcolor': '#161A1D',
    'font': {
        'color': '#A0AABA'
    }
}

style_tabla = { 
    'overflowY': 'auto',
    'height': '390px'
}


style_data_condition = {
    "if": {"state": "selected"},
    "backgroundColor": "rgba(0, 116, 217, 0.3)",
    "border": "1px solid rgba(33,134,244,0.5)",
}

data_table = {
    # 'width': '150px',
    # 'minWidth': '150px',
    # 'maxWidth': '150px',
    # 'overflow': 'hidden',
    # 'textOverflow': 'ellipsis'
}

servis_dropdown = {
    'padding': '0px 5px 0px 15px', 
    'margin': '5px 0px 0px 0px'
}


# Estructuras para análisis por portadoras
opcionesCEs_0 = [
                {"label": "Libre", "value": "L", "disabled": True}, 
                {"label": "Protegido", "value": "P", "disabled": True}, 
                {"label": "S.M.M", "value": "S", "disabled": True},
            ]

opcionesCEs_1 = [
                {"label": "Fronteras", "value": "F", "disabled": True}, 
                {"label": "Determinado", "value": "C", "disabled": True},
                {"label": "Otros", "value": "O", "disabled": True},
            ]

checkAct = {'L': False, 'P': False, 'S': False, 'F': False, 'C': False, 'O': False}

rangosRF_MHz = {'ELF': (3e-6, 3e-5), 'SLF': (3e-5, 0.0003), 'ULF': (0.0003, 0.003), 'VLF': (0.003, 0.03),
                'LF': (0.03, 0.3), 'MF': (0.3, 3), 'HF': (3, 30), 'VHF': (30, 300), 'UHF': (300, 3000), 
                'SHF': (3e+6, 3e+7), 'EHF': (3e+7, 3e+8)}

# Estructuras de conversión en memoria de sesión
TipeGeo = {'tipo':'KML',
            'poligonos': {
                'hayPoli': bool,
                'nPoli': int,
                'data': {
                    'name': [],
                    'geometry': []
                },
            },
            'lineas': { 
                'hayLin': bool,
                'nLin': int,
                'data': {
                    'name': [],
                    'geometry': []
                },
            },
            'puntos': {
                'hayPun': bool,
                'nPun': int,
                'data': {
                    'name': [],
                    'geometry': []
                },
            },
        }

marcadores = ('polygon', 'linestring', 'point')

# Server's de mapas
capaMap = [
            {"value": "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}",
            "label": "USA"},

            {"value": "http://c.tile.stamen.com/watercolor/{z}/{x}/{y}.png",
            "label": "Stamen Acuarela"},

            {"value": "https://stamen-tiles.a.ssl.fastly.net/toner/{z}/{x}/{y}.png",
            "label": "Stamen BW"},

            {"value": "https://stamen-tiles.a.ssl.fastly.net/terrain/{z}/{x}/{y}.jpg",
            "label": "Stamen Terreno"},

            {"value": "https://a.tile.openstreetmap.org/{z}/{x}/{y}.png",
            "label": "OpenStretMap"},

            {"value": "http://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}",
            "label": "Google con Vías"},

            {"value": "http://mt0.google.com/vt/lyrs=r&hl=en&x={x}&y={y}&z={z}",
            "label": "Google Vías Alteradas"},

            {"value": "http://mt0.google.com/vt/lyrs=t&hl=en&x={x}&y={y}&z={z}",
            "label": "Google Terreno"},

            {"value": "http://mt0.google.com/vt/lyrs=p&hl=en&x={x}&y={y}&z={z}",
            "label": "Google Terreno con Vías"},

            {"value": "http://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}",
            "label": "Google Satelital"},

            {"value": "http://mt0.google.com/vt/lyrs=y&hl=en&x={x}&y={y}&z={z}",
            "label": "Google Satelital Hibrido"},

            {"value": "https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga",
            "label": "?"},
        ]
