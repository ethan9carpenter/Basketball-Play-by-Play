import pandas as pd
from plot.plotSankey import Sankey
import numpy as np
import sqlite3 as sql

conn = sql.connect("ncaa_pbp.db")

df = pd.read_sql("""
                SELECT
                    EventID, WTeamID, LTeamID, EventType, EventTeamID
                From
                    "2017-2018"
                WHERE
                    EventType LIKE "%2%" OR
                    EventType LIKE "%3%" OR
                    EventType is "turnover"
                 """, conn)

def match_to_sbsq(df, cols_to_shift, cols_to_match):
    df.sort_values(by=['EventTeamID', 'EventID'], inplace=True)
    for col in cols_to_shift:
        df['next_'+col] = df[col].shift(-1)
    
    for col in cols_to_match:
        df = df[df[col] == df['next_'+col]]
        
    return df

def buildKey(sankey):
    pointDict = {
        'made2_dunk': 2,
        'made2_tip': 2,
        'made2_lay': 2,
        'made2_jump': 2,
        'made3_jump': 3,
        'miss2_dunk': 0,
        'miss2_tip': 0,
        'miss2_lay': 0,
        'miss2_jump': 0,
        'miss3_jump': 0,
        'turnover': 0
        }
    key = {}
    for typ in sankey.key:
        ID = sankey.key[typ]
        key[ID] = pointDict[typ]
        
    return key

df = match_to_sbsq(df, ['WTeamID', 'LTeamID', 'EventTeamID'], ['WTeamID', 'LTeamID', 'EventTeamID'])
source = df['EventType']
sankey = Sankey(source, length=3)

counts = sankey.plotDF
counts['target'] = counts['target'] - sankey.numNodes

pointDict = buildKey(sankey)

counts['points'] = [pointDict[ID % sankey.numNodes] for ID in counts['target']]
counts['points'] = counts['points'] * counts['count']


averages = {}

for value in range(10):
    data = counts[counts['source'] == value]
    count = np.sum(data['count'])
    total = np.sum(data['points'])
    averages[value] = total / count

averages = pd.DataFrame(zip(list(sankey.key.keys()), averages.values()), columns=['labels', 'values'])
averages.sort_values('values', ascending=False, inplace=True)
values = (averages['values'] * 100).round(2)
labels = averages['labels']

if __name__ == '__main__':
    import plotly.offline as py
    import plotly.graph_objs as go
    
    data = go.Bar(
                x=labels,
                y=values
                )
    layout = go.Layout(
                xaxis=dict(tickangle=-45),
                title='ORTG on Subsequent Possession by Possession Type'
                )
    fig = go.Figure(data=[data], layout=layout)
    fig = sankey.fig
    py.plot(fig, filename = 'basic-line.html', auto_open=True)
