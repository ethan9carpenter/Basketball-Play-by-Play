import pandas as pd
import json
from ncaa.analysis.analyze import DataToAnalyze

pointVals = json.load(open('pointVals.json'))

def _applyPointValues(df):
    df['PointValue'] = df['EventType'].apply(lambda x: pointVals[x])
    df['PointValue'] += df['madeFT']
    
    return df



def _getProperColsAndSbsq(df):
    
    df.reset_index(inplace=True)
    df.sort_values(['EventTeamID', 'EventID'], inplace=True)
    
    df = df.join(df.shift(-1), rsuffix='_sbsq')
    

    df = df[(df['EventTeamID'] == df['EventTeamID_sbsq']) &
            (df['GameID'] == df['GameID_sbsq'])]

    return df

def prep(df, conn):
    """
    Preconditions
    :    Already in possession format via ncaa.cleanData.cleanData
    """
    
    df = _applyPointValues(df)
    df = _getProperColsAndSbsq(df)
    

    return DataToAnalyze(df)
    






