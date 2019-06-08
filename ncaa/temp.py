from ncaa.cleanData import cleanData
from ncaa import analysis
from ncaa.load_data import load_data
from ncaa.analysis.analyze import apply_grouping

if __name__ == '__main__':
    import sqlite3 as sql

    conn = sql.connect("ncaa_pbp.db")
    year = 2010
    grouping=['PlayerName']
    
    df = load_data(year, conn, limit=28, toAdd=['name', 'team', 'gameID'])
    df = df.iloc[-2:]
    df.to_csv('temp.csv')
    df = cleanData(df)
    df.to_csv('temp1.csv')
    df = analysis.prep(df)

    df = apply_grouping(df, grouping)
    
    df.sort_values('Count', inplace=True, ascending=False)
    print(df)
    import matplotlib.pyplot as plt
    plt.scatter(df['Count'], df['AveragePoints'])
    for i, txt in enumerate(df.index):
        plt.gca().annotate(txt, (df['Count'][i], df['AveragePoints'][i]))
    plt.show()
    