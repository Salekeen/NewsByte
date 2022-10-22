import pandas as pd
from pathlib import Path
from datetime import datetime


path = Path("./Scraper/Data/all_news")


def get_last_7_days_data():

    df = pd.DataFrame()

    for f in path.iterdir():

        year, month, day = f.stem.split('_')[2:5]
        date = datetime(int(year), int(month), int(day))
        now = datetime.now()

        if abs((date - now).days) <= 8:

            print(date.day, now.day)
            print(abs((date - now).days))
            try:
                temp_df = pd.read_csv(f, encoding="utf8")
            except UnicodeDecodeError:
                temp_df = pd.read_csv(f, encoding="'windows-1252")

            temp_df['date_published'] = date

            # adding a single file dataframe to the main dataframe
            df = pd.concat([df, temp_df], axis=0)

    return df
