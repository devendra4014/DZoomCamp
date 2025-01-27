from sqlalchemy import create_engine
import pandas as pd
from time import time

def main():
    try:
        user = "admin"
        password = "password"
        port = 5432
        host = "localhost"
        db = "nyc_database"

        # create connection with postgres
        engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

        # read data in pandas dataframe
        nyc = pd.read_csv("D:\ZoomCamp\docker-sql\data\green_tripdata_2019-10.csv")
        lookup = pd.read_csv("D:\ZoomCamp\docker-sql\data\zone_lookup.csv")

        # convert to datatime
        nyc.lpep_pickup_datetime = pd.to_datetime(nyc.lpep_pickup_datetime)
        nyc.lpep_dropoff_datetime = pd.to_datetime(nyc.lpep_dropoff_datetime)

        # create table in postgress for both dataframes
        nyc_table = "nyc_taxi"
        lookup_table = "lookup"

        nyc.head(n=0).to_sql(name=nyc_table, con=engine, if_exists='replace')
        lookup.head(n=0).to_sql(name=lookup_table, con=engine, if_exists='replace')

        # load data in both tables
        nyc.to_sql(name=nyc_table, con=engine, if_exists='append')
        lookup.to_sql(name=lookup_table, con=engine, if_exists='append')

        print("data in loaded into postgress database.")

    except Exception as ex:
        print(ex)

if __name__ == '__main__':
    main()