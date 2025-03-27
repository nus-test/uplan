---
title: Properties
layout: default
parent: SparkSQL
---



We have not found clear definitions of properties in the official document and source code, so we examined the properties listed in [Spark Web UI](https://spark.apache.org/docs/3.0.0-preview/web-ui.html#sql-metrics), and copied their descriptions as follows.


| Property                         | Category    | Reference                                                                   | Description                                                                       |
| -------------------------------- | ----------- | --------------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| avg hash probe bucket list iters | Cost        | [Link](https://spark.apache.org/docs/3.0.0-preview/web-ui.html#sql-metrics) | the average bucket list iterations per lookup during aggregation                  |
| data size                        | Cardinality | [Link](https://spark.apache.org/docs/3.0.0-preview/web-ui.html#sql-metrics) | Estimated size of broadcast/shuffled/collected data of the operator               |
| data size of build side          | Cost        | [Link](https://spark.apache.org/docs/3.0.0-preview/web-ui.html#sql-metrics) | the size of the built hash map                                                    |
| fetch wait time                  | Cost        | [Link](https://spark.apache.org/docs/3.0.0-preview/web-ui.html#sql-metrics) | the time spent on fetching data (local and remote)                                |
| local blocks read                | Cardinality | [Link](https://spark.apache.org/docs/3.0.0-preview/web-ui.html#sql-metrics) | the number of blocks read locally                                                 |
| local bytes read                 | Cardinality | [Link](https://spark.apache.org/docs/3.0.0-preview/web-ui.html#sql-metrics) | the number of bytes read locally                                                  |
| metadata time                    | Cost        | [Link](https://spark.apache.org/docs/3.0.0-preview/web-ui.html#sql-metrics) | the time spent on getting metadata like the number of partitions, number of files |
| number of output rows            | Cardinality | [Link](https://spark.apache.org/docs/3.0.0-preview/web-ui.html#sql-metrics) | the number of output rows of the operator                                         |
| peak memory                      | Cost        | [Link](https://spark.apache.org/docs/3.0.0-preview/web-ui.html#sql-metrics) | the peak memory usage in the operator                                             |
| records read                     | Cardinality | [Link](https://spark.apache.org/docs/3.0.0-preview/web-ui.html#sql-metrics) | the number of read records                                                        |
| remote blocks read               | Cardinality | [Link](https://spark.apache.org/docs/3.0.0-preview/web-ui.html#sql-metrics) | the number of blocks read remotely                                                |
| remote bytes read                | Cardinality | [Link](https://spark.apache.org/docs/3.0.0-preview/web-ui.html#sql-metrics) | the number of bytes read remotely                                                 |
| remote bytes read to disk        | Cardinality | [Link](https://spark.apache.org/docs/3.0.0-preview/web-ui.html#sql-metrics) | the number of bytes read from remote to local disk                                |
| scan time                        | Cost        | [Link](https://spark.apache.org/docs/3.0.0-preview/web-ui.html#sql-metrics) | the time spent on scanning data                                                   |
| shuffle bytes written            | Cardinality | [Link](https://spark.apache.org/docs/3.0.0-preview/web-ui.html#sql-metrics) | the number of bytes written                                                       |
| shuffle records written          | Cardinality | [Link](https://spark.apache.org/docs/3.0.0-preview/web-ui.html#sql-metrics) | the number of records written                                                     |
| shuffle write time               | Cardinality | [Link](https://spark.apache.org/docs/3.0.0-preview/web-ui.html#sql-metrics) | the time spent on shuffle writing                                                 |
| sort time                        | Cost        | [Link](https://spark.apache.org/docs/3.0.0-preview/web-ui.html#sql-metrics) | the time spent on sorting                                                         |
| spill size                       | Cost        | [Link](https://spark.apache.org/docs/3.0.0-preview/web-ui.html#sql-metrics) | number of bytes spilled to disk from memory in the operator                       |
| time in aggregation build        | Cost        | [Link](https://spark.apache.org/docs/3.0.0-preview/web-ui.html#sql-metrics) | the time spent on aggregation                                                     |
| time to build hash map           | Cost        | [Link](https://spark.apache.org/docs/3.0.0-preview/web-ui.html#sql-metrics) | the time spent on building a hash map                                             |
| time to collect                  | Cost        | [Link](https://spark.apache.org/docs/3.0.0-preview/web-ui.html#sql-metrics) | the time spent on collecting data                                                 |

## References
* [Spark Web UI](https://spark.apache.org/docs/3.0.0-preview/web-ui.html#sql-metrics)
* [Spark SQL](https://spark.apache.org/docs/3.4.0/sql-ref-syntax-qry-explain.html)
* [Spark Github Commit: f4e53fa9](https://github.com/apache/spark/tree/f4e53fa9)