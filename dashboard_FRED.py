import datetime
import pandas_datareader.data as web
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input

start_year = 2016
start_month = 1
start_day = 1


app = dash.Dash()

app.layout = html.Div(children=[
    html.Div(children='''
        Enter the economic data to graph (try "CPIAUCSL" or "GDP" or fredstlouis tables):
    '''),
    dcc.Input(id='input', value='', type='text'),
    html.Div(id='output-graph')
])

@app.callback(
    Output(component_id='output-graph', component_property='children'),
    [Input(component_id='input', component_property='value')]
)

def update_value(input_data):
    start = datetime.datetime(start_year, start_month, start_day)
    end = datetime.datetime.now()
    df = web.DataReader(input_data, 'fred', start, end)
    print(df.head())

    return dcc.Graph(
        id="output-graph",
        figure={
            'data': [
                {'x': df.index, 'y': df[input_data].astype(str), 'type': 'line', 'name': input_data},
            ],
            'layout': {
                'title': input_data
            }
        }
    )

if __name__ == '__main__':
    app.run_server(debug=True)
