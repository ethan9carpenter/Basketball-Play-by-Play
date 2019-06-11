import json

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

def prep(df, how='o'):
    """
    Preconditions
    :    Already in possession format via ncaa.cleanData.cleanData
    """
    df = _applyPointValues(df)
    df = _getProperColsAndSbsq(df, how=how)
    df.set_index('EventID', inplace=True)
    df = df[df['PlayerName'] != 'Team']
    df.sort_index(inplace=True)

    return df
    






