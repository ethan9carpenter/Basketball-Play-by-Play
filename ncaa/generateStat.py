from ncaa import analysis
from ncaa.load_data import load_clean
from ncaa.analysis.analyze import apply_grouping
import sqlite3 as sql
import warnings
import pandas as pd
import numpy as np

warnings.filterwarnings('ignore')
power5 = ['acc']

year = 2016
conn = sql.connect("ncaa_pbp.db")
#df = load_data(year, conn, 100, '*')
#df = cleanData(df)
df = load_clean(year, conn, limit=None)

df = analysis.prep(df)
conferences = pd.read_sql("SELECT ConfAbbrev, TeamID FROM TeamConferences WHERE Season ={year}".format(year=year), conn)

df = pd.merge(df, conferences, 'left', 'TeamID', suffixes=['', '_'])
df = df[['PlayerName', 'EventPlayerID', 'TeamID', 'TeamName', 'EventType', 'PointValue_sbsq', 'ConfAbbrev']]
df = df[df['ConfAbbrev'].isin(power5)]

labelCols = []
groupingCols = ['PlayerName', 'EventPlayerID', 'TeamID', 'TeamName', 'ConfAbbrev'] + labelCols
teamAvg = apply_grouping(df, ['TeamID']+labelCols)['AveragePoints']
playerData = apply_grouping(df, groupingCols)

df = None

playerData.reset_index(inplace=True)
playerData.set_index(['PlayerName', 'TeamID']+labelCols, inplace=True)
playerData['AveragePoints'] -= teamAvg
playerData.reset_index(inplace=True, level='TeamID')
playerData = playerData[['TeamName', 'ConfAbbrev', 'AveragePoints', 'Count']]
playerData['Total'] = playerData['AveragePoints'] * playerData['Count']
playerData = playerData.groupby(['PlayerName', 'TeamName', 'ConfAbbrev']).sum()
playerData['AveragePoints'] = playerData['Total'] / playerData['Count']
playerData = playerData[playerData['Count'] > 400]
#playerData['Rating'] = playerData['Total'] * np.abs(playerData['AveragePoints'])

print(playerData.sort_values('AveragePoints', ascending=False).reset_index(level='ConfAbbrev', drop=True).reset_index(level='TeamName'))