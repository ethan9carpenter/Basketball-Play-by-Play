from ncaa.cleanData._ftToSingleEvent import singularFT
from ncaa.cleanData._andOnes import doAndOnes
from ncaa.cleanData._generalOff import do_assists


def cleanData(df):
    
    df = do_assists(df)
    
    df = singularFT(df)
    df = doAndOnes(df)
    df.sort_index(inplace=True)
    
    return df
    