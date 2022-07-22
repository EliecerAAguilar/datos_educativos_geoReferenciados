from dash import dcc, html, dash_table, Dash, dash_table
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc

# df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2011_february_us_airport_traffic.csv')
df = pd.read_csv('pma_shp/final.csv', low_memory=False)

# Subset dataframe to show some specific columns in dash web app
df1 = df[['PROVINCIA','CORREGIMIENTO', 'LAT', 'LONG']]

# Find Lat Long center
lat_center = sum(df['LAT']) / len(df['LAT'])
long_center = sum(df['LONG']) / len(df['LONG'])

# Find Lat Long center
# lat_center = sum(df['lat']) / len(df['lat'])
# long_center = sum(df['long']) / len(df['long'])

app = Dash(external_stylesheets=["https://codepen.io/chriddyp/pen/bWLwgP.css"])

# app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = 'Mapa Edu'

layout_map = dict(
    autosize=True,
    height=500,
    weidth=100,
    font=dict(color="#191A1A"),
    titlefont=dict(color="#191A1A", size='14'),
    margin=dict(l=0,r=0,b=0,t=0),
    hovermode="closest",
    plot_bgcolor='#fffcfc',
    paper_bgcolor='#fffcfc',
    legend=dict(font=dict(size=10), orientation='h'),
    mapbox=dict(
        style="open-street-map",
        center=dict(
            lon=long_center,
            lat=lat_center
        ),
        zoom=6,
    )
)

app.layout = html.Div(
    html.Div([
        html.Div([
            html.H1(children='Dash open street map'),
            html.Div(id='mdiv'),
            ],
            className='row'
        ),

        html.Br(),
        html.Br(),
        html.Div([
            html.Div([
                dash_table.DataTable(
                    id='table',
                    columns=[{"name": i, "id": i} for i in df1.columns],
                    data=df1.loc[:9, ].to_dict('records'),
                ),
                    ], className='six columns'),
            html.Br(),
            html.Div([
                dcc.Graph(
                    id='MapPlot',
                    figure={
                        "data": [{
                            "type": "scattermapbox",
                            "lat": list(df.LAT),
                            "lon": list(df.LONG),
                            "hoverinfo": "text",
                            "hovertext": [["Lat: {}Long: {} Count: {} ".format(i, j, k)]for i, j, k in zip(df['LAT'], df['LONG'], df['CORREGIMIENTO'])],
                            "mode": "markers",
                            "name": list(df['PROVINCIA']),
                            "marker": {"size": 15, "opacity": 0.7, "color": '#F70F0F'}
                        }],
                        "layout": layout_map}
                ), ],
        className = 'six columns')],
    className = 'row')
    ])
)

if __name__ == '__main__':
    app.run_server(debug=True)

