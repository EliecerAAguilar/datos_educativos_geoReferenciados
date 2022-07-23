from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import psycopg2
import pandas as pd



#Conexion a la base de Datos
connection = psycopg2.connect(
    database = "educacion",
    user = "dashboard",
    password = "BLHVvZwewtQVQ3",
    host = "educationdb.postgres.database.azure.com",
    port = 5432
)

app = Dash(__name__)



app.layout = html.Div(
    html.Div(className='row', children=[
        html.Div([
            html.H1(children='Dashboard Educativo', style={'text-align':'center'}),
            html.H2(children='''Datos Basados en el nodo de Datos Abiertos de la Republica de Panama''', style={'text-align':'center'})
            ]),

        html.Div(children=[
            html.Label('Area'),
            dcc.Dropdown(['URBANA', 'RURAL', 'INDÍGENA'], 'RURAL' , id='area'),
            html.Div(className='spacer'),
            html.Label('Oferta Academica'),
            dcc.Dropdown(['PRIMARIA MULTIGRADO', 'PRIMARIA UNIGRADO', 'PRIMARIA TELEBASICA'], 'PRIMARIA MULTIGRADO', id='oferta' )
        ]),    
            
        
        html.Div(className='parent', children=[
            dcc.Graph(id='grafica-barra', className='plot'),
            html.Div(className='spacer'),
            dcc.Graph(id='MapPlot', className='map')
        ])
    ]))



@app.callback(Output('grafica-barra', 'figure'), Input('area', 'value'), Input('oferta', 'value'))
def update_chart(area , oferta):    
    sql = f"""SELECT status,gender, sum(quantity) FROM school INNER JOIN level ON school.schoolid = level."schoolID" INNER JOIN result r on level."levelID" = r."levelID" WHERE school.area = '{area}' and school.program = '{oferta}' GROUP BY status, gender;"""
    dat = pd.read_sql_query(sql, connection)
    return px.bar(dat, x="status", y="sum", color="gender",  barmode="stack")



@app.callback(Output('MapPlot', 'figure'), Input('area', 'value'), Input('oferta', 'value'))
def update_map(area , oferta):    
    sql = f"""SELECT name, sum(quantity) as matricula,  ST_X(ST_AsEWKT(location)) AS LAT, ST_Y(ST_AsEWKT(location)) AS LONG FROM school INNER JOIN level ON school.schoolid = level."schoolID" INNER JOIN result r on level."levelID" = r."levelID" WHERE school.area = '{area}' and school.program = '{oferta}' GROUP BY status, name, LONG, LAT;"""
    dat = pd.read_sql_query(sql, connection)
    fig = px.scatter_mapbox(dat, lat="lat", lon="long", hover_name="name", hover_data=["name", "matricula"], color_discrete_sequence=["blue"], zoom=7, height=700)
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig



if __name__ == '__main__':
    app.run_server(debug=True)

