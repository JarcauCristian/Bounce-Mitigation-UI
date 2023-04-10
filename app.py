from dash import Dash, html, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px


app = Dash(__name__, external_stylesheets=['./style.css'])  
server = app.server

df = pd.read_csv('dates.csv')   

app.layout = html.Div([
    html.Div(className='header', children=[
        html.H1('Questionnaire Response Rate')
    ]),
    html.Div(className='dropdowns', children=[
        html.H2('Year'),
        dcc.Dropdown(value=2020, options=[
            {'label':i, 'value':i} for i in df['year'].unique()
        ], id='dropdown-selection-year'),
        html.H2('Month'),
        dcc.Dropdown(id='dropdown-selection-month', value='January')
    ]),
    dcc.Graph(id='graph-content')
], className='main')    

@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection-year', 'value'),
    Input('dropdown-selection-month', 'value')
)
def update_graph(year, month):
    dff = pd.read_json('data.json', orient='columns')
    dff = dff[dff.percentage < 50]
    return px.bar(dff, x='patientId', y='percentage', title=f'Patients with questionnaire response rate less than 50% in {month},{year}', color='percentage', labels={"patientId": "Patient Identifier", "percentage":"Response rate percentage"})  


@callback(
    Output('dropdown-selection-month', 'options'),
    [Input('dropdown-selection-year', 'value')]
)
def update_month(year):
    months = []
    for i in df['year'].unique():
        if year == i:
            months = df.loc[df['year'] == i, 'month']
    return months

if __name__ == '__main__':
    app.run_server()