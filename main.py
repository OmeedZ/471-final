import pandas as pd
from dash import Dash, html
from dash_bootstrap_components.themes import BOOTSTRAP
import plotly
from layout import create_layout
from loader import load_data

def main() -> None:
    data = load_data("data.csv")
    app = Dash(external_stylesheets=[BOOTSTRAP])
    app.title = "471 Final Project"
    app.layout = create_layout(app)
    app.run()





if __name__ == "__main__":
    main()




