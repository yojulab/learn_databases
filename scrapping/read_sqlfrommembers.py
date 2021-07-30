import sqlite3
connect = sqlite3.connect('../db.sqlite3')

import pandas as pd
df = pd.read_sql_query('select * from members where age >= 30', connect)

connect.close()
