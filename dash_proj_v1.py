import dash
import dash_core_components as dcc
import dash_html_components as html


app = dash.Dash()
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Dash Tries',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    html.Div(children='Trying to make a dash from various data sources', style={
        'textAlign': 'center',
        'color': colors['text']
    }),
    dcc.Graph(
        id='Graph1',
        figure={
            'data': [
                {'x': ADD SOME DATA HERE, 'y': AND SOME DATA HERE, 'type': 'bar', 'name': 'Name of the data'},
 
            ],
            'layout': {
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']
                }
            }
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
