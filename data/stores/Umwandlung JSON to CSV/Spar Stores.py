import pandas as pd

with open('spar_stores.json', encoding='utf-8') as inputfile:
    df = pd.read_json(inputfile)

#df = df.transpose(copy = True)

df.to_csv('Spar Stores.csv', encoding='utf-8', index=False)