

pointVals = {'miss2_dunk': 0, 
             'made2_lay': 2, 
             'miss3_jump': 0,
             'made1_free': 1,
             'made2_dunk': 2,
             'made2_tip_and1': 3,
             'miss2_jump': 0,
             'made2_dunk_and0': 2,
             #'made2_jump_and8': ,
             #'made3_jump_and8': ,
             'made2_jump_and0': 2,
             #'made2_tip_and8': ,
             'made3_jump_and1': 4,
             'made2_lay_and0': 2,
             'made3_jump_and0': 3,
             'made2_jump_and1': 3,
             'made3_jump': 3,
             'miss2_tip': 0,
             'made2_jump': 2,
             'made2_tip': 2,
             'made2_tip_and0': 2,
             'made2_dunk_and1': 3,
             'miss2_lay': 0,
             #'made2_lay_and8': ,
             'miss1_free': 0,
             'made2_lay_and1': 3}


def applyPointValues(df):
    df['EventType'] = df['EventType'].apply(lambda x: pointVals[x])
    
    return df