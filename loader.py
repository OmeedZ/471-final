import pandas as pd

class DataSchema:
    INDICATOR = "indicator"
    POPULATION = "population"
    SURFACE_AREA = "surface area (Km2)"
    GINI_INDEX = "GINI index"
    HAPPY_INDEX = "happy planet index"


def load_data(path: str) -> pd.DataFrame:
    data = pd.read_csv(
            path,
            dtype={
                DataSchema.INDICATOR: str,
                DataSchema.POPULATION: float,
                DataSchema.SURFACE_AREA: int,
                DataSchema.GINI_INDEX: float,
                DataSchema.HAPPY_INDEX: float,

            }
    )
    return data
