from sklearn import datasets
boston = datasets.load_boston()

import pandas as pd
df = pd.DataFrame(boston['data'],columns=boston['feature_names'])

import sqlite3
connect = sqlite3.connect('../db.sqlite3')
df.to_sql('boston_table', connect, if_exists='append')

connect.close()

