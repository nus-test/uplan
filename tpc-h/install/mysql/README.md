# The steps to run TPC-H benchmark on MySQL



## 1. Download the TPC-H benchmark and modify makefile according to specific steps for each DBMS.
Unzip the downloaded file
Navigate through the command line to DBGEN folder  
```
$ cd dbgen/
```  

Replace the **makefile** and **tpcd.h** files with the ones provided in this repository.  

Then build the tpc-h benchmark with the following command.  
```
$ make
```

## 2. Generate the files for population. 

Generate 0.1GB of dummy data.
```
$ ./dbgen -s 0.1
```  
Then there are several data files ending with .tbl will be generated in the current folder.

## 3. Populate the database.
Connect to MySQL with permission to reach local files, create database and connect to schema.  
```
$ mysql -u root -p --local-infile
$ mysql> SET GLOBAL local_infile = 1;
```  

Replace the **dss.ddl** and **dss.ri** files with the ones provided in this repository.

Create the schemas.
```
source dss.ddl;
```

Populate tables with generated dummy data.  
```
LOAD DATA LOCAL INFILE 'customer.tbl' INTO TABLE CUSTOMER FIELDS TERMINATED BY '|';
LOAD DATA LOCAL INFILE 'orders.tbl' INTO TABLE ORDERS FIELDS TERMINATED BY '|';
LOAD DATA LOCAL INFILE 'lineitem.tbl' INTO TABLE LINEITEM FIELDS TERMINATED BY '|';
LOAD DATA LOCAL INFILE 'nation.tbl' INTO TABLE NATION FIELDS TERMINATED BY '|';
LOAD DATA LOCAL INFILE 'partsupp.tbl' INTO TABLE PARTSUPP FIELDS TERMINATED BY '|';
LOAD DATA LOCAL INFILE 'part.tbl' INTO TABLE PART FIELDS TERMINATED BY '|';
LOAD DATA LOCAL INFILE 'region.tbl' INTO TABLE REGION FIELDS TERMINATED BY '|';
LOAD DATA LOCAL INFILE 'supplier.tbl' INTO TABLE SUPPLIER FIELDS TERMINATED BY '|';
```  

Alter the schema dependencies.
```
source dss.ri;
```

## 4. Run the queries.
```