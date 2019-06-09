from ncaa.cleanData import cleanData
from ncaa.load_data import load_data


def write_clean_off_poss(conn, yearEnd, newTableName=None, reindex=False, if_exists='fail'):
    df = load_data(yearEnd, conn, toAdd=['name', 'gameID', 'team'])
    df = cleanData(df, reindex=reindex)
    
    if newTableName is None:
        newTableName = 'poss_{}'.format(yearEnd)
        
    df.to_sql(newTableName, conn, if_exists=if_exists)
    
    return df


if __name__ == '__main__':
    import sqlite3
    write_clean_off_poss(sqlite3.connect('ncaa_pbp.db'), 2010, if_exists='replace')