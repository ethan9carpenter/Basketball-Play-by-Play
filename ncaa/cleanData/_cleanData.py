import warnings
import json
import pandas as pd
warnings.filterwarnings('ignore')

def _doAndOnes(df):
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
    df.reset_index(inplace=True)
    df.set_index('EventID', inplace=True)
    
    df = df.fillna(value={'madeFT_': 0, 'attFT_': 0})

    df['madeFT'] += df['madeFT_']
    df['attFT'] += df['attFT_']

    df.drop(['attFT_', 'madeFT_'], inplace=True, axis=1)    

    return df


def _do_assists(df):
    """
    Preconditions
    -------------
    -Already did andOnes
    """
    #shifting 1 instead of -1 because of how assists appear in pbp data
    
    df['isAssisted'] = df['EventType'].shift(1) == 'assist'
        
        
    for col in ['PlayerName', 'EventPlayerID']:
        assistCol = 'assist'+col
        
        df[assistCol] = df[col].shift(1)
        df[assistCol] = df[df['isAssisted']][assistCol]
    
    df.rename({'assistEventPlayerID': 'assistPlayerID'}, inplace=True, axis=1)
    df['assistPlayerID'] = df['assistPlayerID'].fillna(-1)

    df = df[df['EventType'] != 'assist']
    
    
    return df

def _do_assists_(df):
    """
    Preconditions
    -------------
    -Already did andOnes
    """    
    assists = df[df['EventType'] == 'assist']
    assists = assists[['EventPlayerID', 'PlayerName', 'GameID', 'EventTeamID', 'WPoints', 'LPoints']]
    assists.rename({'EventPlayerID': 'assistPlayerID',
                    'PlayerName': 'assistPlayerName'},
                    axis=1, inplace=True)
    
    df = df[df['EventType'] != 'assist']
    df = pd.merge(df.reset_index(), assists, on=['GameID', 'EventTeamID', 'WPoints', 'LPoints'], how='left')
    df.set_index('EventID', inplace=True)
    
    
    df['assistPlayerID'] = df['assistPlayerID'].fillna(-1)
    df['isAssisted'] = df[df['assistPlayerID'] >= 0] 
    
    return df

def _proper_col_type(df):
    properTypes = json.load(open('resources/properTypes.json'))

    for col in df:
        df[col] = df[col].astype(properTypes[col])
            
    return df    
    