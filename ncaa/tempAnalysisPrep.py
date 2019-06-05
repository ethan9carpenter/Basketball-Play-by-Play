import pandas as pd
import json
from ncaa.cleanData import cleanData

#class GroupingAnalysis: ??????

pointVals = json.load(open('pointVals.json'))

def _applyPointValues(df):
    df['PointValue'] = df['EventType'].apply(lambda x: pointVals[x])
    
    return df

def tidy_name(name):
    name = name.split('_')
    first = name[-1]
    name = ' '.join([first]+name[:-1])

    return name.title()

def _add_names(df, conn):
    names = pd.read_sql("""Select 
                               PlayerID, PlayerName, TeamName
                           FROM 
                               players
                           LEFT OUTER JOIN 
                               Teams
                           WHERE 
                               Teams.TeamID = players.TeamID
                               AND PlayerName is not "Team"
                        """, conn)

    names['PlayerName'] = names['PlayerName'].apply(tidy_name)
    df = pd.merge(df, names, how='left', left_on='EventPlayerID', right_on='PlayerID')
    
    return df

def _grouping(df, grouping):    
    grouped = df.groupby(grouping)
    
    mean = pd.DataFrame(grouped.mean()['PointValue_sbsq'])
    mean.columns = ['AveragePoints']
    
    count = pd.DataFrame(grouped.count()['PointValue_sbsq'])
    count.columns = ['Count']
    df = mean.join(count)
    
    return df

def _getProperColsAndSbsq(df):
    
    df.reset_index(inplace=True)
    df.sort_values(['EventTeamID', 'EventID'], inplace=True)
    
    df = df.join(df.shift(-1), rsuffix='_sbsq')
    

    df = df[(df['EventTeamID'] == df['EventTeamID_sbsq']) &
            (df['GameID'] == df['GameID_sbsq'])]

    return df

def _sameFT(event):
    ftTypes = ['ft_0_1', 'ft_1_1', 'ft_0_2', 
               'ft_1_2', 'ft_2_2', 'ft_0_3',
               'ft_1_3', 'ft_2_3', 'ft_3_3']
    if event in ftTypes:
        return 'ft'
    else:
        return event

def _all_ft_same(df):
    
    df['EventType'] = df['EventType'].apply(_sameFT)
    #df['EventType'].loc[df['EventType'].isin(ftTypes)] = 'ft'
    #print(df['EventType'].loc[df['EventType'].isin(ftTypes)])
    return df


def prep(df, conn, grouping=None, uniqueft=False):
    """
    Precondition: already in possession format
    
    grouping : array-like
        ('PlayerName', 'EventType', 'isAssisted', 'assistPlayerID', 'TeamName') 
    """
    
    df = _applyPointValues(df)
    df = _getProperColsAndSbsq(df)
    df = _add_names(df, conn)

    if uniqueft:
        df = _all_ft_same(df)
    if grouping is not None: 
        df = _grouping(df, grouping)

    return df

def _add_game_id(df, conn):
    """SELECT
        *,
        "2011-2012".Season
    FROM
        "2011-2012"
        LEFT OUTER JOIN games
    WHERE
        games.Season = "2011-2012".Season
        AND games.WTeamID = "2011-2012".WTeamID
        AND games.LTeamID = "2011-2012".LTeamID
        AND games.DayNum = "2011-2012".DayNum
    LIMIT 1000
    """
    on = ['WTeamID', 'LTeamID', 'Season', 'DayNum']
    games = pd.read_sql("SELECT * FROM games", conn)
    
    df = pd.merge(games, df.reset_index(), on=on, how='right')
    df.set_index('EventID', inplace=True)
    
    return df

def load_data(year, conn, limit=''):
    tableName = '"{}-{}"'.format(year-1, year)
    if limit != '':
        limit = 'LIMIT ' + str(limit)
    df = pd.read_sql("""
                    SELECT
                        *
                    From
                        {0}
                    WHERE
                        EventType NOT LIKE "%8"
                        AND EventType IN 
                            (SELECT EventType FROM events WHERE isOffense = 1)
                    {1}
                     """.format(tableName, limit), conn, index_col='EventID')
    df = _add_game_id(df, conn)

    return df

if __name__ == '__main__':
    import sqlite3 as sql

    conn = sql.connect("ncaa_pbp.db")
    year = 2018
    grouping=['EventType', 'madeFT', 'attFT']
    
    df = load_data(year, conn, limit=1000)

    df = cleanData(df, reindex=False)

    df = prep(df, conn, grouping=grouping, uniqueft=True)
    df.sort_values('Count', inplace=True, ascending=False)
    print(df)
    
    import matplotlib.pyplot as plt
    plt.scatter(df['Count'], df['AveragePoints'])
    for i, txt in enumerate(df.index):
        plt.gca().annotate(txt, (df['Count'][i], df['AveragePoints'][i]))
    #plt.show()
    




