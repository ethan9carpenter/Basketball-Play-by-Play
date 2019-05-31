import sqlite3 as sql
import pandas as pd
from ncaa.cleanData import cleanData

conn = sql.connect("ncaa_pbp.db")
df = pd.read_sql("""
                    SELECT
                        *
                    From
                        "2017-2018"
                    Limit
                        1000000
                     """, conn, index_col='EventID')

df = cleanData(df)
df = df[df.columns[9:]]
df = df[df['ftCode'].isin([0, 1])]
print(df)