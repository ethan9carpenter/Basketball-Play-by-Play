import pandas as pd
from ncaa.cleanData import cleanData


def write_off_poss(conn, yearEnd, tableName=None, reindex=False):
    df = pd.read_sql("""
                        SELECT
                            *
                        From
                            "{}-{}"
                         """.format(yearEnd-1, yearEnd), conn, index_col='EventID')
    
    df = cleanData(df, reindex=reindex)
    df = df[~df['EventType'].isin(['made2_jump_and8', 'made3_jump_and8', 'made2_tip_and8', 'made2_lay_and8'])]
    
    if tableName is None:
        df.to_sql('poss_{}'.format(yearEnd), conn)


#FIX THE and8 issue
#might have a problem somehwer when sorting by team, could lose chronological order, make sure that it stays in order
#add a line to make sure last play of one game and first play of next game are not pairs

#df = df[df['EventType'].isin(['made2_jump_and8', 'made3_jump_and8', 'made2_tip_and8', 'made2_lay_and8'])]