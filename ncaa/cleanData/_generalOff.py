import pandas as pd
import sqlite3 as sql
import numpy as np

conn = sql.connect("ncaa_pbp.db")

offensivePlays = pd.read_sql("SELECT * FROM events WHERE isOffense", conn)
defensivePlays = pd.read_sql("SELECT * FROM events WHERE NOT isOffense", conn)

df = pd.read_sql("""
                SELECT
                    *
                From
                    "2017-2018"
                Limit
                    1000
                 """, conn)

def initial_trim(df):
    df = df[np.isin(df['EventType'], offensivePlays)]
    
    return df

def do_assists(df):
    df['previous'] = df['EventType'].shift(1)
    df['isAssisted'] = df['previous'] == 'assist'
    
    df = df.drop('previous', axis=1)
    
    df['assistID'] = df['EventPlayerID'].shift(1) 
    df['assistID'] = df[df['isAssisted']]['assistID']
    
    df = df.drop('test', axis=1)
    
    return df