import pandas as pd
import warnings
#warnings.filterwarnings('ignore')

def doAndOnes(df):
    """
    Preconditions
    -------------
    -Already singularizedFTs
    """
    df.reset_index(inplace=True)
    df.set_index(['ElapsedSeconds', 'EventTeamID', 'GameID', 'EventPlayerID'], inplace=True)
    
    fts = df[df['attFT'] == 1]
    df = df[df['attFT'] != 1]
    
    fts = fts[['madeFT', 'attFT']]
    
    
    df = df.join(fts, rsuffix='_')
    df['madeFT'] += df['madeFT_']
    df['attFT'] += df['attFT_']
    
    df.drop(['attFT_', 'madeFT_'], inplace=True, axis=1)
    
    df.reset_index(inplace=True)
    df.set_index('EventID', inplace=True)

    return df
    
    
if __name__ == '__main__':
    from ncaa.cleanData._ftToSingleEvent import singularFT
    import sqlite3 as sql


    df = pd.read_sql("""
                     SELECT * FROM "2017-2018" LIMIT 1000
                     """, sql.connect('ncaa_pbp.db'), index_col='EventID')
    df = singularFT(df)
    print(doAndOnes(df))