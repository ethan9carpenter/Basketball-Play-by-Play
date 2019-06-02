import sqlite3 as sql
import pandas as pd
from ncaa.cleanData import cleanData

conn = sql.connect("ncaa_pbp.db")

for year in range (2014, 2019+1):
    df = pd.read_sql("""
                        SELECT
                            *
                        From
                            "{}-{}"
                         """.format(year-1, year), conn, index_col='EventID')
    
    df = cleanData(df, reindex=False)
    df = df[~df['EventType'].isin(['made2_jump_and8', 'made3_jump_and8', 'made2_tip_and8', 'made2_lay_and8'])]
    df.to_sql('poss_{}'.format(year), conn)
    print(year)


#FIX THE and8 issue
#might have a problem somehwer when sorting by team, could lose chronological order, make sure that it stays in order
#add a line to make sure last play of one game and first play of next game are not pairs

#df = df[df['EventType'].isin(['made2_jump_and8', 'made3_jump_and8', 'made2_tip_and8', 'made2_lay_and8'])]