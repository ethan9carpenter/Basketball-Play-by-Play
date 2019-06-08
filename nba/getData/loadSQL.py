import pandas as pd
import sqlite3 as sql

def loadQuery(fp, db):
    with open(fp) as file:
        query = file.read()
    conn = sql.connect(db)
    df = pd.read_sql(query, conn)
    
    return df    
    