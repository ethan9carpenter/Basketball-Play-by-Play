import sqlite3
import pandas as pd

conn = sqlite3.connect('ncaa_pbp.db')

for year in range(2010, 2020):
    fileName = 'ncaa/mens-machine-learning-competition-2019/PlayByPlay_{}/Events_{}.csv'.format(year, year)
    df = pd.read_csv(fileName)
    df.to_sql('{}-{}'.format(year-1, year), conn)
    print(year)
