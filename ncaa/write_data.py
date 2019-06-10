from ncaa.cleanData import cleanData
from ncaa.load_data import load_data


def write_clean_off_poss(conn, yearEnd, newTableName=None, reindex=False, if_exists='fail'):
    df = load_data(yearEnd, conn, toAdd=['name', 'gameID', 'team'])
    
    df = cleanData(df, reindex=reindex)
    
    if newTableName is None:
        newTableName = 'clean_{}'.format(yearEnd)
       
    df.to_sql(newTableName, conn, if_exists=if_exists)
    
    return df


if __name__ == '__main__':
    import sqlite3
    import cProfile
    for year in range(2010, 2019+1):
        write_clean_off_poss(sqlite3.connect('ncaa_pbp.db'), year, if_exists='replace')
        print(year)
"""
    cProfile.run('''
write_clean_off_poss(sqlite3.connect('ncaa_pbp.db'), 2010, if_exists='replace')
''', sort='cumtime')
"""