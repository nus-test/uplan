---
title: TiDB
layout: default
has_children: true
---

# Overview

[TiDB](https://www.pingcap.com/tidb/) is an open-source distributed relational database management system. It is designed to process both OLTP (Online Transaction Processing) and OLAP (Online Analytical Processing) workloads.

TiDB supports representating query plans in [text, table, JSON, and dot graph formats](https://docs.pingcap.com/tidb/dev/sql-statement-explain) in its shell. 


## Example
```sql
CREATE TABLE t0 (c0 INT);
CREATE TABLE t1 (c0 INT);
CREATE TABLE t2 (c0 INT PRIMARY KEY);
INSERT INTO t0 VALUES (1),(2),(3),(4),(5),(6),(7),(8),(9),(10);
INSERT INTO t2 VALUES (1),(2),(3),(4),(5),(6),(7),(8),(9),(10);
```

### Table format of the query plan

```sql
EXPLAIN SELECT t1.c0 FROM t0 JOIN t1 ON t0.c0 = t1.c0
  WHERE t0.c0 < 100 GROUP BY t1.c0
  UNION SELECT c0 FROM t2 WHERE c0 < 10;
```

The column `id` includes operations, and other columns include properties of associated operations.

| id                                   | estRows  | task      | access object | operator info                                               |
|--------------------------------------|----------|-----------|---------------|-------------------------------------------------------------|
| HashAgg_16                           | 6.82     | root      |               | group by:Column#6, funcs:firstrow(Column#6)->Column#6       |
| └─Union_17                           | 7.49     | root      |               |                                                             |
|   ├─HashAgg_19                       | 4.15     | root      |               | group by:test.t1.c0, funcs:firstrow(test.t1.c0)->test.t1.c0 |
|   │ └─HashJoin_21                    | 4.15     | root      |               | inner join, equal:[eq(test.t0.c0, test.t1.c0)]              |
|   │   ├─TableReader_24(Build)        | 3.32     | root      |               | data:Selection_23                                           |
|   │   │ └─Selection_23               | 3.32     | cop[tikv] |               | lt(test.t0.c0, 100), not(isnull(test.t0.c0))                |
|   │   │   └─TableFullScan_22         | 10.00    | cop[tikv] | table:t0      | keep order:false, stats:pseudo                              |
|   │   └─TableReader_27(Probe)        | 3323.33  | root      |               | data:Selection_26                                           |
|   │     └─Selection_26               | 3323.33  | cop[tikv] |               | lt(test.t1.c0, 100), not(isnull(test.t1.c0))                |
|   │       └─TableFullScan_25         | 10000.00 | cop[tikv] | table:t1      | keep order:false, stats:pseudo                              |
|   └─TableReader_30                   | 4.17     | root      |               | data:TableRangeScan_29                                      |
|     └─TableRangeScan_29              | 4.17     | cop[tikv] | table:t2      | range:[-inf,10), keep order:false, stats:pseudo             |



### JSON format of the query plan

```sql
EXPLAIN FORMAT=tidb_json SELECT t1.c0 FROM t0 JOIN t1 ON t0.c0 = t1.c0
  WHERE t0.c0 < 100 GROUP BY t1.c0
  UNION SELECT c0 FROM t2 WHERE c0 < 10;
```

Operations in the `id` fields, and properties are in other fields.

```json
[
    {
        "id": "HashAgg_16",
        "estRows": "6.82",
        "taskType": "root",
        "operatorInfo": "group by:Column#6, funcs:firstrow(Column#6)->Column#6",
        "subOperators": [
            {
                "id": "Union_17",
                "estRows": "7.49",
                "taskType": "root",
                "subOperators": [
                    {
                        "id": "HashAgg_19",
                        "estRows": "4.15",
                        "taskType": "root",
                        "operatorInfo": "group by:test.t1.c0, funcs:firstrow(test.t1.c0)->test.t1.c0",
                        "subOperators": [
                            {
                                "id": "HashJoin_21",
                                "estRows": "4.15",
                                "taskType": "root",
                                "operatorInfo": "inner join, equal:[eq(test.t0.c0, test.t1.c0)]",
                                "subOperators": [
                                    {
                                        "id": "TableReader_24(Build)",
                                        "estRows": "3.32",
                                        "taskType": "root",
                                        "operatorInfo": "data:Selection_23",
                                        "subOperators": [
                                            {
                                                "id": "Selection_23",
                                                "estRows": "3.32",
                                                "taskType": "cop[tikv]",
                                                "operatorInfo": "lt(test.t0.c0, 100), not(isnull(test.t0.c0))",
                                                "subOperators": [
                                                    {
                                                        "id": "TableFullScan_22",
                                                        "estRows": "10.00",
                                                        "taskType": "cop[tikv]",
                                                        "accessObject": "table:t0",
                                                        "operatorInfo": "keep order:false, stats:pseudo"
                                                    }
                                                ]
                                            }
                                        ]
                                    },
                                    {
                                        "id": "TableReader_27(Probe)",
                                        "estRows": "3323.33",
                                        "taskType": "root",
                                        "operatorInfo": "data:Selection_26",
                                        "subOperators": [
                                            {
                                                "id": "Selection_26",
                                                "estRows": "3323.33",
                                                "taskType": "cop[tikv]",
                                                "operatorInfo": "lt(test.t1.c0, 100), not(isnull(test.t1.c0))",
                                                "subOperators": [
                                                    {
                                                        "id": "TableFullScan_25",
                                                        "estRows": "10000.00",
                                                        "taskType": "cop[tikv]",
                                                        "accessObject": "table:t1",
                                                        "operatorInfo": "keep order:false, stats:pseudo"
                                                    }
                                                ]
                                            }
                                        ]
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "id": "TableReader_30",
                        "estRows": "4.17",
                        "taskType": "root",
                        "operatorInfo": "data:TableRangeScan_29",
                        "subOperators": [
                            {
                                "id": "TableRangeScan_29",
                                "estRows": "4.17",
                                "taskType": "cop[tikv]",
                                "accessObject": "table:t2",
                                "operatorInfo": "range:[-inf,10), keep order:false, stats:pseudo"
                            }
                        ]
                    }
                ]
            }
        ]
    }
]
```


## References
* [TiDB EXPLAIN Overview](https://docs.pingcap.com/tidb/stable/explain-overviewn)
* [TiDB EXPLAIN ANALYZE](https://docs.pingcap.com/tidb/v6.5/sql-statement-explain-analyze)
* [TiDB EXPLAIN](https://docs.pingcap.com/tidb/v6.5/sql-statement-explain)
* [TiDB Github: Commit 1e868bb6](https://github.com/pingcap/tidb/tree/f54e63ba)