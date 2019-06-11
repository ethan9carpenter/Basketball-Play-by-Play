from ncaa import analysis
from ncaa.load_data import load_data, load_clean
from ncaa.analysis.analyze import apply_grouping

if __name__ == '__main__':
    import sqlite3 as sql

    conn = sql.connect("ncaa_pbp.db")
    year = 2012
    
    df = load_clean(year, conn, limit='')
    
    df = analysis.prep(df)
    
    
    df = df[df['PlayerName'] == 'Anthony Davis']
    df = apply_grouping(df, ['PlayerName', 'EventType'])