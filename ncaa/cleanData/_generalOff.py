
def do_assists(df):
    df['previous'] = df['EventType'].shift(1)
    df['isAssisted'] = df['previous'] == 'assist'
    
    df.drop('previous', axis=1, inplace=True)
    
    df['assistPlayerID'] = df['EventPlayerID'].shift(1) 
    df['assistPlayerID'] = df[df['isAssisted']]['assistPlayerID']
    
    df = df[df['EventType'] != 'assist']
    
    return df