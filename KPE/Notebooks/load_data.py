import pandas as pd
from pathlib import Path


path = Path("../../Scraper/Data/all_news")


def get_df():

    df = pd.DataFrame()

    for f in path.iterdir():
        # reading the file in dataframe
        try:
            temp_df = pd.read_csv(f, encoding="utf8")
        except UnicodeDecodeError:
            temp_df = pd.read_csv(f, encoding="'windows-1252")

        # adding a single file dataframe to the main dataframe
        df = pd.concat([df, temp_df], axis=0)

    return df
