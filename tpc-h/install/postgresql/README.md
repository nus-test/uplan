# The steps to run TPC-H benchmark on PostgreSQL



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

Each line requires to remove the last '|' in order to be compatible with PostgreSQL.
```
sed -i 's/|$//' *.tbl
```

All data files have to be copied to **/tmp** folder in order to be accessible by PostgreSQL.
```
cp *.tbl /tmp
```

## 3. Populate the database.
Connect to PostgreSQL to create database.  
```
$ psql
$ psql> CREATE DATABASE tpch;
```  

Reconnect to PostgreSQL to enter the database.
```
$ psql> \q
$ psql -d tpc-h
```

Execute the sql file to create the schemas.
``` 
\i dss.ddl;
```

Populate tables with generated dummy data.  
```
Copy region FROM '/tmp/region.tbl' WITH DELIMITER AS '|';
Copy nation FROM '/tmp/nation.tbl' WITH DELIMITER AS '|';
Copy part FROM '/tmp/part.tbl' WITH DELIMITER AS '|';
Copy supplier FROM '/tmp/supplier.tbl' WITH DELIMITER AS '|';
Copy customer FROM '/tmp/customer.tbl' WITH DELIMITER AS '|';
Copy lineitem FROM '/tmp/lineitem.tbl' WITH DELIMITER AS '|';
Copy partsupp FROM '/tmp/partsupp.tbl' WITH DELIMITER AS '|';
Copy orders FROM '/tmp/orders.tbl' WITH DELIMITER AS '|';
```  

Replace the **dss.ri** files with the ones provided in this repository.

Alter the schema dependencies.
```
\i dss.ri;
```

## 4. Run the queries.
```