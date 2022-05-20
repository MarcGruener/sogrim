import pandas as pd
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split

model = XGBRegressor()
model.load_model("")

data = pd.read_excel("/aggregated.xlsx","Main")

test_train_split = 0.7*len(data)
print(test_train_split)