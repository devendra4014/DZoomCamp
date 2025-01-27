# NYC Taxi data Ingestion in Postgress and Terraforming
This project involves setting up a Dockerized PostgreSQL database for NYC taxi data, creating a data pipeline, performing analysis, and deploying infrastructure using Terraform. 
The README provides step-by-step instructions and queries for various tasks.

## Docker Setup
### PostgreSQL Container
Run the following Docker command to start a PostgreSQL container:
```sh
docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="nyc_taxi" \
  -v ./postgres_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  --network=pg-network \
  --name pg-database \
  postgres:15
```
### pgAdmin Container
Launch a pgAdmin container with the following command:
```sh
docker run -it \
    -e PGADMIN_DEFAULT_EMAIL="example@admin.com" \
    -e PGADMIN_DEFAULT_PASSWORD="default" \
    -p 8080:80 \
    --network=pg-network \
    --name pg-admin \
    dpage/pgadmin4
```
### Build docker image 
- build docker image with python 3.9
- add dependencies required to install in requirements.txt file
- execute below command to build image
  ```sh
    docker build -t my-python-docker .
  ```
- To run the container:
  ```sh
    docker run -it my-python-docker
  ```
- check pip version
  ```sh
  root@b2397db96924:/# pip --version
  pip 24.3.1 from /usr/local/lib/python3.12/site-packages/pip (python 3.12)
  ```
## Running Docker-Compose
- run this below docker compose file 
[docker-compose file](docker_sql/docker-compose.yaml)
- cd to location where docker-compose.yaml file resides and execute below command
  ```sh
   docker-compose up -d
  ```
# gcp Terraform setup
go to => [terraform folder](terraform), here you will find required files to create resources in GCP using terraform.

### create public private key
```
ssh-keygen -t rsa -b 4096 -f gcp
```

## create config
- create a config file at `touch ~/.shh/config`
- open file in vs code `code config`
- add below details to file
  ```sh
    # VM Connection Details
    Host zoomcamp
        HostName vm-add-ress  # Replace with your VM's IP address
        User devendra          # Replace with your VM username
        Port 22             # Standard SSH port
        IdentityFile C:/Users/Devendra/.ssh/gcp  # Path to your private SSH key 
        
    # Optional settings for specific commands 
    #  -  "StrictHostKeyChecking no" to bypass host key checking 
    #  -  "ConnectTimeout 5" to set a timeout for connection attempts 
  ```

## install terraform
- create bin directory
```sh
sudo apt update
cd ~
mkdir bin
cd bin
```
- download terraform binary using wget
```sh
wget https://releases.hashicorp.com/terraform/1.10.4/terraform_1.10.4_linux_386.zip
sudo apt-get install unzip
unzip terraform_1.10.4_linux_386.zip
rm terraform_1.10.4_linux_386.zip
```
- open bashrc file
```sh
cd ~
vim .bashrc
```
 
- add path to bashrc file
```sh
export PATH="${HOME}/bin:${PATH}"
```
- logout and again login or execute below command
```sh
source .bashrc
```

## Analysis Queries
### Trip Segmentation Count
During the period of October 1st 2019 (inclusive) and November 1st 2019 (exclusive), how many trips, respectively, happened:
- Up to 1 mile
  ```sql
  Select count(*) from nyc_taxi 
  where
    lpep_pickup_datetime >= '2019-10-01' AND 
    lpep_dropoff_datetime < '2019-11-01' AND 
    trip_distance <=1
  ```
- In between 1 (exclusive) and 3 miles (inclusive)
```sql
Select count(*) from nyc_taxi 
where
  lpep_pickup_datetime >= '2019-10-01' AND 
	lpep_dropoff_datetime < '2019-11-01' AND 
	trip_distance <= 3 and trip_distance > 1
```
- In between 3 (exclusive) and 7 miles (inclusive)
  ```sql
  Select count(*) from nyc_taxi 
  where
    lpep_pickup_datetime >= '2019-10-01' AND 
	  lpep_dropoff_datetime < '2019-11-01' AND 
	  trip_distance <= 7 and trip_distance > 3
  ```
- In between 7 (exclusive) and 10 miles (inclusive),

  ```sql
    Select count(*) from nyc_taxi 
    where
      lpep_pickup_datetime >= '2019-10-01' AND 
      lpep_dropoff_datetime < '2019-11-01' AND 
      trip_distance <= 10 and trip_distance > 7
  ```
- Over 10 miles
  ```sql
    Select count(*) from nyc_taxi 
    where
      lpep_pickup_datetime >= '2019-10-01' AND 
      lpep_dropoff_datetime < '2019-11-01' AND 
      trip_distance > 10
  ```
## Longest trip for each day
Which was the pick up day with the longest trip distance? Use the pick up time for your calculations.
```sql
Select DATE(lpep_pickup_datetime), 
	    MAX(trip_distance) as mx  
    from nyc_taxi
    GROUP BY DATE(lpep_pickup_datetime)
    order by 2 desc limit 1
```

## Three biggest pickup zones
Which were the top pickup locations with over 13,000 in total_amount (across all trips) for 2019-10-18?
```sql
Select b."Zone", SUM(total_amount)
    from nyc_taxi as a
    inner join lookup as b
        on b."LocationID" = a."PULocationID"
    WHERE DATE(lpep_pickup_datetime) = '2019-10-18'
    GROUP BY b."Zone"
    ORDER BY 2 desc LIMIT 3
```
## Largest tip
For the passengers picked up in Ocrober 2019 in the zone name "East Harlem North" which was the drop off zone that had the largest tip?
```sql
WITH cte AS (
        Select a."DOLocationID",
            a."PULocationID", tip_amount,
            DENSE_RANK() OVER (PARTITION BY b."Zone" order by tip_amount desc) as rnk
        from nyc_taxi as a
        inner join lookup as b
            on b."LocationID" = a."PULocationID"
        WHERE 
            EXTRACT(MONTH FROM lpep_pickup_datetime) = '10' AND 
            EXTRACT(YEAR FROM lpep_pickup_datetime) = '2019' AND
            b."Zone" = 'East Harlem North'
    )
    select b."Zone" from cte as a
    inner join lookup as b
        on b."LocationID" = a."DOLocationID"
    where rnk = 1
```