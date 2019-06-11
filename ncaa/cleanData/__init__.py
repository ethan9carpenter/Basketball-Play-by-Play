from ncaa.cleanData._ftToSingleEvent import singularFT
from ncaa.cleanData._cleanData import doAndOnes, do_assists, proper_col_type


def cleanData(df, reindex=False):
    df = singularFT(df)
    df = doAndOnes(df)   #slow
    df = do_assists(df)
    df = proper_col_type(df)
    
    
    if reindex:
        df.reset_index(inplace=True)
    
    df.sort_index(inplace=True)

    return df
    