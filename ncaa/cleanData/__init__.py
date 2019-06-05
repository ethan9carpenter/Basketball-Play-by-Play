from ncaa.cleanData._ftToSingleEvent import singularFT
from ncaa.cleanData._andOnes import doAndOnes
from ncaa.cleanData._generalOff import do_assists
ftEventNames = ('made1_free', 'miss1_free')
ftCodes = {0: (0, 1), 
           1: (0, 1), 
           2: (0, 1),
           3: (0, 1),
           4: (0, 1)}

def cleanData(df, reindex=False):
    df = do_assists(df)
    df = singularFT(df)
    #df = doAndOnes(df)
    df.drop('index', axis=1, inplace=True)
    
    if reindex:
        df = df.reset_index()
    
    return df
    