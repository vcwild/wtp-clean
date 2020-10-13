import numpy as np 
import pandas as pd 
from os import listdir
from shutil import copy2 

# Set path
path = "./Merged/"
archives = listdir(path)

# Replace characters
for i in range(0, len(archives)):
    df = pd.read_csv(f"{path}{archives[i]}", encoding="utf8")
    columns = df.columns

    for column in columns:
        df[str(column)] = df[str(column)].map(lambda x: str(x).replace(",", "."))
        df[str(column)] = df[str(column)].map(lambda x: str(x).replace("<", ""))
        df[str(column)] = df[str(column)].map(lambda x: str(x).strip())

        title = str(archives[i]).split(".")[0]
        df.to_csv(f"./Tidy/{title}.csv", encoding='utf8', index=False)