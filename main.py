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
               'unemployment prcnt (2018)': 'Float64',
                'Economic Growth (2018)': 'Float64',
                "GDP ($ USD billions PPP) (2018)": 'Float64',
                "GDP per capita in $ (PPP) (2018)": 'Float64',
                "financial freedom score (2018)": 'Float64',
                "judicial effectiveness score (2018)": 'Float32',
                "indicator": "str",
                'GDP ($ USD billions PPP) (2019)': "Float64"
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
                          "unemployment prcnt (2018)",
                          "GDP ($ USD billions PPP) (2018)",
                          "GDP per capita in $ (PPP) (2018)",
                          "Economic Growth (2018)",
                          "financial freedom score (2018)",
                          "judicial effectiveness score (2018)"
                          ],
                 value='population (2018)', id='selected-metric'),
    dcc.Graph(id='c-line'),
    dcc.Dropdown(options=["GDP (USD Billions)",
                          "GDP per capita in USD",
                          "Health Expenditure percentage of GDP",
                          "Health Expenditure per person",
                          "Military Spending as percentage of GDP",
                          "unemployment"
                          ],
                 value='GDP (USD Billions)', id='new_metric'),
])

#line-graph
@app.callback(
    Output('c-line', 'figure'),
    Input('new_metric', 'val')
 )
def line_graph(new_metric):
    #sclicing dataframe
    df_gdp=df[['GDP ($ USD billions PPP) (2018)', 'GDP ($ USD billions PPP) (2019)', 'GDP ($ USD billions PPP) (2020)',
            'GDP ($ USD billions PPP) (2021)']]
    df_gdp2=df[['GDP per capita in $ (PPP) (2018)', 'GDP per capita in $ (PPP) (2019)','GDP per capita in $ (PPP) (2020)',
                'GDP per capita in $ (PPP) (2021)']]
    df_health=df[['health expenditure prcnt of GDP (2014)','health expenditure prcnt of GDP (2015)',
                  'health expenditure prcnt of GDP (2016)','health expenditure prcnt of GDP (2017)',
                  'health expenditure prcnt of GDP (2018)','health expenditure prcnt of GDP (2019)',
                  'health expenditure prcnt of GDP (2020)','health expenditure prcnt of GDP (2021)',
                  'health expenditure prcnt of GDP (Latest)']]
    df_health2 = df[["health expenditure per person (2015)",'health expenditure per person (2018)',
                  'health expenditure per person (2019)']]
    df_military=df[['Military Spending as prcnt of GDP (2019)','Military Spending as prcnt of GDP (2021)']]
    df_unemployment=df[['unemployment prcnt (2018)','unemployment prcnt (2021)']]
    
    #melting dataframe
    df_gdp=df_gdp.melt(id_vars="indicator", var_name="metric", value_name="Value")
    df_gdp2=df_gdp2.melt(id_vars="indicator", var_name="metric", value_name="Value")
    df_health=df_health.melt(id_vars="indicator", var_name="metric", value_name="Value")
    df_health2=df_health2.melt(id_vars="indicator", var_name="metric", value_name="Value")
    df_military=df_military.melt(id_vars="indicator", var_name="metric", value_name="Value")
    df_unemployment=df_unemployment.melt(id_vars="indicator", var_name="metric", value_name="Value")

    #converting column to int
    df_gdp['metric'] = df_gdp['metric'].astype('str').str.extractall('(\d+)').unstack().fillna('').sum(axis=1).astype(int)
    df_gdp2['metric'] = df_gdp2['metric'].astype('str').str.extractall('(\d+)').unstack().fillna('').sum(axis=1).astype(int)
    df_health['metric'] = df_health['metric'].astype('str').str.extractall('(\d+)').unstack().fillna('').sum(axis=1).astype(int)
    df_health2['metric'] = df_health2['metric'].astype('str').str.extractall('(\d+)').unstack().fillna('').sum(axis=1).astype(int)
    df_military['metric'] = df_military['metric'].astype('str').str.extractall('(\d+)').unstack().fillna('').sum(axis=1).astype(int)
    df_unemployment['metric'] = df_unemployment['metric'].astype('str').str.extractall('(\d+)').unstack().fillna('').sum(axis=1).astype(int)
    #converting vals to float
    df_gdp['Value'] = df_gdp['Value'].astype(float)
    df_gdp2['Value'] = df_gdp2['Value'].astype(float)
    df_health['Value'] = df_health['Value'].astype(float)
    df_health2['Value'] = df_health2['Value'].astype(float)
    df_military['Value'] = df_military['Value'].astype(float)
    df_unemployment['Value'] = df_unemployment['Value'].astype(float)

    if new_metric == 'GDP (USD Billions)':
        fig = px.line(df_gdp,x="metric",y="Value",color='indicator')
    elif new_metric == 'GDP per capita in USD':
        fig = px.line(df_gdp2,x="metric",y="Value",color='indicator')
    elif new_metric == 'Health Expenditure percentage of GDP':
        fig = px.line(df_health,x="metric",y="Value",color='indicator')
    elif new_metric == 'Health Expenditure per person':
        fig = px.line(df_health2,x="metric",y="Value",color='indicator')
    elif new_metric == 'Military Spending as percentage of GDP':
        fig = px.line(df_military,x="metric",y="Value",color='indicator')
    elif new_metric == 'unemployment':
        fig = px.line(df_unemployment,x="metric",y="Value",color='indicator')
    else:
        fig = px.line(df_gdp,x="metric",y="Value",color='indicator')
    
    return fig

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
