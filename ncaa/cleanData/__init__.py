from ncaa.cleanData._ftToSingleEvent import singularFT
from ncaa.cleanData._cleanData import doAndOnes, do_assists


def cleanData(df):
    df = do_assists(df)
    df = singularFT(df)
    
    df = doAndOnes(df)
    
    df.sort_index(inplace=True)
    
    return df
    