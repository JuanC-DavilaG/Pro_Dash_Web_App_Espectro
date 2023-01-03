import dash
from dash.dependencies import Input, Output, State
from dash import Dash, html, dcc, callback

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>Hola</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        <div>My Custom header</div>
        <div>Hola Mundo</div>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
        <div>My Custom footer</div>

        <button onclick="saludar()">Click</button>

        <div>Click</div>
        <div>Aquí</div>
    </body>
    <script> 

        function saludar(){
            console.log('Hola')
        }

        function 

    </script>
</html>
'''

app.layout = html.Div([
    html.H1('Titulo'),

    html.Div(id='blank-output'),
    html.Div(id='blank-output_0'),
    dcc.Tabs(id='tabs-example', value='tab-1', children=[
        dcc.Tab(label='Tab one', value='tab-1'),
        dcc.Tab(label='Tab two', value='tab-2'),
    ]),

    html.Button(id="boton_saludar", name='click', children='click'),
    html.Div(id='div_din')
])

app.clientside_callback(
    """
    function(tab_value) {
        if (tab_value === 'tab-1') {
            document.title = 'En Tab 1'
        } else if (tab_value === 'tab-2') {
            document.title = 'En Tab 2'
        }
    }
    """,
    Output('blank-output', 'children'),
    Input('tabs-example', 'value')
)

app.clientside_callback(
    """
    function(tab_value) {
        console.log(tab_value)
    }
    """,
    Output('blank-output_0', 'children'),
    Input('boton_saludar', 'n_clicks')
)

@callback(
    Output('div_din', 'children'),
    Input('boton_saludar', 'n_clicks'),
    State('div_din', 'children'),
)
def update_output(valor, chil):
    
    if chil != None:

        print(valor)
        return valor

    return ''

if __name__ == '__main__':
    app.run_server(debug=True)