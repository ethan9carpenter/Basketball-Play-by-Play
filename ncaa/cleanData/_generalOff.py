import numpy as np
import sqlite3 as sql
import pandas as pd

conn = sql.connect("ncaa_pbp.db")

offensivePlays = pd.read_sql("SELECT * FROM events WHERE isOffense = 1", conn)
defensivePlays = pd.read_sql("SELECT * FROM events WHERE isOffense = 0", conn)


def initial_trim(df):
    df = df[np.isin(df['EventType'], offensivePlays)]
    
    return df

def do_assists(df):
    df['previous'] = df['EventType'].shift(1)
    df['isAssisted'] = df['previous'] == 'assist'
    
    df = df.drop('previous', axis=1)
    
    df['assistPlayerID'] = df['EventPlayerID'].shift(1) 
    df['assistPlayerID'] = df[df['isAssisted']]['assistPlayerID']
    
    df = df[df['EventType'] != 'assist']
    
    return df

if __name__ == '__main__':


    
    
    df = pd.read_sql("""
                    SELECT
                        *
                    From
                        "2017-2018"
                    Limit
                        1000
                     """, conn)