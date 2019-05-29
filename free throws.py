#!/usr/bin/env python
# coding: utf-8

# In[240]:


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
                 """, conn)
df.set_index('EventID', inplace=True)


# In[241]:


df['isFT'] = (df['EventType'] == 'made1_free') | (df['EventType'] == 'miss1_free')

df = df[df['isFT']]


# In[242]:


temp = df.shift(-1)
temp2 = df.shift(-2)
temp3 = df.shift(1)
df = temp3.join(df, lsuffix='_prev')
df = df.join(temp, rsuffix='_2')
df = df.join(temp2, rsuffix='_3')


# In[243]:


df


# In[244]:


df = df[(df['ElapsedSeconds_prev'] != df['ElapsedSeconds'])]
#df.drop(df.columns[:3], axis=1, inplace=True)


# In[245]:


oneFT = df[(df['ElapsedSeconds'] != df['ElapsedSeconds_2']) &
           (df['ElapsedSeconds'] != df['ElapsedSeconds_3'])]
twoFT = df[(df['ElapsedSeconds'] == df['ElapsedSeconds_2']) &
           (df['ElapsedSeconds'] != df['ElapsedSeconds_3'])]
threeFT = df[(df['ElapsedSeconds'] == df['ElapsedSeconds_2']) &
           (df['ElapsedSeconds'] == df['ElapsedSeconds_3'])]


# In[246]:


twoFT


# In[247]:


oneFT['numFT'] = 1
twoFT['numFT'] = 2
threeFT['numFT'] = 3


# In[249]:


df.set_index(['ElapsedSeconds', 'EventType', 'EventPlayerID'], inplace=True)
df = df.join(oneFT[['ElapsedSeconds', 'EventType', 'EventPlayerID', 'numFT']].             set_index(['ElapsedSeconds', 'EventType', 'EventPlayerID']))
df = df.join(twoFT[['ElapsedSeconds', 'EventType', 'EventPlayerID', 'numFT']].             set_index(['ElapsedSeconds', 'EventType', 'EventPlayerID']), rsuffix='_0')
df = df.join(threeFT[['ElapsedSeconds', 'EventType', 'EventPlayerID', 'numFT']].             set_index(['ElapsedSeconds', 'EventType', 'EventPlayerID']), rsuffix='_1')


# In[250]:


df['numFT'] = df['numFT'].fillna(0)
df['numFT_0'] = df['numFT_0'].fillna(0)
df['numFT_1'] = df['numFT_1'].fillna(0)
df['numFT'] = df['numFT'] + df['numFT_0'] + df['numFT_1']


# In[251]:


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


# In[252]:


df.reset_index(inplace=True)
df.set_index(['ElapsedSeconds', 'EventPlayerID', 'isFT'], inplace=True)


# In[253]:


merged = orig.join(df, rsuffix='_')
merged.reset_index(inplace=True)

merged = merged[['ElapsedSeconds', 'EventPlayerID', 'isFT', 'EventType', 'numFT', 'EventID']]
merged.set_index('EventID', inplace=True)


# In[254]:


merged[merged['numFT'] >= 1]


# In[ ]:





# In[ ]:




