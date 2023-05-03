import pandas as pd
from dash import Dash, html, dcc, dash_table
from dash_bootstrap_components.themes import BOOTSTRAP
import plotly
import plotly.express as px

def load_data(path: str) -> pd.DataFrame:
    data = pd.read_csv(
            path
    )
    return data

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

def main() -> None:
    data = load_data("data.csv")
    app = Dash(external_stylesheets=[BOOTSTRAP])
    app.title = "471 Final Project"
    app.layout = create_layout(app, data=data)
    app.run()





if __name__ == "__main__":
    main()
