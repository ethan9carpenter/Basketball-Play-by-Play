import pandas as pd

def _add_game_id(df, conn):
    on = ['WTeamID', 'LTeamID', 'Season', 'DayNum']
    games = pd.read_sql("SELECT * FROM games", conn)

    df = pd.merge(games, df, on=on, how='right')
    
    return df

def _tidy_name(name):
    name = name.split('_')
    first = name[-1]
    name = ' '.join([first]+name[:-1])

    return name.title()

def _add_names(df, conn):
    names = pd.read_sql("""Select 
                               PlayerID, PlayerName
                           FROM 
                               players
                        """, conn)

    names['PlayerName'] = names['PlayerName'].apply(_tidy_name)
    df = pd.merge(df, names, how='left', left_on='EventPlayerID', right_on='PlayerID')
    
    return df

def _add_teams(df, conn):
    names = pd.read_sql("""Select 
                               TeamID, TeamName
                           FROM 
                               Teams
                        """, conn)

    df = pd.merge(df, names, how='left', left_on='EventTeamID', right_on='TeamID')
    
    return df

def load_data(year, conn, limit='', toAdd=[]):
    addOther = {'name': _add_names,
                'gameID': _add_game_id,
                'team': _add_teams}
    
    tableName = '"{}-{}"'.format(year-1, year)
    limit = 'LIMIT ' + str(limit) if isinstance(limit, int) else ''
    
    df = pd.read_sql("""
                    SELECT
                        *
                    From
                        {tableName}
                    WHERE
                        EventType NOT LIKE "%8"
                        AND EventType IN 
                            (SELECT EventType FROM events WHERE isOffense = 1)
                    {lim}
                     """.format(tableName=tableName, lim=limit), conn)
    for table in toAdd:
        df = addOther[table](df, conn)
        
    df.set_index('EventID', inplace=True)
    df.drop('index', axis=1, inplace=True)

    return df