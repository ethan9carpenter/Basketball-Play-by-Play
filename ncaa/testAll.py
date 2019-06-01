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
                        1000000000
                     """, conn, index_col='EventID')

df = cleanData(df, reindex=False)
df.to_sql('test', conn, if_exists='replace')

df = df[df['EventType'].isin(['made2_jump_and8', 'made3_jump_and8', 'made2_tip_and8', 'made2_lay_and8'])]