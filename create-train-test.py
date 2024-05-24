
import pandas as pd
from sklearn.model_selection import train_test_split

raw_df = pd.read_csv('raw_features.csv')
raw_df.sort_values(by = 'id', inplace = True)

X = raw_df['id'].values
y = raw_df['grade'].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 2016, stratify = y)

test_indicator = [id in X_test for id in X]

print(test_indicator)

