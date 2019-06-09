import warnings
warnings.filterwarnings('ignore')

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
    df.reset_index(inplace=True)
    df.set_index('EventID', inplace=True)
    
    df = df.fillna(value={'madeFT_': 0, 'attFT_': 0})

    df['madeFT'] += df['madeFT_']
    df['attFT'] += df['attFT_']

    df.drop(['attFT_', 'madeFT_'], inplace=True, axis=1)    

    return df


def do_assists(df):
    """
    Preconditions
    -------------
    -Already did andOnes
    """
    #shifting 1 instead of -1 because of how assists appear in pbp data
    
    df['isAssisted'] = df['EventType'].shift(1) == 'assist'
        
        
    for col in ['PlayerName', 'EventPlayerID']:
        df['assist'+col] = df[col].shift(1)
        df['assist'+col] = df[df['isAssisted']]['assist'+col]

    df = df[df['EventType'] != 'assist']
    
    return df