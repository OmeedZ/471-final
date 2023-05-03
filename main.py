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

def create_map(app: Dash, data) -> html.Div:
    return html.Div(
        className="app-div",
        children=[
            html.H1(app.title),
            dcc.Graph(figure=px.choropleth(data, locations="indicator", locationmode="country names",
                                           color="population (2018)", hover_name="indicator",
                                           range_color=[0, 1000], color_continuous_scale="Blues"))
        ]
    )

def create_chart(app: Dash, data) -> html.Div:
    df = px.data.iris()
    fig = px.scatter(df, x="sepal_width", y="sepal_length")
    return html.Div(
        className="app-div1",
        children=[
            html.H1(app.title),
            dcc.Graph(figure=fig)
        ]
    )



def main() -> None:
    data = load_data("data.csv")
    app = Dash(external_stylesheets=[BOOTSTRAP])
    app.title = "471 Final Project"
    app.layout = create_map(app, data=data)
    app.layout = create_chart(app, data=data)
    app.run()





if __name__ == "__main__":
    main()
