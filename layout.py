from dash import Dash, html, dash_table, dcc
import plotly.express as px


def create_layout(app: Dash, data) -> html.Div:
    return html.Div(
        className="app-div",
        children=[
            html.H1(app.title),
            dash_table.DataTable(data=data.to_dict('records'), page_size=10),
            dcc.Graph(figure=px.scatter(
                data, x='indicator', y='human development index (2021)'))
        ]
    )
