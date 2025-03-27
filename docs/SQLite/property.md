---
title: Properties
layout: default
parent: SQLite
---

The properties are defined together with operations, and we distinguished them by their locations in query plans, as the first phrase of each line is the operation, and the rest are properties. 


| Property                    | Category      | Reference                                                               | Description                                    |
| --------------------------- | ------------- | ----------------------------------------------------------------------- | ---------------------------------------------- |
| (a=? AND b>?)               | Configuration | [Link](https://www.sqlite.org/eqp.html)                                 | The predicate for filters.                     |
| USING INDEX                 | Configuration | [Link](https://github.com/sqlite/sqlite/blob/9089f060/src/expr.c#L2958) | Whether the associated operation uses indexes. |
| USING ROWID SEARCH ON TABLE | Configuration | [Link](https://github.com/sqlite/sqlite/blob/9089f060/src/expr.c#L2878) | Whether using rowid to search tables.          |

## References
* [SQLite EXPLAIN QUERY PLAN](https://www.sqlite.org/eqp.html)
* [SQLite Github: Commit 9089f060](https://github.com/sqlite/sqlite/blob/9089f060)