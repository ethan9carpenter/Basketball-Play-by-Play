
def do_assists(df):
    #shifting 1 instead of -1 because of how assists appear in pbp data
    df['isAssisted'] = df['EventType'].shift(1) == 'assist'
        
    df['assistPlayerID'] = df['EventPlayerID'].shift(1) 
    df['assistPlayerID'] = df[df['isAssisted']]['assistPlayerID']
    
    df = df[df['EventType'] != 'assist']
    
    return df