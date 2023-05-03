import pandas as pd


class DataSchema:
    INDICATOR = "indicator"
    POPULATION = "population"
    SURFACE_AREA = "surface area (Km2)"
    GINI_INDEX = "GINI index"
    HAPPY_INDEX = "happy planet index"


def load_data(path: str) -> pd.DataFrame:
    data = pd.read_csv(
        path
    )
    return data
