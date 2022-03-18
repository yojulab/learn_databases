import pandas as pd

sheef_df = pd.read_excel('./datasets_template.xlsx', sheet_name='programers_ANIMAL_INS',header=3)

import sqlite3

con = sqlite3.connect("./db.sqlite3")

sheef_df.to_sql('ANIMAL_INS', con, if_exists='replace')

pass