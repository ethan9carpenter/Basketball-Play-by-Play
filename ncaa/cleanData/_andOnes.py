import pandas as pd
import sqlite3 as sql
from ncaa.cleanData._ftToSingleEvent import singularFT
#from ncaa.cleanData import ftEventNames
import warnings
warnings.filterwarnings('ignore')

def _trimToAndOnePlays(df):
    toKeep = df[df['ftCode'] >= 0]['ElapsedSeconds']
    #    toKeep = df[df['attFT'] == 1]['ElapsedSeconds']

    df = df[df['ElapsedSeconds'].isin(toKeep)]

    df = df[(df['LPoints'] > 0) |
            (df['WPoints'] > 0) |
            (df['ftCode'].isin([0, 1]))]
    df = df[~df['ftCode'].isin([2, 3, 4, 5])]
    
    return df

def _createJoinedDF(df):
    ft = df[df['ftCode'] >= 0]
    shots = df[~df.index.isin(ft.index)]
    
    shots.reset_index(inplace=True)
    shots.set_index(['WTeamID', 'LTeamID', 'ElapsedSeconds', 'Season', 'DayNum'], inplace=True)
    ft.reset_index(inplace=True)
    ft.set_index(['WTeamID', 'LTeamID', 'ElapsedSeconds', 'Season', 'DayNum'], inplace=True)
    
    df = shots.join(ft, rsuffix='_ft')
    
    return df

def _renameAndNarrow(df):
    #Renames EventType so that it has shot type and ft results
    #narros to two columns that will be replaced in orig
    df['EventType'] = df['EventType'] + '_and' + df['ftCode_ft'].astype(int).apply(str)
    toDrop = df['EventID_ft']
    df.rename(columns={'ftCode_ft': 'ftCode'}, inplace=True)
    df = df[['EventType', 'ftCode']]
    
    return df, toDrop

def _replaceInOrig(orig, df, toDrop):
    orig = orig[~orig.index.isin(toDrop)] #drop all and1 ft attempts
    
    and1 = orig[orig.index.isin(df.index)]
    orig = orig[~orig.index.isin(df.index)]
    
    and1['ftCode'] = df['ftCode']
    and1['EventType'] = df['EventType']
    
    df = orig.append(and1)
    df.sort_index(inplace=True)
    
    return df

def doAndOnes(df):
    orig = df.copy()
    #pre: already singularizedFTs
    
    df = _trimToAndOnePlays(df)
    
    df = df[['Season', 'DayNum', 'WTeamID', 'LTeamID', 'ElapsedSeconds', 'EventType', 'ftCode']]
    
    df = _createJoinedDF(df)
    
    
    df.reset_index(inplace=True)
    df.set_index('EventID', inplace=True)
    
    df = df[['EventType', 'ftCode_ft', 'EventID_ft', 'EventType_ft']]
    df.dropna(inplace=True)
    
    df, toDrop = _renameAndNarrow(df)
    
    df = _replaceInOrig(orig, df, toDrop)
    
    return df
    
    
if __name__ == '__main__':
    df = pd.read_sql("""
                     SELECT * FROM "2017-2018" LIMIT 1000
                     """, sql.connect('ncaa_pbp.db'), index_col='EventID')
    df = singularFT(df)
    print(doAndOnes(df))