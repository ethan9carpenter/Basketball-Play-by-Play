import pandas as pd
import sqlite3 as sql
#from ncaa.cleanData import ftEventNames
ftEventNames = ('made1_free', 'miss1_free')


def _prepare(df):
    df = df[['EventType', 'ElapsedSeconds']]
    df = df[df['EventType'].isin(ftEventNames)]
    
    temp = df.shift(1)
    temp = temp.join(df, lsuffix='_prev')
    temp = temp.join(df.shift(-1), rsuffix='_2')
    temp = temp.join(df.shift(-2), rsuffix='_3')
    df = temp

    df = df[(df['ElapsedSeconds_prev'] != df['ElapsedSeconds'])]

    df.drop(['ElapsedSeconds_prev', 'EventType_prev'], axis=1, inplace=True)
    
    df['EventType'] = df['EventType'] == 'made1_free'
    df['EventType_2'] = df['EventType_2'] == 'made1_free'
    df['EventType_3'] = df['EventType_3'] == 'made1_free'
    
    return df

def _getByLen(df):
    oneFT = df[(df['ElapsedSeconds'] != df['ElapsedSeconds_2']) &
               (df['ElapsedSeconds'] != df['ElapsedSeconds_3'])]
    twoFT = df[(df['ElapsedSeconds'] == df['ElapsedSeconds_2']) &
               (df['ElapsedSeconds'] != df['ElapsedSeconds_3'])]
    threeFT = df[(df['ElapsedSeconds'] == df['ElapsedSeconds_2']) &
               (df['ElapsedSeconds'] == df['ElapsedSeconds_3'])]

    oneFT = oneFT[['ElapsedSeconds', 'EventType']]
    twoFT = twoFT[['ElapsedSeconds', 'EventType', 'ElapsedSeconds_2', 'EventType_2']]
    threeFT = threeFT[['ElapsedSeconds', 'EventType', 'ElapsedSeconds_2', 'EventType_2', 
                     'ElapsedSeconds_3', 'EventType_3']]
    
    return oneFT, twoFT, threeFT

def _getBySeq(oneFT, twoFT, threeFT):
    # name is _made_attempts
    _1_2 = twoFT[(~twoFT['EventType']) & (twoFT['EventType_2'])]
    _2_2 = twoFT[(twoFT['EventType']) & (twoFT['EventType_2'])]
    _0_2 = twoFT[(~twoFT['EventType']) & (~twoFT['EventType_2'])]
    _0_1 = oneFT[~oneFT['EventType']]
    _1_1 = oneFT[oneFT['EventType']]
    _0_3 = threeFT[(~threeFT['EventType']) & (~threeFT['EventType_2']) & (~threeFT['EventType_3'])]
    _1_3 = threeFT[(~threeFT['EventType']) & (~threeFT['EventType_2']) & (threeFT['EventType_3'])]
    _2_3 = threeFT[(~threeFT['EventType']) & (threeFT['EventType_2']) & (threeFT['EventType_3'])]
    _3_3 = threeFT[(threeFT['EventType']) & (threeFT['EventType_2']) & (threeFT['EventType_3'])]
    
    seqs = [_0_1, _1_1, _0_2, _1_2, _2_2,   
            _0_3, _1_3, _2_3, _3_3]
    
    for i, data in enumerate(seqs):
        data['ftCode'] = i
        print(i, data.__name__)
    
    return seqs

def singularFT(df):
    original = df.copy()
    df = _prepare(df)
    
    oneFT, twoFT, threeFT = _getByLen(df)
    seqs = _getBySeq(oneFT, twoFT, threeFT)
    
    finalDF = pd.concat(seqs)    
    finalDF = finalDF['ftCode']    
    
    original['ftCode'] = finalDF    
    
    toRemove = original[original['EventType'].isin(ftEventNames)]
    toRemove = toRemove[~toRemove.index.isin(finalDF.index)]    
    
    original = original[~original.index.isin(toRemove.index)]    
    
    return original


if __name__ == '__main__':
    conn = sql.connect("ncaa_pbp.db")
    data = pd.read_sql("""
                    SELECT
                        *
                    From
                        "2016-2017"
                    Limit
                        1000
                     """, conn, index_col='EventID')
    result = singularFT(data)
    #result = result[result['EventType'].isin(ftEventNames)]
    print(result)
    
    
    
    
