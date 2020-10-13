import numpy as np 
import pandas as pd 
from os import listdir
from shutil import copy2 
import regex as re 

# Define path
path = "./Normalized/"
matches = listdir(path)

# Merge datasets
df = pd.DataFrame()
for i in range(0, len(matches) - 1):
    df_1 = pd.read_csv(path + matches[i], encoding='utf8')
    df_2 = pd.read_csv(path + matches[i + 1], encoding='utf8')
    partial = df_1.append(df_2)
    df = df.append(partial)

# Merge columns with the same name
df["CIANETO"] = [x[0] if str(x[0]) != "nan" else x[1] for x in zip(df["CIANETO"], df["CIANETO.1"])]
df["MERCÚRIO"] = [x[0] if str(x[0]) != "nan" else x[1] for x in zip(df["MERCÚRIO"], df["MERCÚRIO.1"])]
df["FENOL"] = [x[0] if str(x[0]) != "nan" else x[1] for x in zip(df["FENOL"], df["FENÓIS"])]
df["SÓLIDOS"] = [x[0] if str(x[0]) != "nan" else x[1] for x in zip(df["SÓLIDOS"], df["SÓLIDOS_VOLÁTEIS"])]

# Drop duplicates
df.drop(columns=["CIANETO.1", "MERCÚRIO.1", "FENÓIS", "SÓLIDOS_VOLÁTEIS"], inplace=True)
tidy = df.drop_duplicates()

# Change column names
tidy.ENTIDADE = tidy.ENTIDADE.map(lambda x: x.replace(".1", ""))
tidy.ENTIDADE = tidy.ENTIDADE.map(lambda x: x.replace(".1", ""))
tidy.ENTIDADE = tidy.ENTIDADE.map(lambda x: x.replace("ANAMB", "ANAMBI"))
tidy.ENTIDADE = tidy.ENTIDADE.map(lambda x: x.replace("ANAMBII", "ANAMBI"))
tidy.ENTIDADE = tidy.ENTIDADE.map(lambda x: x.replace("LAB. ANÁLISE AMBIENTAL", "ANAMBI"))
tidy.ENTIDADE = tidy.ENTIDADE.map(lambda x: x.replace("SANEAMB", "ANAMBI"))
tidy.ENTIDADE = tidy.ENTIDADE.map(lambda x: x.replace("itt Fossil", "ITT FOSSIL"))
tidy.ENTIDADE = tidy.ENTIDADE.map(lambda x: x.replace("itt Fossil / NUCMAT*", "ITT FOSSIL"))
tidy.ENTIDADE = tidy.ENTIDADE.map(lambda x: x.replace("ITT FOSSIL / NUCMAT*", "ITT FOSSIL"))
tidy.ENTIDADE = tidy.ENTIDADE.map(lambda x: x.replace("Lab. Quimica e Farmácia", "LAB. QUIMICA"))
tidy.ENTIDADE = tidy.ENTIDADE.map(lambda x: re.sub(r"\s+", " ", x))

# Separate dataset into entity subsets and export each one to Entities
entities = tidy.ENTIDADE.unique().tolist()
tables = [tidy[tidy["ENTIDADE"] == entity] for entity in entities]

for table in tables:
    name = table.ENTIDADE.unique()[0].replace(" ", "_").lower()
    name = name.replace("/", "")
    name = name.replace(".", "")
    path = "./Entities/"
    table.to_csv(f"{path}{name}.csv", encoding="utf8", header=True, index=False)