from ncaa import analysis
from ncaa.load_data import load_clean
from ncaa.analysis.analyze import apply_grouping
import sqlite3 as sql
import warnings
import pandas as pd

warnings.filterwarnings('ignore')
power5 = ['acc', 'big_ten', 'big_twelve', 'sec', 'pac_twelve']

year = 2012
conn = sql.connect("ncaa_pbp.db")
#df = load_data(year, conn, 100, '*')
#df = cleanData(df)
df = load_clean(year, conn, limit=None)

df = analysis.prep(df)
conferences = pd.read_sql("SELECT ConfAbbrev, TeamID FROM TeamConferences WHERE Season ={year}".format(year=year), conn)

df = pd.merge(df, conferences, 'left', 'TeamID', suffixes=['', '_'])
df = df[['PlayerName', 'EventPlayerID', 'TeamID', 'TeamName', 'EventType', 'PointValue_sbsq', 'ConfAbbrev']]
df = df[df['ConfAbbrev'].isin(power5)]

labelCols = ['PlayerName', 'EventType']
groupingCols = ['EventPlayerID', 'TeamID', 'TeamName', 'ConfAbbrev'] + labelCols
teamAvg = apply_grouping(df, ['TeamID'])['AveragePoints']
playerData = apply_grouping(df, groupingCols)
df = None

playerData.reset_index(inplace=True)
playerData.set_index(['TeamID']+labelCols, inplace=True)
playerData['AveragePoints'] -= teamAvg
playerData.reset_index(inplace=True, level=0)
playerData = playerData[['TeamName', 'ConfAbbrev', 'AveragePoints', 'Count']]
playerData['Total'] = playerData['AveragePoints'] * playerData['Count']
playerData = playerData.groupby(['PlayerName', 'TeamName', 'ConfAbbrev']).sum()
playerData['AveragePoints'] = playerData['Total'] / playerData['Count']
#playerData = playerData[playerData['Count'] > 450]
playerData['Rating'] = playerData['Total'] * playerData['AveragePoints']

print(playerData.sort_values('Rating', ascending=False).reset_index(level=2, drop=True).drop('Total', axis=1))