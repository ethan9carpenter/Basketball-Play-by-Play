import pandas as pd
import numpy as np
import sqlite3 as sql

conn = sql.connect("ncaa_pbp.db")
df = pd.read_sql("""
                SELECT
                    EventID, ElapsedSeconds, EventType, EventPlayerID
                From
                    "2017-2018"
                Limit
                    10000
                 """, conn, index_col='EventID')

df['isFT'] = (df['EventType'] == 'made1_free') | (df['EventType'] == 'miss1_free')
df = df[df['isFT']]

temp = df.shift(1)
temp = temp.join(df, lsuffix='_prev')
temp = temp.join(df.shift(-1), rsuffix='_2')
temp = temp.join(df.shift(-2), rsuffix='_3')
df = temp

df = df[df['ElapsedSeconds_prev'] != df['ElapsedSeconds']]


oneFT = df[(df['ElapsedSeconds'] != df['ElapsedSeconds_2']) &
           (df['ElapsedSeconds'] != df['ElapsedSeconds_3'])]
twoFT = df[(df['ElapsedSeconds'] == df['ElapsedSeconds_2']) &
           (df['ElapsedSeconds'] != df['ElapsedSeconds_3'])]
threeFT = df[(df['ElapsedSeconds'] == df['ElapsedSeconds_2']) &
           (df['ElapsedSeconds'] == df['ElapsedSeconds_3'])]


oneFT['numFT'] = 1
twoFT['numFT'] = 2
threeFT['numFT'] = 3

df.set_index(['ElapsedSeconds', 'EventType', 'EventPlayerID'], inplace=True)
df = df.join(oneFT[['ElapsedSeconds', 'EventType', 'EventPlayerID', 'numFT']].\
             set_index(['ElapsedSeconds', 'EventType', 'EventPlayerID']))
df = df.join(twoFT[['ElapsedSeconds', 'EventType', 'EventPlayerID', 'numFT']].\
             set_index(['ElapsedSeconds', 'EventType', 'EventPlayerID']), rsuffix='_0')
df = df.join(threeFT[['ElapsedSeconds', 'EventType', 'EventPlayerID', 'numFT']].\
             set_index(['ElapsedSeconds', 'EventType', 'EventPlayerID']), rsuffix='_1')




df['numFT'] = df['numFT'].fillna(0)
df['numFT_0'] = df['numFT_0'].fillna(0)
df['numFT_1'] = df['numFT_1'].fillna(0)
df['numFT'] = df['numFT'] + df['numFT_0'] + df['numFT_1']

orig = pd.read_sql("""
                SELECT
                    EventID, ElapsedSeconds, EventType, EventPlayerID
                From
                    "2017-2018"
                Limit
                    10000
                 """, conn)
orig['isFT'] = (orig['EventType'] == 'made1_free') | (orig['EventType'] == 'miss1_free')
orig.set_index(['ElapsedSeconds', 'EventPlayerID', 'isFT'], inplace=True)

df.reset_index(inplace=True)
df.set_index(['ElapsedSeconds', 'EventPlayerID', 'isFT'], inplace=True)

merged = orig.join(df, rsuffix='_')
merged.reset_index(inplace=True)

merged = merged[['ElapsedSeconds', 'EventPlayerID', 'isFT', 'EventType', 'numFT', 'EventID']]
merged.set_index('EventID', inplace=True)
