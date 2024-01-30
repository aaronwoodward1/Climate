import pandas as pd
import numpy as np
import dash
from dash import Dash, dcc, html, Input, Output, State, callback
# import dash_core_components as dcc
# import dash_html_components as html
import plotly.graph_objects as go
import plotly.express as px

# from dash.dependencies import Input, Output, callback

data = pd.read_csv(
    "https://raw.githubusercontent.com/aaronwoodward1/Climate/main/FEMA_Flood_Claims_2022%20-%20Financial%20Losses%20by%20State.csv")

# Converting dataset from wide to long format using pandas 'melt' function
data = data.melt(id_vars='State',
             var_name="metric",
             value_name="value")

char_removal = ['$', ',', " "]

for char in char_removal:
    data['value'] = data['value'].str.replace(char, "")

data['value'] = data['value'].str.replace("-", "0")
data['value'] = data['value'].fillna(0)
data['value'] = data['value'].astype(float)
data['State'] = data['State'].str.title()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#Applying State Abbreviations:
#Option 1: create a dictionary, transform into pandas dataframe, then merge to main dataframe
# state_abbr_dict = {'State':['Alabama','Alaska','Arizona','Arkansas','California','Colorado','Connecticut',
#                             'Delaware', 'District of Columbia', 'Florida','Georgia'],
#                    'State_abbr':['AL','AK','AZ','AR','CA','CO','CT','DE','DC','FL','GA', ]}
#Option 2: Merge with State Abbreviation dataset
state_abbr_df = pd.read_csv(
    "https://raw.githubusercontent.com/aaronwoodward1/Climate/main/50%20states%20and%20abbreviations%20-%20Sheet1.csv")


df = pd.merge(data, state_abbr_df, how='left', on='State')
df = df[df['State']!='Grand Total']

# fig.update_geos(fitbounds="locations", visible=False)
# fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
# fig.show()


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
# app = dash.Dash()

app.layout = html.Div([
    html.H1("Flood insurance claims data for 2022", style={"textAlign": "center"}),
    html.Hr(),
    html.P("Choose metric of interest:"),
    dcc.Dropdown(id='metric-type', clearable=False,
                 value="Number of Records",
                 options=[{'label': x, 'value': x} for x in
                          df["metric"].unique()]),
    dcc.Graph(id="map")
])

@app.callback(Output(component_id='map', component_property='figure'),
              [Input(component_id='metric-type', component_property='value')])
def update_map(metric_selected):
    dff = df[metric_selected == df['metric']]

    fig = px.choropleth(locations=dff['Abbreviation'], color=dff['value'], locationmode="USA-states",
                        color_continuous_scale='Blues', scope="usa")

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)

#server.shutdown()


