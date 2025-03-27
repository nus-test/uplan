---
title: PostgreSQL
layout: default
has_children: true
---

# Overview

[PostgreSQL](https://www.postgresql.org/) is a open-source relational DBMS.

PostgreSQL supports representing query plans in [text, table, JSON, XML, and YAML](https://www.postgresql.org/docs/14/sql-explain.html) formats in its shell. 

## Example
```sql
CREATE TABLE t0 (c0 INT);
CREATE TABLE t1 (c0 INT);
CREATE TABLE t2 (c0 INT PRIMARY KEY);
INSERT INTO t0 SELECT * FROM generate_series(1,1000000);
INSERT INTO t2 SELECT * FROM generate_series(1,100);
```

### Text format of the query plan

```sql
EXPLAIN (SUMMARY TRUE)
SELECT t1.c0 FROM t0 JOIN t1 ON t0.c0 = t1.c0
  WHERE t0.c0 < 100 GROUP BY t1.c0
  UNION SELECT c0 FROM t2 WHERE c0 < 10;
```

The words followed by the `->` are operations, and others are properties of the operations.

```shell
                                                  QUERY PLAN                                                  
--------------------------------------------------------------------------------------------------------------
 HashAggregate  (cost=62998.82..63009.32 rows=1050 width=4)
   Group Key: t1.c0
   ->  Append  (cost=27150.40..62996.20 rows=1050 width=4)
         ->  Group  (cost=27150.40..62949.08 rows=200 width=4)
               Group Key: t1.c0
               ->  Gather Merge  (cost=27150.40..62948.08 rows=400 width=4)
                     Workers Planned: 2
                     ->  Group  (cost=26150.38..61901.89 rows=200 width=4)
                           Group Key: t1.c0
                           ->  Merge Join  (cost=26150.38..56906.48 rows=1998164 width=4)
                                 Merge Cond: (t0.c0 = t1.c0)
                                 ->  Sort  (cost=25970.60..26362.39 rows=156719 width=4)
                                       Sort Key: t0.c0
                                       ->  Parallel Seq Scan on t0  (cost=0.00..10301.95 rows=156719 width=4)
                                             Filter: (c0 < 100)
                                 ->  Sort  (cost=179.78..186.16 rows=2550 width=4)
                                       Sort Key: t1.c0
                                       ->  Seq Scan on t1  (cost=0.00..35.50 rows=2550 width=4)
         ->  Bitmap Heap Scan on t2  (cost=10.74..31.37 rows=850 width=4)
               Recheck Cond: (c0 < 10)
               ->  Bitmap Index Scan on t2_pkey  (cost=0.00..10.53 rows=850 width=0)
                     Index Cond: (c0 < 10)
 Planning Time: 0.124 ms
(23 rows)
```

### JSON format of the query plan

```sql
EXPLAIN (FORMAT JSON, VERBOSE TRUE, SUMMARY TRUE)
SELECT t1.c0 FROM t0 JOIN t1 ON t0.c0 = t1.c0
  WHERE t0.c0 < 100 GROUP BY t1.c0
  UNION SELECT c0 FROM t2 WHERE c0 < 10;
```

The value of the key `Node Type` is the operation, and others are properties of the operations.

```shell
                            QUERY PLAN
-------------------------------------------------------------------
 [                                                                +
   {                                                              +
     "Plan": {                                                    +
       "Node Type": "Aggregate",                                  +
       "Strategy": "Hashed",                                      +
       "Partial Mode": "Simple",                                  +
       "Parallel Aware": false,                                   +
       "Async Capable": false,                                    +
       "Startup Cost": 62998.82,                                  +
       "Total Cost": 63009.32,                                    +
       "Plan Rows": 1050,                                         +
       "Plan Width": 4,                                           +
       "Output": ["t1.c0"],                                       +
       "Group Key": ["t1.c0"],                                    +
       "Planned Partitions": 0,                                   +
       "Plans": [                                                 +
         {                                                        +
           "Node Type": "Append",                                 +
           "Parent Relationship": "Outer",                        +
           "Parallel Aware": false,                               +
           "Async Capable": false,                                +
           "Startup Cost": 27150.40,                              +
           "Total Cost": 62996.20,                                +
           "Plan Rows": 1050,                                     +
           "Plan Width": 4,                                       +
           "Subplans Removed": 0,                                 +
           "Plans": [                                             +
             {                                                    +
               "Node Type": "Group",                              +
               "Parent Relationship": "Member",                   +
               "Parallel Aware": false,                           +
               "Async Capable": false,                            +
               "Startup Cost": 27150.40,                          +
               "Total Cost": 62949.08,                            +
               "Plan Rows": 200,                                  +
               "Plan Width": 4,                                   +
               "Output": ["t1.c0"],                               +
               "Group Key": ["t1.c0"],                            +
               "Plans": [                                         +
                 {                                                +
                   "Node Type": "Gather Merge",                   +
                   "Parent Relationship": "Outer",                +
                   "Parallel Aware": false,                       +
                   "Async Capable": false,                        +
                   "Startup Cost": 27150.40,                      +
                   "Total Cost": 62948.08,                        +
                   "Plan Rows": 400,                              +
                   "Plan Width": 4,                               +
                   "Output": ["t1.c0"],                           +
                   "Workers Planned": 2,                          +
                   "Plans": [                                     +
                     {                                            +
                       "Node Type": "Group",                      +
                       "Parent Relationship": "Outer",            +
                       "Parallel Aware": false,                   +
                       "Async Capable": false,                    +
                       "Startup Cost": 26150.38,                  +
                       "Total Cost": 61901.89,                    +
                       "Plan Rows": 200,                          +
                       "Plan Width": 4,                           +
                       "Output": ["t1.c0"],                       +
                       "Group Key": ["t1.c0"],                    +
                       "Plans": [                                 +
                         {                                        +
                           "Node Type": "Merge Join",             +
                           "Parent Relationship": "Outer",        +
                           "Parallel Aware": false,               +
                           "Async Capable": false,                +
                           "Join Type": "Inner",                  +
                           "Startup Cost": 26150.38,              +
                           "Total Cost": 56906.48,                +
                           "Plan Rows": 1998164,                  +
                           "Plan Width": 4,                       +
                           "Output": ["t1.c0"],                   +
                           "Inner Unique": false,                 +
                           "Merge Cond": "(t0.c0 = t1.c0)",       +
                           "Plans": [                             +
                             {                                    +
                               "Node Type": "Sort",               +
                               "Parent Relationship": "Outer",    +
                               "Parallel Aware": false,           +
                               "Async Capable": false,            +
                               "Startup Cost": 25970.60,          +
                               "Total Cost": 26362.39,            +
                               "Plan Rows": 156719,               +
                               "Plan Width": 4,                   +
                               "Output": ["t0.c0"],               +
                               "Sort Key": ["t0.c0"],             +
                               "Plans": [                         +
                                 {                                +
                                   "Node Type": "Seq Scan",       +
                                   "Parent Relationship": "Outer",+
                                   "Parallel Aware": true,        +
                                   "Async Capable": false,        +
                                   "Relation Name": "t0",         +
                                   "Schema": "public",            +
                                   "Alias": "t0",                 +
                                   "Startup Cost": 0.00,          +
                                   "Total Cost": 10301.95,        +
                                   "Plan Rows": 156719,           +
                                   "Plan Width": 4,               +
                                   "Output": ["t0.c0"],           +
                                   "Filter": "(t0.c0 < 100)"      +
                                 }                                +
                               ]                                  +
                             },                                   +
                             {                                    +
                               "Node Type": "Sort",               +
                               "Parent Relationship": "Inner",    +
                               "Parallel Aware": false,           +
                               "Async Capable": false,            +
                               "Startup Cost": 179.78,            +
                               "Total Cost": 186.16,              +
                               "Plan Rows": 2550,                 +
                               "Plan Width": 4,                   +
                               "Output": ["t1.c0"],               +
                               "Sort Key": ["t1.c0"],             +
                               "Plans": [                         +
                                 {                                +
                                   "Node Type": "Seq Scan",       +
                                   "Parent Relationship": "Outer",+
                                   "Parallel Aware": false,       +
                                   "Async Capable": false,        +
                                   "Relation Name": "t1",         +
                                   "Schema": "public",            +
                                   "Alias": "t1",                 +
                                   "Startup Cost": 0.00,          +
                                   "Total Cost": 35.50,           +
                                   "Plan Rows": 2550,             +
                                   "Plan Width": 4,               +
                                   "Output": ["t1.c0"]            +
                                 }                                +
                               ]                                  +
                             }                                    +
                           ]                                      +
                         }                                        +
                       ]                                          +
                     }                                            +
                   ]                                              +
                 }                                                +
               ]                                                  +
             },                                                   +
             {                                                    +
               "Node Type": "Bitmap Heap Scan",                   +
               "Parent Relationship": "Member",                   +
               "Parallel Aware": false,                           +
               "Async Capable": false,                            +
               "Relation Name": "t2",                             +
               "Schema": "public",                                +
               "Alias": "t2",                                     +
               "Startup Cost": 10.74,                             +
               "Total Cost": 31.37,                               +
               "Plan Rows": 850,                                  +
               "Plan Width": 4,                                   +
               "Output": ["t2.c0"],                               +
               "Recheck Cond": "(t2.c0 < 10)",                    +
               "Plans": [                                         +
                 {                                                +
                   "Node Type": "Bitmap Index Scan",              +
                   "Parent Relationship": "Outer",                +
                   "Parallel Aware": false,                       +
                   "Async Capable": false,                        +
                   "Index Name": "t2_pkey",                       +
                   "Startup Cost": 0.00,                          +
                   "Total Cost": 10.53,                           +
                   "Plan Rows": 850,                              +
                   "Plan Width": 0,                               +
                   "Index Cond": "(t2.c0 < 10)"                   +
                 }                                                +
               ]                                                  +
             }                                                    +
           ]                                                      +
         }                                                        +
       ]                                                          +
     },                                                           +
     "Planning Time": 1.954                                       +
   }                                                              +
 ]
(1 row)
```


## References
* [PostgreSQL EXPLAIN](https://www.postgresql.org/docs/14/sql-explain.html)
* [PostgreSQL Github: Commit 1e868bb6](https://github.com/postgres/postgres/tree/1e868bb6)
* [pgMustard](https://www.pgmustard.com/docs/explain)
