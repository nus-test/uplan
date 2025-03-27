# The steps to run TPC-H benchmark on TiDB



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
Copy all `*.tbl` files into the current folder, and run following commands to populate the database.
```
$ mysql -h 127.0.0.1 -P 4000 -u root -D test < dss.sql
$ mysql -h 127.0.0.1 -P 4000 -u root --local-infile=1 -D tpch < load.sql
```  

## 4. Run the queries.
```