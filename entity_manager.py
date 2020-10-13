import numpy as np 
import pandas as pd

# Read file
path = "./Entities/"
name = "entity_name"
filename = name + ".csv"
df = pd.read_csv(path + filename, encoding='utf8')

# Transformations
df["DATA"] =  pd.to_datetime(df["DATA"], format="%Y-%m-%d")
# df.drop(columns=["ENTIDADE"], inplace=True)

# Select max value in month interval
period = df.DATA.dt.to_period("M")
tidy = df.groupby(period).mean()
tidy.index = tidy.index.rename("DATE")
# tidy.drop(columns="DATA", inplace=True)
df = tidy

# Remove null columns
aux = pd.DataFrame(df.isnull().sum() / df.shape[0], columns=["NULL_COUNT"])
threshold = 1
features = aux[aux["NULL_COUNT"] < threshold].index.tolist()
filtered = df[features]
filtered["ENTIDADE"] = name.upper()

# Define data threshold
threshold = 60
percentage = (1 - filtered.isnull().sum() / filtered.shape[0]) * 100
percentage = pd.Series(np.around(percentage.values, 2), index=percentage.index)

# Filter data and export as csv
filtered = filtered[sorted(filtered.columns)]
path = "./Tidy_Entities/"
filtered.to_csv(path + filename, encoding='utf8')

# Print removed data
print(
    f"\033[31mLinhas: {df.shape[0]}\n"
    f"Colunas: {df.shape[1]}\n\n"
    f"\033[32m-> Features: \n{df.columns.tolist()}\n\n"
    f"\033[34m-> Valores ÚNICOS: \n{df.nunique()}\n\n"
    f"\033[36m-> Valores FALTANTES: \n{df.isnull().sum()}\033[0"
)