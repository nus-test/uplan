# Artifacts for Query Plan Study

This repository contains the artifact for the ICDE'25 paper ["Towards a Unified Query Plan Representation"](https://arxiv.org/pdf/2408.07857v2).

Our artifact includes 
1) a website that allows further studying our results and raw data, 
2) the reusable library described in Section 4,
3) the visualization application described in Application 2, Section 5,
4) the benchmarking application described in Application 3, Section 5.

## Structure
* [sqlancer_uplan/](sqlancer_uplan/): Contains the integrated SQLancer and UPlan.
* [docs/](docs/): Contains the study results and the second application: visualization, both of which have been deployed on https://nus-test.github.io/uplan.
* [tpc-h/](tpc-h/): Contains the scripts to configure TPC-H benchmark and experimental data for the third application: benchmarking.
* [wdbench](wdbench/): Contains the scripts to configure the WDBench benchmark and experimental data for the third application: benchmarking.
* [ycsb](ycsb/): Contains the scripts to configure the YCSB benchmark and experimental data for the third application: benchmarking.

* Other python files are the reusable library **UPlan** for converting query plans into the unified representation. Please see below for more details.

## UPlan
To transfer an original TiDB query plan into the unified representation, run:
```bash
python3 main.py -t tidb -i tpc-h/queryplan_raw/1.tidb
```
The unified query plan in the text format will be printed on the console.


## Testing
1. Compile the SQLancer with UPlan

```bash
cd sqlancer_uplan
mvn -B package -DskipTests=true
cd target
```

2. Start a DBMS server in a terminal
```bash
# For example, start a MySQL server
docker run -it -p 3306:3306 -e MYSQL_ROOT_PASSWORD=root mysql
# Start a PostgreSQL server
docker run -p 5432:5432 -e POSTGRES_PASSWORD=root -it postgres:14.7
# Start a TiDB server
docker run -it -p 4000:4000 pingcap/tidb:v6.5.1
```

**Note**: SQLancer requires a database `test` for PostgreSQL. Before running SQLancer, please login to the PostgreSQL server and create the database:
```bash
psql -U postgres -h 127.0.0.1 -p 5432 -c 'CREATE DATABASE test;'
```

3. Then start another terminal to run the SQLancer with UPlan
```bash
# Start MySQL Testing with QPG
java -jar sqlancer-2.0.0.jar --num-threads 1 --uplan /path/to/unifiedqueryplan --host 127.0.0.1 --username root --password root --port 3306 --qpg-enable true mysql --oracle TLP_WHERE
# Start MySQL Testing with CERT
java -jar sqlancer-2.0.0.jar --num-threads 1 --uplan /path/to/unifiedqueryplan --host 127.0.0.1 --username root --password root --port 3306 mysql --oracle CERT
# Start PostgreSQL Testging with QPG
java -jar sqlancer-2.0.0.jar --num-threads 1 --uplan /path/to/unifiedqueryplan --host 127.0.0.1 --username postgres --password root --port 5432 --qpg-enable true postgres --oracle QUERY_PARTITIONING
# Start PostgreSQL Testing with CERT
java -jar sqlancer-2.0.0.jar --num-threads 1 --uplan /path/to/unifiedqueryplan --host 127.0.0.1 --username postgres --password root --port 5432 postgres --oracle CERT
# Start TiDB Testing with QPG
java -jar sqlancer-2.0.0.jar --num-threads 1 --uplan /path/to/unifiedqueryplan --host 127.0.0.1 --username root --password '' --qpg-enable true --port 4000 tidb --oracle WHERE
# Start TiDB Testing with CERT
java -jar sqlancer-2.0.0.jar --num-threads 1 --uplan /path/to/unifiedqueryplan --host 127.0.0.1 --username root --password '' --port 4000 tidb --oracle CERT
```

In above commands, `/path/to/unifiedqueryplan` needs to be update to the real folder of `main.py`, which is the root of this repository.

### Code reference
Through UPlan, we implemented the unified QPG and CERT (main.py: Line 40-45), so different DBMSs can reuse the same implementation, instead of implementing customized QPG and CERT for each DBMS.

In sqlancer_uplan/src/sqlancer/common/DBMSCommon.java, we implemented an interface `parseQueryPlan()` at line 74 to call the unified implementation of QPG and CERT. In this way, we can easily apply QPG and CERT to different DBMSs.

## Found Bugs
Please see `sqlancer_uplan/bugs.json`.