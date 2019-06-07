from ncaa.cleanData import cleanData
from ncaa import analysis
from ncaa.load_data import load_data

if __name__ == '__main__':
    import sqlite3 as sql

    conn = sql.connect("ncaa_pbp.db")
    year = 2018
    grouping=['PlayerName', 'EventPlayerID_sbsq']
    
    df = load_data(year, conn, limit=1000, toAdd=['name', 'team', 'gameID'])
    df = cleanData(df)
    print(df.columns)
    df = analysis.prep(df, conn)
    df = df.apply_grouping(grouping)
    
    df.sort_values('Count', inplace=True, ascending=False)
    print(df)
    
    import matplotlib.pyplot as plt
    plt.scatter(df['Count'], df['AveragePoints'])
    for i, txt in enumerate(df.index):
        plt.gca().annotate(txt, (df['Count'][i], df['AveragePoints'][i]))
    #plt.show()
    