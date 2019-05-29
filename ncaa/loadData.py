import pandas as pd
import sqlite3 as sql

def load(limit=-1):
    conn = sql.connect("ncaa_pbp.db")
    df = pd.read_sql("""
                SELECT
                    EventID, WTeamID, LTeamID, EventType, EventTeamID
                From
                    "2017-2018"
                WHERE
                    EventType LIKE "%2%" OR
                    EventType LIKE "%3%" OR
                    EventType is "turnover"
                 """, conn, index_col='EventID')
    
    return df