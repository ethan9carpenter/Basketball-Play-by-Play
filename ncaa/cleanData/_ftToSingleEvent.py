import pandas as pd

madeFT = 'made1_free'
missFT = 'miss1_free'
ftEvents = (madeFT, missFT)

def _getByTripLen(df):
    oneFT = df[(df['ElapsedSeconds'] != df['ElapsedSeconds_2']) &
               (df['ElapsedSeconds'] != df['ElapsedSeconds_3'])]
    twoFT = df[(df['ElapsedSeconds'] == df['ElapsedSeconds_2']) &
               (df['ElapsedSeconds'] != df['ElapsedSeconds_3'])]
    threeFT = df[(df['ElapsedSeconds'] == df['ElapsedSeconds_2']) &
               (df['ElapsedSeconds'] == df['ElapsedSeconds_3'])]
    oneFT = oneFT[:2]
    twoFT = twoFT[:4]
    threeFT = threeFT[:6]
    
    return oneFT, twoFT, threeFT

def _getByOutcome(oneFT, twoFT, threeFT):
    _0 = oneFT[~oneFT['EventType']]
    _1 = oneFT[oneFT['EventType']]
    _00 = twoFT[(~twoFT['EventType']) & (~twoFT['EventType_2'])]
    _01 = twoFT[(~twoFT['EventType']) & (twoFT['EventType_2'])]
    _11 = twoFT[(twoFT['EventType']) & (twoFT['EventType_2'])]
    _000 = threeFT[(~threeFT['EventType']) & (~threeFT['EventType_2']) & (~threeFT['EventType_3'])]
    _001 = threeFT[(~threeFT['EventType']) & (~threeFT['EventType_2']) & (threeFT['EventType_3'])]
    _011 = threeFT[(~threeFT['EventType']) & (threeFT['EventType_2']) & (threeFT['EventType_3'])]
    _111 = threeFT[(threeFT['EventType']) & (threeFT['EventType_2']) & (threeFT['EventType_3'])]
    
    return [_0, _1,
            _00, _01, _11,
            _000, _001, _011, _111]
    
def _createSeqDF(df):
    temp = df.shift(1)
    temp = temp.join(df, lsuffix='_prev')
    temp = temp.join(df.shift(-1), rsuffix='_2')
    temp = temp.join(df.shift(-2), rsuffix='_3')
    df = temp
    
    return df

def _trimAndFormat(df):
    df = df[(df['ElapsedSeconds_prev'] != df['ElapsedSeconds'])]
    df.drop(['ElapsedSeconds_prev', 'EventType_prev'], axis=1, inplace=True)
    
    
    df['EventType'] = df['EventType'] == madeFT
    df['EventType_2'] = df['EventType_2'] == madeFT
    df['EventType_3'] = df['EventType_3'] == madeFT

def _replaceFT(finalDF, original):
    original['ftCode'] = finalDF
    toRem = original[original['EventType'].isin(ftEvents)]
    toRem = toRem[~toRem.index.isin(finalDF.index)]
    original = original[~original.index.isin(toRem.index)]
    
    return original

def singularFT(df):
    original = df.copy()
    df = df['EventID', 'ElapsedSeconds', 'EventType']
    
    df = _createSeqDF(df)
    df = _trimAndFormat(df)
    
    oneFT, twoFT, threeFT = _getByTripLen(df)
    seqs = _getByOutcome(oneFT, twoFT, threeFT)
    
    for i, data in enumerate(seqs):
        data['ftCode'] = i
    finalDF = pd.concat(seqs)
    
    finalDF = _replaceFT(finalDF, original)

    return original

