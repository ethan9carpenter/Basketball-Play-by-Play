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
    df['madeFT'] += df['madeFT_']
    df['attFT'] += df['attFT_']
    
    df.drop(['attFT_', 'madeFT_'], inplace=True, axis=1)
    
    df.reset_index(inplace=True)
    df.set_index('EventID', inplace=True)

    return df


def do_assists(df):
    #shifting 1 instead of -1 because of how assists appear in pbp data
    '''
    df['isAssisted'] = df['EventType'].shift(1) == 'assist'
        
    df['assistPlayerID'] = df['EventPlayerID'].shift(1) 
    df['assistPlayerID'] = df[df['isAssisted']]['assistPlayerID']
    '''
    df = df[df['EventType'] != 'assist']
    
    return df