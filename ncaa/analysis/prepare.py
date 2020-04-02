import json
import pandas as pd
from ncaa.analysis.analyze import apply_grouping

_pointVals = json.load(open('resources/pointVals.json'))

def _applyPointValues(df):
    df['PointValue'] = df['EventType'].apply(lambda x: _pointVals[x])
    df['PointValue'] += df['madeFT']
    
    return df

def _getProperColsAndSbsq(df, how):
    df.reset_index(inplace=True)
    
    if how == 'o':
        df.sort_values(['EventTeamID', 'EventID'], inplace=True)
        
        df = df.join(df.shift(-1), rsuffix='_sbsq')
    
        df = df[(df['EventTeamID'] == df['EventTeamID_sbsq']) &
                (df['GameID'] == df['GameID_sbsq'])]
    
    return df

def prep(df, year, conn, how='o'):
    """
    Preconditions
    :    Already in possession format via ncaa.cleanData.cleanData
    """
    df = _applyPointValues(df)
    df = _getProperColsAndSbsq(df, how=how)
    df.set_index('EventID', inplace=True)
    df = df[df['PlayerName'] != 'Team']
    df.sort_index(inplace=True)

    conferences_df = pd.read_sql("SELECT ConfAbbrev, TeamID FROM TeamConferences WHERE Season ={year}".format(year=year), conn)
    
    df = pd.merge(df, conferences_df, 'left', 'TeamID', suffixes=['', '_'])
    df = df[['PlayerName', 'EventPlayerID', 'TeamID', 'TeamName', 'EventType', 'PointValue_sbsq', 'ConfAbbrev']]
     
    return df

def visual_filters(df, labelCols, minCount=0, conferences=None):
    constantCols = ['EventPlayerID', 'TeamID', 'TeamName']

    if conferences:
        df = df[df['ConfAbbrev'].isin(conferences)]
    teamAvg = apply_grouping(df, ['TeamID'])['AveragePoints']
    df = apply_grouping(df, constantCols + labelCols)
    df = df[df['Count'] > minCount]
    
    df.reset_index(inplace=True)
    df = pd.merge(df, teamAvg.reset_index().rename({'AveragePoints': 'TeamAvg'}, axis=1), on='TeamID', how='left') 
        
    return df
    






