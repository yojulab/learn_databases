from sklearn import datasets
data = datasets.load_iris()

import pandas as pd
df = pd.DataFrame(data['data'],columns=data['feature_names'])

import sqlite3
connect = sqlite3.connect('../db.sqlite3')
df.to_sql('iris_table', connect, if_exists='append')

connect.close()
