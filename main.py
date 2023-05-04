from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go

import pandas as pd

df = pd.read_csv(
    'data.csv')

app = Dash(__name__)

app.layout = html.Div([
    dcc.Graph(id='c_graph'),
    dcc.Dropdown(options=df["ISO Country code (2018)"],
                 value='USA', id='selected-country'),
])


@app.callback(
    Output('c_graph', 'figure'),
    Input('selected-country', 'value'))
def update_figure(selected_country):

    df_m = df

    df_m.replace(',', '', regex=True, inplace=True)

    df_m = df_m.astype({'population (2018)': 'float64'})

    mid = df_m.iloc[df_m.index[df_m["ISO Country code (2018)"]
                               == selected_country]]["population (2018)"].values[0]

    df_m["adjusted"] = df_m.apply(
        lambda row: ((mid - row["population (2018)"]) / row["population (2018)"]) * 100, axis=1)

    max = df_m["adjusted"].max()

    min = df_m["adjusted"].min()

    print(df_m['adjusted'])

    fig = go.Figure(go.Choropleth(
        locations=df_m['ISO Country code (2018)'],
        z=df_m["adjusted"],
        zmax=600,
        zmin=-100,
        colorscale='Turbo',
        autocolorscale=False,
        reversescale=True,
        marker_line_color='darkgray',
        colorbar_title='Adjusted Population Difference',
        colorbar=dict(thickness=20, ticklen=3, outlinewidth=0),
        marker_line_width=0.5,
    ))

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
