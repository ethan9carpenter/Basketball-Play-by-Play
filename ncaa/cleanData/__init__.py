from ncaa.cleanData._ftToSingleEvent import singularFT
from ncaa.cleanData._cleanData import _doAndOnes, _do_assists, _proper_col_type


def cleanData(df, reindex=False):
    df = singularFT(df)
    df = _doAndOnes(df)   #slow
    df = _do_assists(df)
    df = _proper_col_type(df)
    
    
    if reindex:
        df.reset_index(inplace=True)
    
    df.sort_index(inplace=True)

    return df
    