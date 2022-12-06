import pandas as pd
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px


#shapeFile = gpd.read_file('heatMap_location\localidades.zip')
file = pd.read_csv('heatMap_location\locations.csv')
file['location_date'] = pd.to_datetime(file['location_date'])
file['fecha'] = pd.to_datetime(file['location_date']).dt.date
file['hora'] = pd.to_datetime(file['location_date']).dt.time

agrupar = file.groupby(file.phone_id)
phoneIdList = []
for i in agrupar:
    phoneIdList.append(i)


fig = px.density_mapbox(mapbox_style="stamen-terrain",zoom=11,center={'lat':39.51228846680233, 'lon':2.5049221227392557},width=800,height=600)
fig.update_layout(paper_bgcolor= '#8da9c4')


app = Dash(__name__)

app.layout = html.Div(
    children=[
        dbc.Row([
            html.Div([
                html.H1(children='VISOR DE DISPOSITIVOS', id='title')])]),
        dbc.Row([
            html.Div([
                dcc.Graph(id='map', figure=fig )],className='mapa'),
            html.Div([ 
                dcc.Slider(0,23,step=1,
                            marks={0:'00:00\n Horas',6:'06:00',12:'12:00\n Horas',18:'18:00',23:'23:00\n Horas'},
                            dots=True,value=12,
                            id='slider'),
                dcc.Dropdown(file['location_date'].dt.date.unique(),placeholder='Selecciona fecha...',searchable=True, 
                                id='dropdown')],className='rowFechaHora')])
    ]
)


@app.callback(Output('map','figure'),Input('slider','value'),Input('dropdown','value'),prevent_initial_call=True)

def sliderTime(timeValue,dateValue):
    templatesHover = """
    <b>PHONE ID: </b>%{customdata[0]}<br>
    <b>FECHA: </b>%{customdata[1]}<br>
    <b>HORA: </b>%{customdata[2]}"""

    time = file.loc[(file.location_date.dt.hour == timeValue) & (file.location_date.dt.date == pd.to_datetime(dateValue))]
    fig = px.scatter_mapbox(time,lon=time['longitude'],lat=time['latitude'],mapbox_style="stamen-terrain",
                        color=time['phone_id'].astype(str),
                        zoom=11,center={'lat':39.51228846680233, 'lon':2.5049221227392557},
                        size='phone_id',
                        size_max=15,
                        hover_data=[time['phone_id'],time['fecha'],time['hora']])
    fig.update_layout(title='Fecha: ' + str(dateValue)+ '\nHora: ' + str(timeValue) + ':00',legend_title_text='phone_id'.upper(),
                        title_pad_l=150, paper_bgcolor= '#8da9c4')
    fig.update_traces(hovertemplate=templatesHover,hoverinfo="none",hoverlabel=dict(bgcolor='#F7F2F1',font_size=11))

    return fig
    

if __name__ == '__main__':
    app.run_server(debug=True)

    
    
