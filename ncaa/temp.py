from ncaa.cleanData import cleanData
from ncaa import analysis
from ncaa.load_data import load_data
from ncaa.analysis.analyze import apply_grouping

if __name__ == '__main__':
    import sqlite3 as sql

    conn = sql.connect("ncaa_pbp.db")
    year = 2010
    grouping=['PlayerName']
    
    df = load_data(year, conn, limit=40, toAdd=['name', 'team', 'gameID'])
    
    df = cleanData(df)
    
    df = analysis.prep(df)
    df = df[df['PlayerName'] != 'Team']
    df = apply_grouping(df, grouping)
    df = df[df['Count'] > 500]
    
    df.sort_values('Count', inplace=True, ascending=False)
    
    print(df)
    import matplotlib.pyplot as plt
    plt.scatter(df['Count'], df['AveragePoints'])
    for i, txt in enumerate(df.index):
        plt.gca().annotate(txt, (df['Count'][i], df['AveragePoints'][i]))
    plt.show()
    