import sqlite3
import pandas as pd
import re
import numpy as np

# Connect to the database
conn = sqlite3.connect('property.db')
c = conn.cursor()

#fetch all data from the database to a dataframe
df = pd.read_sql_query("SELECT * FROM properties", conn)

#convert price column to float remove all text and symbols
df['price'] = df['price'].str.replace(r'\D+', '', regex=True)

clean_df = pd.DataFrame(columns=df.columns)

for index, row in df.iterrows():
    try:
        # row['price'] = float(row['price'])
        # row['price'] = float(row['price'])
        row['price'] = np.nan
        clean_df = clean_df.concat(row, ignore_index=True)
        print(row['price'])
    except ValueError:
        row['price'] = np.nan
        print(row['price'])
print(df.head())

#drop all na from price column
df = df.dropna(subset=['price'])

df.to_csv('property.csv', index=False)
print(df.info())