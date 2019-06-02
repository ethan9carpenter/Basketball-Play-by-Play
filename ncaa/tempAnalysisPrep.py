import sqlite3 as sql
import pandas as pd
import json

conn = sql.connect("ncaa_pbp.db")
'''
df = pd.read_sql("""
                    SELECT
                        EventPlayerID, EventTeamID, EventType, EventID
                    From
                        test
                    Limit
                        1000000000
                     """, conn, index_col='EventID')
                     '''

pointVals = json.load(open('pointVals.json')) 


def _applyPointValues(df):
    df['PointValue'] = df['EventType'].apply(lambda x: pointVals[x])
    
    return df

def tidy_names(name):
    name = name.split('_')
    first = name[-1]
    last = ' '.join(name[:-1])
    name = first.title() + ' ' + last.title()

    return name

def _add_names(df):
    names = pd.read_sql("""Select PlayerID, PlayerName FROM players""", conn)

    df.set_index('EventPlayerID', inplace=True)
    names['PlayerName'] = names['PlayerName'].apply(tidy_names)
    names.set_index('PlayerID', inplace=True)
    df = df.join(names)
    
    return df


def _grouping(df):
    mean = df.groupby(['PlayerName', 'EventType']).mean()
    mean.columns = ['AveragePoints']
    count = df.groupby(['PlayerName', 'EventType']).count()
    count.columns = ['Count']
    
    df = mean.join(count)
    
    return df

def _getProperColsAndSbsq(df):
    df.reset_index(inplace=True)
    df.sort_values(['EventTeamID', 'EventID'], inplace=True)
    df = df.join(df.shift(-1), rsuffix='_sbsq')
    
    df.drop(['EventType_sbsq', 'EventPlayerID_sbsq', 'EventID_sbsq'], axis=1, inplace=True)
    
    df = df[df['EventTeamID'] == df['EventTeamID_sbsq']]
    
    df = df[['EventPlayerID', 'EventType', 'PointValue_sbsq']]
    
    return df


def prep(df):
    #Precondition: already in possession format
    df = _applyPointValues(df)
    df = _getProperColsAndSbsq(df)
    df = _add_names(df)
    df = _grouping(df)
    
    return df

if __name__ == '__main__':
    from collections import Counter
    import pandas as pd
    import sqlite3 as sql
    
    conn = sql.connect("ncaa_pbp.db")
    year = 2010
    df = pd.read_sql("""
                    SELECT
                        EventPlayerID, EventTeamID, EventType, EventID
                    From
                        "poss_{}"
                    WHERE
                        EventType NOT LIKE "%8"
                     """.format(year), conn, index_col='EventID')
    prep(df)
    




