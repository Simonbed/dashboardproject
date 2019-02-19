import dash
import dash_core_components as dcc
import dash_html_components as html

import pandas as pd
import sqlite3
import pandas.io.sql as pdsql

from dash.dependencies import Input, Output


conn = sqlite3.connect("econometrics_trial.sqlite")
sql = """
SELECT *
FROM Economics
"""


## With sql data into the pandas df, it makes it easy to plot the data
df = pdsql.read_sql(sql, conn)

print(df.columns)
dates = [df["DATE_LIST"].values.tolist()]
values = [df["CPIUSRTE"].astype(str)]


app = dash.Dash(__name__)
## Here we will add the input
app.layout = html.Div(children=[
    html.Div(children='''
        Enter the row to graph (ex : CPIUSRTE):
    '''),
    dcc.Input(id='input', value='', type='text'),
    html.Div(id='output-graph')
])

@app.callback(
    Output(component_id='output-graph', component_property='children'),
    [Input(component_id='input', component_property='value')]
)

def update_value(input_data):

    header_str = "Econ Data " + str(input_data)

    html.H1(header_str),
    return dcc.Graph(
        id='output-graph',
        figure = {
            'data': [
                {'x': df.index, 'y': df[input_data].astype(str), 'type':'line', 'name':'US Consumer Price Index'}],
            'layout' : {'title': df[input_data].astype(str)
                }
            })

if __name__ == "__main__":
    app.run_server(debug=True)

### This actually works for now. Ill work on it more another time
