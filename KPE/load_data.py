import pandas as pd
from os import listdir 
from os.path import isfile, join 

path = "../Get Data/Data/all_news"

def get_df():

    df = pd.DataFrame()
    
    for f in listdir(path):
        # reading the file in dataframe
        try:
            temp_df = pd.read_csv(f"{path}/{f}",encoding="utf8")
        except UnicodeDecodeError:
            temp_df = pd.read_csv(f"{path}/{f}",encoding="'windows-1252")
        
        # adding a single file dataframe to the main dataframe
        df = pd.concat([df,temp_df],axis=0)

    return df 