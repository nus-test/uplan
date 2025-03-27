---
title: Operations
layout: default
parent: SQLite
---

SQLite specifies operations and properties in parameters of the function call [ExplainQueryPlan()](https://github.com/sqlite/sqlite/blob/908dec74/src/select.c#L2713). We distinguished operations and properties by their locations in query plans, as the first phrase of each line is the operation, and the rest are properties. 



| Operation           | Category | Reference                                                                    | Description                                                                                                                                                                       |
| ------------------- | -------- | ---------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| COMPOUND QUERY      | Combinator      | [Link](https://github.com/sqlite/sqlite/blob/9089f060/src/select.c#L2923)    | Each component query of a compound query (UNION, UNION ALL, EXCEPT, or INTERSECT) is assigned and computed separately and is given its own line in the EXPLAIN QUERY PLAN output. |
| CO-ROUTINE          | Join     | [Link](https://github.com/sqlite/sqlite/blob/9089f060/src/select.c#L7364)    | Run the subquery co-routine instead of storing temperature results in memory.                                                                                                     |
| LEFT                | Combinator      | [Link](https://github.com/sqlite/sqlite/blob/9089f060/src/select.c#L3637)    | The left query for a composed query.                                                                                                                                              |
| LEFT-MOST SUBQUERY  | Combinator      | [Link](https://github.com/sqlite/sqlite/blob/9089f060/src/select.c#L2924)    | The left subquery is a composed query.                                                                                                                                            |
| LIST SUBQUERY       | Join     | [Link](https://github.com/sqlite/sqlite/blob/9089f060/src/expr.c#L3207)      | A subquery that returns a list of values.                                                                                                                                         |
| MATERIALIZE         | Executor | [Link](https://github.com/sqlite/sqlite/blob/9089f060/src/select.c#L7417)    | Materialize data into memory to speed up follow-up calculation.                                                                                                                   |
| MERGE               | Combinator      | [Link](https://github.com/sqlite/sqlite/blob/9089f060/src/select.c#L3628)    | Merge the results of two queries.                                                                                                                                                 |
| MULTI-INDEX OR      | Combinator      | [Link](https://github.com/sqlite/sqlite/blob/9089f060/src/wherecode.c#L2272) |  OR optimization, in which there will be a single top-level record for the search, with two sub-records, one for each index:                                                      |
| RECURSIVE STEP      | Executor | [Link](https://github.com/sqlite/sqlite/blob/9089f060/src/select.c#L2747)    | Execute the recursive SELECT taking the single row in Current as the value for the recursive table. Store the results in the Queue.                                               |
| REUSE LIST SUBQUERY | Executor | [Link](https://github.com/sqlite/sqlite/blob/9089f060/src/expr.c#L3157)      | Reuse a previously computed list subquery.                                                                                                                                        |
| REUSE SUBQUERY      | Join     | [Link](https://github.com/sqlite/sqlite/blob/9089f060/src/expr.c#L3347)      | Reuse a previously computed subquery.                                                                                                                                             |
| RIGHT               | Combinator      | [Link](https://github.com/sqlite/sqlite/blob/9089f060/src/select.c#L3652)    | The right query for a composed query.                                                                                                                                             |
| SCAN                | Producer | [Link](https://github.com/sqlite/sqlite/blob/9089f060/src/select.c#L6655)    | Scan the entire table.                                                                                                                                                            |
| SCAN CONSTANT ROW   | Producer | [Link](https://github.com/sqlite/sqlite/blob/9089f060/src/where.c#L5935)     | Read constant values.                                                                                                                                                             |
| SEARCH              | Producer | [Link](https://www.sqlite.org/eqp.html)                                      | Scan partial table via indexes.                                                                                                                                                   |
| SETUP               | Executor | [Link](https://github.com/sqlite/sqlite/blob/908dec74/src/select.c#L2713)    | Store the results of the setup query in Queue.                                                                                                                                    |
| USE TEMP B-TREE     | Executor | [Link](https://github.com/sqlite/sqlite/blob/9089f060/src/select.c#L3027)    | Optimization for a composed query that stores a subquery into a b-tree in memory for efficiency.                                                                                  |


## References
* [SQLite EXPLAIN QUERY PLAN](https://www.sqlite.org/eqp.html)
* [SQLite Github: Commit 9089f060](https://github.com/sqlite/sqlite/blob/9089f060)