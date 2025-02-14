### Create Internal Table in Big Query
- create table with schema
    ```sql
    CREATE OR REPLACE TABLE `starry-core-448108-u6.nyc_dataset.nyc_taxi`
    (
        VendorID INT64,
        tpep_pickup_datetime TIMESTAMP,
        tpep_dropoff_datetime TIMESTAMP,
        passenger_count INT64,
        trip_distance FLOAT64,
        RatecodeID INT64,
        store_and_fwd_flag STRING,
        PULocationID INT64,
        DOLocationID INT64,
        payment_type INT64,
        fare_amount FLOAT64,
        extra FLOAT64,
        mta_tax FLOAT64,
        tip_amount FLOAT64,
        tolls_amount FLOAT64,
        improvement_surcharge FLOAT64,
        total_amount FLOAT64,
        congestion_surcharge FLOAT64,
        Airport_fee FLOAT64
    );
    ```
- load data in table
    ```sql
    LOAD DATA INTO `starry-core-448108-u6.nyc_dataset.nyc_taxi`
    FROM FILES (
        format = 'PARQUET',
        uris = ['gs://shunnya-bucket/yellow_tripdata_2024*.parquet']
    );
    ```

### Create External Table in Big Query
```SQL
CREATE OR REPLACE EXTERNAL TABLE `starry-core-448108-u6.nyc_dataset.yellow_taxi_external`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://shunnya-bucket/yellow_tripdata_2024-*.parquet']
);
```

## Questions
#### count of records
```sql
SELECT count(*) as total_records FROM nyc_dataset.partitioned_taxi_table
```	
`Answer` : 20332093

#### Write a query to count the distinct number of PULocationIDs for the entire dataset on both the tables. What is the estimated amount of data that will be read when this query is executed on the External Table and the Table?


```sql
select count(distinct PULocationID) as pulocation_count FROM nyc_dataset.partitioned_taxi_table 
-- zero byte data processed

select count(distinct PULocationID) as pulocation_count FROM starry-core-448108-u6.nyc_dataset.yellow_taxi_external
-- 155.12 mb processed
-- pulocation_count => 262
```
`Answer` : 0 MB for the External Table and 155.12 MB for the Materialized Table

#### Write a query to retrieve the PULocationID from the table (not the external table) in BigQuery. Now write a query to retrieve the PULocationID and DOLocationID on the same table. Why are the estimated number of Bytes different?
```SQL
SELECT PULocationID FROM `nyc_dataset.partitioned_taxi_table`

SELECT PULocationID, DOLocationID FROM `nyc_dataset.partitioned_taxi_table`
```
`ANSWER`: BigQuery is a columnar database, and it only scans the specific columns requested in the query. Querying two columns (PULocationID, DOLocationID) requires reading more data than querying one column (PULocationID), leading to a higher estimated number of bytes processed.


#### How many records have a fare_amount of 0?
```SQL
SELECT COUNT(*) FROM `nyc_dataset.partitioned_taxi_table`
WHERE fare_amount = 0
```
`ANSWER`: 8333

#### What is the best strategy to make an optimized table in Big Query if your query will always filter based on tpep_dropoff_datetime and order the results by VendorID (Create a new table with this strategy)
```SQL
CREATE OR REPLACE TABLE nyc_dataset.optimised_query_table
PARTITION BY 
  DATE(tpep_dropoff_datetime)
CLUSTER BY
  VendorID
AS 
(SELECT * FROM  nyc_dataset.partitioned_taxi_table)
```
`ANSWER`: Partition by tpep_dropoff_datetime and Cluster on VendorID

#### Write a query to retrieve the distinct VendorIDs between tpep_dropoff_datetime 2024-03-01 and 2024-03-15 (inclusive)
- Use the materialized table you created earlier in your from clause and note the estimated bytes. Now change the table in the from clause to the partitioned table you created for question 5 and note the estimated bytes processed. What are these values?
```sql
-- non partitoned regular table
SELECT DISTINCT VendorID 
FROM 
  nyc_dataset.nyc_taxi
WHERE 
  tpep_dropoff_datetime BETWEEN '2024-03-01' AND '2024-03-15'

-- partioned and clustered table
SELECT DISTINCT VendorID 
FROM 
  `nyc_dataset.optimised_query_table`
WHERE 
  tpep_dropoff_datetime BETWEEN '2024-03-01' AND '2024-03-15'
```

##### Where is the data stored in the External Table you created?
`ANSWER`: GCP Bucket

#### It is best practice in Big Query to always cluster your data:
`ANSWER`: False

#### Write a SELECT count(*) query FROM the materialized table you created. How many bytes does it estimate will be read? Why?
```sql
SELECT count(*) AS CNT FROM `nyc_dataset.nyc_taxi`
```
`ANSWER`: Because it does not have to read any data.