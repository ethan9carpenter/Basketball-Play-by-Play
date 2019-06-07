import pandas as pd
from ncaa.cleanData import cleanData


def write_off_poss(conn, yearEnd, newTableName=None, reindex=False):
    df = pd.read_sql("""
                        SELECT
                            *
                        From
                            "{}-{}"
                         """.format(yearEnd-1, yearEnd), conn, index_col='EventID')
    
    df = cleanData(df, reindex=reindex)
    #df = df[~df['EventType'].isin(['made2_jump_and8', 'made3_jump_and8', 'made2_tip_and8', 'made2_lay_and8'])]
    
    if newTableName is None:
        df.to_sql('poss_{}'.format(yearEnd), conn)


if __name__ == '__main__':
    import sqlite3
    write_off_poss(sqlite3.connect('ncaa_pbp.db'), 2011)