import polars as pl
from rich import print


def load_info():
    data = pl.scan_csv(
        "data/puzzle_info.csv",
    )
    return data


def load_data():
    data = pl.read_csv(
        "data/puzzles.csv",
    )
    return data


df = load_data()
print(df.head(5))
print(df.shape)
print(len(df["solution_state"][0]))
print(len(df["initial_state"][0]))
