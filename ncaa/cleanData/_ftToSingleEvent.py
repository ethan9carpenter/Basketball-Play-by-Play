import pandas as pd

ftEventNames = ('made1_free', 'miss1_free')

def _prepare(df):
    df = df[['EventType', 'ElapsedSeconds']]
    df = df[df['EventType'].isin(ftEventNames)]

    temp = df.shift(1)
    temp = temp.join(df, lsuffix='_-1')
    temp = temp.join(df.shift(-1), rsuffix='_1')
    temp = temp.join(df.shift(-2), rsuffix='_2')
    
    df = temp
    df = df[(df['ElapsedSeconds_-1'] != df['ElapsedSeconds'])]

    df.drop(['ElapsedSeconds_-1', 'EventType_-1'], axis=1, inplace=True)
    
    for col in ('EventType', 'EventType_1', 'EventType_2'):
        df[col] = (df[col] == 'made1_free')
    
    return df

def _getByLen(df):
    oneBoo = df['ElapsedSeconds'] != df['ElapsedSeconds_1']
    twoBoo = df['ElapsedSeconds'] == df['ElapsedSeconds_1']
    threeBoo = df['ElapsedSeconds'] == df['ElapsedSeconds_2']
    
    oneFT = df[oneBoo & ~twoBoo]
    twoFT = df[twoBoo & ~threeBoo]
    threeFT = df[threeBoo]
    
    oneFT = oneFT[['ElapsedSeconds', 'EventType']]
    twoFT = twoFT[['ElapsedSeconds', 'EventType', 'ElapsedSeconds_1', 'EventType_1']]
    threeFT = threeFT[['ElapsedSeconds', 'EventType', 'ElapsedSeconds_1', 'EventType_1', 
                     'ElapsedSeconds_2', 'EventType_2']]
    
    return oneFT, twoFT, threeFT


def _get_ind_seq(df, num):
    df['numMade'] = df['EventType'].astype(int)
    for i in range(1, num):
        df['numMade'] += df['EventType_'+str(i)].astype(int)
    
    groups = [df[df['numMade'] == i] for i in range(num+1)]
    names = [str(i) + '_' + str(num) for i in range(num+1)]

    return dict(zip(names, groups))

def _getBySeq(oneFT, twoFT, threeFT):
    seqs = {}
    
    for i, df in enumerate([oneFT, twoFT, threeFT]):
        seqs.update(_get_ind_seq(df, i+1))

    for name in seqs:
        data = seqs[name]
        data['EventType'] = 'ft'
        data['madeFT'] = int(name[0])
        data['attFT'] = int(name[-1])
    
    return pd.concat(seqs.values(), sort=False)

def singularFT(df):
    original = df.copy()
    df = _prepare(df)

    oneFT, twoFT, threeFT = _getByLen(df)

    finalDF = _getBySeq(oneFT, twoFT, threeFT)
    fts = original[original['EventType'].isin(ftEventNames)]
    
    fts.drop('EventType', inplace=True, axis=1)
    fts = fts.join(finalDF[['EventType', 'madeFT', 'attFT']])

    cols = list(original.columns) + ['madeFT', 'attFT']
    fts = fts[cols]

    fts = fts[fts.index.isin(finalDF.index)]

    original = original[~original['EventType'].isin(ftEventNames)]
    for col in ('madeFT', 'attFT'):
        original[col] = 0

    original = original.append(fts)
    

    return original
    
    
    
