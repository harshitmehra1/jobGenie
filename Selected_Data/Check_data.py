import pandas as pd

df = pd.read_csv("./Selected_Data/under_100mb.csv")


print("Columns:", df.columns.tolist())
print(df.head(5))
