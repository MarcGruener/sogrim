import pandas as pd

with open('migros_stroes.json', encoding='utf-8') as inputfile:
    df = pd.read_json(inputfile)

#df = df.transpose(copy = True)

df.to_csv('Migros Stores.csv', encoding='utf-8', index=False)