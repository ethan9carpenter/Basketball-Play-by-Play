from ncaa import analysis
from ncaa.load_data import load_data, load_clean
from ncaa.analysis.analyze import apply_grouping
from ncaa.plot import plot

if __name__ == '__main__':
    import sqlite3 as sql

    conn = sql.connect("ncaa_pbp.db")
    year = 2019
    
    df = load_clean(year, conn, limit='')
    df = analysis.prep(df)
    #avg = df['PointValue'].mean()
    
    df = df[df['PlayerName'] != 'Team']
    
    df = df[df['TeamName'].isin(['Duke'])]
    #df = df[df['EventType'].isin(['made3_jump', 'miss3_jump', 'made2_dunk'])]
    
    teams = apply_grouping(df, ['TeamName'])
    df = apply_grouping(df, ['PlayerName', 'TeamName', 'EventType'])
    
    df['AveragePoints'] -= teams['AveragePoints']
    df.reset_index(level=1, drop=True, inplace=True)
    
    df = df[df['Count'] > 35]
    df = df.loc[['Reddish Cam', 'Williamson Zion', 'Barrett Rj']]
    
    df.sort_values('Count', inplace=True, ascending=False)
    
    #df = df.head(25)
    
    print(df)
    plot(df, avg=0)