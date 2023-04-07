from dash import Dash, html, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px

app = Dash(__name__, external_stylesheets=['./style.css'])

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')

app.layout = html.Div([
    html.Div(className='header', children=[
        html.H1('Bounce Metigation')
    ]),
    html.Div(className='dropdowns', children=[
        html.H2('Year'),
        dcc.Dropdown(df.country.unique(), 'Canada', id='dropdown-selection-year'),

        html.H2('Month'),
        dcc.Dropdown(df.year.unique(), 1952, id='dropdown-selection-month')
    ]),

    dcc.Graph(id='graph-content')
], className='main')

@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection-year', 'value'),
    Input('dropdown-selection-month', 'val')
)
def update_graph(value, val):
    dff = df[df.country==value]
    dff = dff[df.year==val]
    print(dff)
    return px.line(dff, x='year', y='pop')

if __name__ == '__main__':
    app.run_server(debug=True)
