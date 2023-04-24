import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

app = dash.Dash(__name__)
server = app.server

uniquelaunchsites = spacex_df['Launch Site'].unique().tolist()
lsites = []
lsites.append({'label': 'All Sites', 'value': 'All Sites'})
for site in uniquelaunchsites:
    lsites.append({'label': site, 'value': site})

graph_options = [
    {'label': 'Pie Chart', 'value': 'pie'},
    {'label': 'Scatter Chart', 'value': 'scatter'},
    {'label': 'Bar Chart', 'value': 'bar'}
]

app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36',
                   'font-size': 40}),
    dcc.Dropdown(id='site_dropdown',
                 options=lsites,
                 placeholder='Select a Launch Site here',
                 searchable=True,
                 value='All Sites'),
    html.Br(),
    dcc.Dropdown(id='graph_dropdown',
                 options=graph_options,
                 placeholder='Select a Graph Type',
                 value='pie'),
    html.Br(),
    html.Div(id='graph_container'),
    html.P("Payload range (Kg):"),
    dcc.RangeSlider(
        id='payload_slider',
        min=0,
        max=10000,
        step=1000,
        marks={
            0: '0 kg',
            1000: '1000 kg',
            2000: '2000 kg',
            3000: '3000 kg',
            4000: '4000 kg',
            5000: '5000 kg',
            6000: '6000 kg',
            7000: '7000 kg',
            8000: '8000 kg',
            9000: '9000 kg',
            10000: '10000 kg'
        },
        value=[min_payload, max_payload]
    )
])

@app.callback(
    Output(component_id='graph_container', component_property='children'),
     [Input(component_id='site_dropdown', component_property='value'),
     Input(component_id='graph_dropdown', component_property='value'),
     Input(component_id="payload_slider", component_property="value")]
)
def update_graph(site_dropdown, graph_type, payload_slider):
    if site_dropdown == 'All Sites':
        df = spacex_df[spacex_df['class'] == 1]
    else:
        df = spacex_df.loc[spacex_df['Launch Site'] == site_dropdown]

    filtered_df = df[(df['Payload Mass (kg)'] >= payload_slider[0]) & (df['Payload Mass (kg)'] <= payload_slider[1])]
    if graph_type == 'pie':
        fig = px.pie(filtered_df, values='Payload Mass (kg)', names='Mission Outcome')
    elif graph_type == 'scatter':
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='Launch Site', color='Booster Version Category')
    elif graph_type == 'bar':
        fig = px.bar(filtered_df, x='Launch Site', y='Payload Mass (kg)', color='Booster Version Category')
    return dcc.Graph(figure=fig)

if __name__ == '__main__':
    app.run_server(debug=False)
