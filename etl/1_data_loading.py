import os
import pandas as pd
from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    String,
    Integer,
)

from sqlalchemy.orm import sessionmaker

# Define database connection
engine = create_engine('sqlite:///../db/marathon.db')

# Define metadata
metadata = MetaData()

# Define table schema
table_name = 'marathon_results'
table = Table(table_name, metadata,
              Column('id', Integer, primary_key=True, autoincrement=True),
              Column('bib', Integer),
              Column('name', String),
              Column('age', Integer),
              Column('gender', String),
              Column('city', String),
              Column('state', String),
              Column('country', String),
              Column('citizenship', String),
              Column('time_at_5_kilometers', String),
              Column('time_at_10_kilometers', String),
              Column('time_at_15_kilometers', String),
              Column('time_at_20_kilometers', String),
              Column('time_half_marathon_at_21_kilometers', String),
              Column('time_at_25_kilometers', String),
              Column('time_at_30_kilometers', String),
              Column('time_at_35_kilometers', String),
              Column('time_at_40_kilometers', String),
              Column('running_pace', String),
              Column('official_time_full_marathon_at_42_kilometers', String),
              Column('place_overall', String),
              Column('place_by_gender', Integer),
              Column('place_by_division_age_group', Integer),
              Column('marathon_name', String),
              Column('marathon_year', Integer),
              Column('marathon_city', String),
              )

# Create table in the database
metadata.create_all(engine)

# Directory containing CSV files
csv_directory = '../raw_data'

dfs = []
# Iterate over CSV files in the directory
for filename in os.listdir(csv_directory):
    if filename.endswith('.csv'):
        # Read CSV file into a DataFrame
        filepath = os.path.join(csv_directory, filename)
        df = pd.read_csv(filepath)
        df.columns = ['orig_index', 'bib', 'name', 'age', 'gender', 'city', 'state', 'country','citizenship', 'empty', 'time_at_5_kilometers', 'time_at_10_kilometers', 'time_at_15_kilometers', 'time_at_20_kilometers', 'time_half_marathon_at_21_kilometers', 'time_at_25_kilometers','time_at_30_kilometers', 'time_at_35_kilometers', 'time_at_40_kilometers', 'running_pace', 'projected_time', 'official_time_full_marathon_at_42_kilometers', 'place_overall','place_by_gender', 'place_by_division_age_group']
        # Extract marathon name and year from filename
        marathon_name, marathon_year = filename.split('.')[0].split('_')
        
        # Add columns for marathon name and year
        df['marathon_name'] = marathon_name
        df['marathon_year'] = int(marathon_year)
        df['marathon_city'] = 'Boston'
        
        # Append DataFrame to the list
        dfs.append(df)
        
        # Concatenate all DataFrames into one
combined_df = pd.concat(dfs, ignore_index=True)
combined_df = combined_df.drop(columns=['orig_index', 'projected_time', 'empty'])

# Define a function to load data from a CSV file into the database
def load_data_to_table(engine, table, df):
    Session = sessionmaker(bind=engine)
    session = Session()
    
    df.to_sql(table.name, engine, if_exists='append', index=False)
    
    session.commit()
    session.close()


load_data_to_table(engine, table, combined_df)
