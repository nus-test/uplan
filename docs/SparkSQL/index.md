---
title: SparkSQL
layout: default
has_children: true
---

# Overview
[Spark](https://spark.apache.org/) is a multi-language execution engine for large-scale data analytics. [Spark SQL](https://spark.apache.org/sql/) is a SQL interface of Spark for working with structured data.

SparkSQL supports a text format of query plans in the shell and a graph format of query plans in the official [Web UI](https://spark.apache.org/docs/3.0.0-preview/web-ui.html#sql-metrics).

## Example
```sql
CREATE TABLE t0 (c0 INT)
CREATE TABLE t1 (c0 INT)
CREATE TABLE t2 (c0 INT)
INSERT INTO t0 VALUES (1),(2),(3),(4),(5),(6),(7),(8),(9),(10)
INSERT INTO t2 VALUES (1),(2),(3),(4),(5),(6),(7),(8),(9),(10)
```

### Text format of the query plan

```sql
EXPLAIN SELECT t1.c0 FROM t0 JOIN t1 ON t0.c0 = t1.c0 WHERE t0.c0 < 100 GROUP BY t1.c0 UNION SELECT c0 FROM t2 WHERE c0 < 10
```

The words followed by `+-` are operations, and others are properties. 

```shell
|== Physical Plan ==
AdaptiveSparkPlan isFinalPlan=false
+- HashAggregate(keys=[c0#90], functions=[])
   +- Exchange hashpartitioning(c0#90, 200), ENSURE_REQUIREMENTS, [plan_id=271]
      +- HashAggregate(keys=[c0#90], functions=[])
         +- Union
            :- HashAggregate(keys=[c0#90], functions=[])
            :  +- Exchange hashpartitioning(c0#90, 200), ENSURE_REQUIREMENTS, [plan_id=266]
            :     +- HashAggregate(keys=[c0#90], functions=[])
            :        +- Project [c0#90]
            :           +- BroadcastHashJoin [c0#89], [c0#90], Inner, BuildLeft, false
            :              :- BroadcastExchange HashedRelationBroadcastMode(List(cast(input[0, int, false] as bigint)),false), [plan_id=261]
            :              :  +- Filter (isnotnull(c0#89) AND (c0#89 < 100))
            :              :     +- Scan hive default.t0 [c0#89], HiveTableRelation [`default`.`t0`, org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe, Data Cols: [c0#89], Partition Cols: []]
            :              +- Filter ((c0#90 < 100) AND isnotnull(c0#90))
            :                 +- Scan hive default.t1 [c0#90], HiveTableRelation [`default`.`t1`, org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe, Data Cols: [c0#90], Partition Cols: []]
            +- Filter (isnotnull(c0#91) AND (c0#91 < 10))
               +- Scan hive default.t2 [c0#91], HiveTableRelation [`default`.`t2`, org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe, Data Cols: [c0#91], Partition Cols: []]

```




## References
* [Spark Web UI](https://spark.apache.org/docs/3.0.0-preview/web-ui.html#sql-metrics)
* [Spark SQL](https://spark.apache.org/docs/3.4.0/sql-ref-syntax-qry-explain.html)
* [Spark Github Commit: f4e53fa9](https://github.com/apache/spark/tree/f4e53fa9)