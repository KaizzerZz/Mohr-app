from dash import Dash, html, dash_table, dcc, callback, Output, Input  
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

def get_line(σx,σy,τ,θ):
    σ_pr = (σx+σy)/2
    r = (((σx-σy)/2)**2 + τ**2)**0.5
    cosb = ((σx-σy)*np.cos(2*θ)/2 + τ*np.sin(2*θ))/r
    sinb = -1*((σx-σy)*np.sin(2*θ)/2 - τ*np.cos(2*θ))/r

    σx1 = σ_pr + r*cosb #D_x
    τx1y1 = r*sinb #D_y

    σx2 = σx1 - 2*(σx1-σ_pr) #D'_x
    τx2y2 = -τx1y1 #D'_y
    x=[σx1,σx2]
    y=[τx1y1,τx2y2]

    return x,y



#There's no incorporation of data here, everything will be gotten from the user's input

#Initialize the app
app = Dash(__name__)
server = app.server

#App layout
app.layout = html.Div([
    html.H1(children='Mohr\'s circle app for principal stresses',style={'textAlign':'center','color':'#7FDBFF'}), #I'll be able to style this
    html.Div(children='Insert the corresponding data'),
    'σx:',
    dcc.Input(id='AxialX', value = 30, type="number",step=1),
    'σy:',
    dcc.Input(id='AxialY', value = 40, type="number",step=1),
    'τ:',
    dcc.Input(id='Shear', value = 20, type="number",step=1),
    'θ',
    dcc.Input(id='Angle', value = 60, type="number",step=1),
    dcc.Graph(id='Mohr',figure=go.Figure(data=[]))
])

@callback(
    Output("Mohr","figure"),
    Input('AxialX','value'),
    Input('AxialY','value'),
    Input('Shear','value'),
    Input('Angle','value')
)
def Generate_circle(σx,σy,τ,angle):
    #Circle
    σ_pr = (σx+σy)/2
    (x_a,y_a) = (σx,τ)
    (x_b,y_b) = (σy,-τ)
    r = (((σx-σy)/2)**2 + τ**2)**0.5
    θ = angle*np.pi/180
    x_l,y_l = get_line(σx,σy,τ,θ)

    dict_of_fig = dict({
    "data": [{'line': {'color': 'black'},
            'x': [-1000, 1000],
            'y': [0, 0],
            'type': 'scatter',
            'name':'Eje x'},
            {'line': {'color': 'black'},
            'x': [0, 0],
            'y': [-1000, 1000],
            'type': 'scatter',
            'name':'Eje y'},
            {'line': {'color': 'blue'},
            'marker': {'size': 10},
            'x': [σ_pr],
            'y': [0],
            'type': 'scatter',
            'name':'Centro'},
            {'line': {'color': '#7fb800'},
            'x': [x_a,x_b],
            'y': [y_a,y_b],
            'text':["A (θ=0°)","B (θ=90°)"],
            'mode':'lines+text',
            'textposition':"bottom center",
            'type': 'scatter',
            'name':'Línea AB'},
            {'line': {'color': '#f6511d'},
            'x': x_l,
            'y': y_l,
            'type': 'scatter',
            'text':[f"D (θ={str(angle)})",f"D' (θ={str(angle+90)})"],
            'mode':"lines+text",
            'textposition':'top center',
            'name':'Línea DD\''}
             ],
    "layout": {"title": {"text": "Círculo de Mohr",
                         'y':0.9,
                         'x':0.46,
                         "xanchor":"center"},
               "xaxis": {'range':[σ_pr-2*r, σ_pr+2*r],'showgrid':False},
               "yaxis": {'range':[-2*r, 2*r]},
               "width": 600,
               "height": 600,
               "xaxis_title":"Axial Stress (σ)",
               "yaxis_title":"Shear Stress (τ)",
               "transition":{
                'duration': 500,
                'easing': 'cubic-in-out'
                            },           
               "shapes":[{'line': {'color': 'LightSeaGreen'},
                    'type':'circle',
                    'x0':σ_pr-r,
                    'x1':σ_pr+r,
                    'xref':'x',
                    'y0':-r,
                    'y1':r,
                    'yref':'y'}]}}
)
    

    fig = go.Figure(dict_of_fig)
    return fig

#Run the app
if __name__ == '__main__':  
    app.run(debug=True)