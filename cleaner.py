import numpy as np 
import pandas as pd 
from os import listdir
from shutil import copy2 

# Define path
path = "./Dataset/"
word = "word"
archives = listdir(path) 
matches = [value for value in archives if word in value]
matches = sorted(matches)

# Merge both dataframes
df = pd.DataFrame()
for i in range(0, len(matches) - 1):
    df_1 = pd.read_csv(path + matches[i], encoding='utf8')
    df_2 = pd.read_csv(path + matches[i + 1], encoding='utf8')
    partial = df_1.append(df_2)
    df = df.append(partial)

# Generate csv for outcome
df.to_csv(f"./Merged/{word}.csv", encoding='utf8', index=False)

# Generate log
copy2("cleaner.ipynb", f"./Logs/{word}.ipynb")

