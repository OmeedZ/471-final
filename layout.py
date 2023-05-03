from dash import Dash, html, dash_table, dcc
import plotly.express as px


def create_layout(app: Dash, data) -> html.Div:
    return html.Div(
        className="app-div",
        children=[
            html.H1(app.title),
            # dcc.Graph(figure=px.scatter(
            #     data, x='indicator', y='human development index (2021)')),
            dcc.Graph(figure=px.choropleth(data, locations="indicator", locationmode="country names",
                                           color="population (2018)", hover_name="indicator",
                                           range_color=[0, 1000], color_continuous_scale="Blues"))
        ]
    )
