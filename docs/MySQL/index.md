---
title: MySQL
layout: default
has_children: true
---

# Overview

[MySQL](https://www.mysql.com/) is a open-source relational DBMS.

MySQL supports table and JSON formats of query plans in the shell, and also supports a graph format of query plans in the official IDE [MySQL Workbench](https://dev.mysql.com/doc/workbench/en/wb-performance-explain.html).

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
Each line denotes a table scan and associated properties.

| id | select_type  | table      | partitions | type  | possible_keys | key     | key_len | ref  | rows | filtered | Extra                                      |
|----|--------------|------------|------------|-------|---------------|---------|---------|------|------|----------|--------------------------------------------|
|  1 | PRIMARY      | t1         | NULL       | ALL   | NULL          | NULL    | NULL    | NULL |    1 |   100.00 | Using where; Using temporary               |
|  1 | PRIMARY      | t0         | NULL       | ALL   | NULL          | NULL    | NULL    | NULL |   10 |    10.00 | Using where; Using join buffer (hash join) |
|  2 | UNION        | t2         | NULL       | range | PRIMARY       | PRIMARY | 4       | NULL |    9 |   100.00 | Using where; Using index                   |
|  3 | UNION RESULT | <union1,2> | NULL       | ALL   | NULL          | NULL    | NULL    | NULL | NULL |     NULL | Using temporary                            |



### JSON format of the query plan
```sql
EXPLAIN FORMAT=JSON SELECT t1.c0 FROM t0 JOIN t1 ON t0.c0 = t1.c0
  WHERE t0.c0 < 100 GROUP BY t1.c0
  UNION SELECT c0 FROM t2 WHERE c0 < 10;
```
Operations are either keys, such as ``grouping_operation`` and ``nested_loop``, or values, such as ``ALL`` for the key ``access_type`` refers to a table scanning method. Other keys and values are properties of associated operations. We distinguished operations and properties according to the semantics.


```json
 {
  "query_block": {
    "union_result": {
      "using_temporary_table": true,
      "select_id": 3,
      "table_name": "<union1,2>",
      "access_type": "ALL",
      "query_specifications": [
        {
          "dependent": false,
          "cacheable": true,
          "query_block": {
            "select_id": 1,
            "cost_info": {
              "query_cost": "1.60"
            },
            "grouping_operation": {
              "using_temporary_table": true,
              "using_filesort": false,
              "nested_loop": [
                {
                  "table": {
                    "table_name": "t1",
                    "access_type": "ALL",
                    "rows_examined_per_scan": 1,
                    "rows_produced_per_join": 1,
                    "filtered": "100.00",
                    "cost_info": {
                      "read_cost": "0.25",
                      "eval_cost": "0.10",
                      "prefix_cost": "0.35",
                      "data_read_per_join": "8"
                    },
                    "used_columns": [
                      "c0"
                    ],
                    "attached_condition": "(`tass`.`t1`.`c0` < 100)"
                  }
                },
                {
                  "table": {
                    "table_name": "t0",
                    "access_type": "ALL",
                    "rows_examined_per_scan": 10,
                    "rows_produced_per_join": 1,
                    "filtered": "10.00",
                    "using_join_buffer": "hash join",
                    "cost_info": {
                      "read_cost": "0.92",
                      "eval_cost": "0.10",
                      "prefix_cost": "1.60",
                      "data_read_per_join": "8"
                    },
                    "used_columns": [
                      "c0"
                    ],
                    "attached_condition": "(`tass`.`t0`.`c0` = `tass`.`t1`.`c0`)"
                  }
                }
              ]
            }
          }
        },
        {
          "dependent": false,
          "cacheable": true,
          "query_block": {
            "select_id": 2,
            "cost_info": {
              "query_cost": "2.06"
            },
            "table": {
              "table_name": "t2",
              "access_type": "range",
              "possible_keys": [
                "PRIMARY"
              ],
              "key": "PRIMARY",
              "used_key_parts": [
                "c0"
              ],
              "key_length": "4",
              "rows_examined_per_scan": 9,
              "rows_produced_per_join": 9,
              "filtered": "100.00",
              "using_index": true,
              "cost_info": {
                "read_cost": "1.16",
                "eval_cost": "0.90",
                "prefix_cost": "2.06",
                "data_read_per_join": "72"
              },
              "used_columns": [
                "c0"
              ],
              "attached_condition": "(`tass`.`t2`.`c0` < 10)"
            }
          }
        }
      ]
    }
  }
}
```

## References
* [MySQL WorkBench](https://www.mysql.com/products/workbench/)
* [MySQL Document](https://dev.mysql.com/doc/refman/8.0/en/explain-output.html)
* [MySQL Github Commit: e57893fe](https://github.com/mysql/mysql-server/blob/e57893fe/)
* [MySQL WorkBench Github Commit: 4e1ee296 ](https://github.com/mysql/mysql-workbench/blob/4e1ee296/plugins/wb.query.analysis/explain_renderer.py)