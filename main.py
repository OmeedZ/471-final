from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go

import pandas as pd

# importing data
df = pd.read_csv('data.csv')
df = df.dropna(axis=0, subset=['indicator'])

df.replace(',', '', regex=True, inplace=True)
df.replace('-', '0', regex=True, inplace=True)
df.fillna(0.0, inplace=True)

df = df.astype({'population (2018)': 'Float64',
               'unemployment (%) (2018)': 'Float64',
                'Economic Growth (2018)': 'Float64',
                "GDP ($ USD billions PPP) (2018)": 'Float64',
                "GDP per capita in $ (PPP) (2018)": 'Float64',
                "financial freedom score (2018)": 'Float64',
                "judicial effectiveness score (2018)": 'Float32'
                })

def get_max(determine):
    return ((df[determine].max() -
             df[determine].min()) / df[determine].max()) * 100


app = Dash(__name__)

app.layout = html.Div([
    dcc.Graph(id='c_graph'),
    dcc.Dropdown(options=df["indicator"],
                 value='United States', id='selected-country'),
    dcc.Dropdown(options=["population (2018)",
                          "unemployment (%) (2018)",
                          "GDP ($ USD billions PPP) (2018)",
                          "GDP per capita in $ (PPP) (2018)",
                          "Economic Growth (2018)",
                          "financial freedom score (2018)",
                          "judicial effectiveness score (2018)"
                          ],
                 value='population (2018)', id='selected-metric'),
    dcc.Graph(id='c-line'),
    dcc.Dropdown(['GDP ($ USD billions PPP)', 'GDP per capita in $ (PPP)', 'health expenditure prcnt of GDP',
                'health expenditure per person', 'Military Spending as prcnt of GDP', 'unemployment'],
                'GDP ($ USD billions PPP)', id = 'selected-metric', placeholder = "select a metric"
                )
                
])

#line-graph
@app.callback(
    Output('c-line', 'figure'),
    Input('selected-metric', 'value')
)
def line_graph(selected_metric):
    pass

# chloropleth map
@ app.callback(
    Output('c_graph', 'figure'),
    Input('selected-country', 'value'),
    Input('selected-metric', 'value'))
def update_figure(selected_country, selected_metric):
    df_m = df
    max = get_max(selected_metric)
    min = - max

    mid = df_m.iloc[df_m.index[df_m["indicator"]
                               == selected_country]][selected_metric].values[0]

    df_m["adjusted"] = df_m.apply(
        lambda row: ((row[selected_metric] - mid) / mid) * 100, axis=1)
    fig = go.Figure(go.Choropleth(
        locations=df_m['ISO Country code (2018)'],
        z=df_m["adjusted"],
        zmax=max,
        zmin=min,
        colorscale='Blues',
        autocolorscale=False,
        reversescale=False,
        marker_line_color='darkgray',
        colorbar_title=selected_metric,
        colorbar=dict(thickness=20, ticklen=3, outlinewidth=0),
        marker_line_width=0.5,
        hoverinfo="text",
        hovertext=df_m[[selected_metric, "indicator"]],
    ))
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
