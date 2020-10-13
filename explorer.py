import numpy as np 
import pandas as pd 
from os import listdir
from shutil import copy2 

# Define path
path = "./Tidy/"
archives = sorted(listdir(path))

# Define columns (optional)
name = archives[17].split(".")[0]
df = pd.read_csv(path + name + ".csv", encoding='utf8')
# df.rename(columns={"PARÂMETROS": "ENTIDADE"}, inplace=True)
# df.ENTIDADE = df.ENTIDADE.map(lambda x: x.replace("P2/P6", "P2"))
columns = df.columns
new_columns = [x.split()[0] for x in columns] 
df.columns = new_columns
df.drop(columns=["OBSERVAÇÕES", "ANAL."], inplace=True)
# df.rename(columns={"PORCENTAGEM": "PORCENTAGEM_SÓLIDOS", "SÓLIDOS": "SÓLIDOS_VOLÁTEIS"}, inplace=True)
# df.rename(columns={"Parâmetros": "ENTIDADE"}, inplace=True)
# df.columns = [x.upper() for x in new_columns]
# df["ENTIDADE"] = name

# Apply transformations
transposed = df.T
transposed = transposed.reset_index()
transposed.columns = transposed.values[0]
transposed.rename(columns={"DATA": "ENTIDADE"}, inplace=True)
transposed.drop(axis=0, index=[0], inplace=True)
transposed = transposed.melt(id_vars=['ENTIDADE'])
transposed.rename(columns={"variable": "DATA", "value": name}, inplace=True)
df = transposed

# Export normalized data
df.to_csv(f"./Normalized/{name}.csv", encoding='utf8', index=False)

# Generate logs
copy2("explorer.ipynb", f"./Normlogs/{name}.ipynb")