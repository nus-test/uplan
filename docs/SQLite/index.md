---
title: SQLite
layout: default
has_children: true
---

# Overview

[SQLite](https://sqlite.org/) is an embedded relational DBMS, which is a library that runs in the same process as the application using it.

SQLite supports a text format of query plans in its shell.

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
EXPLAIN QUERY PLAN SELECT t1.c0 FROM t0 JOIN t1 ON t0.c0 = t1.c0
  WHERE t0.c0 < 100 GROUP BY t1.c0
  UNION SELECT c0 FROM t2 WHERE c0 < 10;
```

The first phrase followed by a ``--`` is an operation, and others are properties.

```shell
QUERY PLAN
`--COMPOUND QUERY
   |--LEFT-MOST SUBQUERY
   |  |--SCAN t0
   |  |--SEARCH t1 USING AUTOMATIC COVERING INDEX (c0=?)
   |  `--USE TEMP B-TREE FOR GROUP BY
   `--UNION USING TEMP B-TREE
      `--SEARCH t2 USING COVERING INDEX sqlite_autoindex_t2_1 (c0<?)

```

## References
* [SQLite EXPLAIN QUERY PLAN](https://www.sqlite.org/eqp.html)
* [SQLite Github: Commit 9089f060](https://github.com/sqlite/sqlite/blob/9089f060)