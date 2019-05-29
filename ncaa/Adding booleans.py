#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import sqlite3 as sql


# In[8]:


conn = sql.connect("ncaa_pbp.db")

df = pd.read_sql("""
                SELECT
                    *
                From
                    "2017-2018"
                Limit
                    1000
                 """, conn)


# In[11]:


df['previous'] = df['EventType'].shift(1)
df['isAssisted'] = df['previous'] == 'assist'


# In[13]:


df.drop('previous', inplace=True, axis=1)


# In[16]:


df['prevID'] = df['EventPlayerID'].shift(1)


# In[18]:


df['test'] = df[df['isAssisted']]['prevID']


# In[20]:


df['prevID'] = df['test']
df.drop('test', axis=1, inplace=True)


# In[21]:


df


# In[ ]:




