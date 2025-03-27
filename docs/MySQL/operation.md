---
title: Operations
layout: default
parent: MySQL
---

The operations and properties in MySQL do not have a significant difference in formats, and are defined together in the [source code](https://github.com/mysql/mysql-server/blob/e57893fe/sql/opt_explain_json.cc#L102).

We referred to the [official documentation](https://dev.mysql.com/doc/refman/8.0/en/explain-output.html) and the [Workbench](https://github.com/mysql/mysql-workbench/blob/4e1ee296/plugins/wb.query.analysis/explain_renderer.py) to understand the semantics and distinguish the operations and properties.

Most operations are defined as the keys in the JSON format of query plans except for the operations of the Read category, which are showed as the values of the key `access_type`. 


| Operation                  | Category | Reference                                                                                | Description                                                                                               |
| -------------------------- | -------- | ---------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| ALL                        | Producer | [Link](https://github.com/mysql/mysql-server/blob/e57893fe/sql/opt_explain.cc#L115)      | A full table scan.                                                                                        |
| attached_subqueries        | Producer | [Link](https://github.com/mysql/mysql-server/blob/e57893fe/sql/opt_explain_json.cc#L104) | Scan data from subqueries.                                                                                |
| buffer_result              | Executor | [Link](https://github.com/mysql/mysql-server/blob/e57893fe/sql/opt_explain_json.cc#L105) | Cache the data into the buffer.                                                                           |
| const                      | Producer | [Link](https://github.com/mysql/mysql-server/blob/e57893fe/sql/opt_explain.cc#L115)      | The table has only one row for the scan.                                                                  |
| duplicates_removal         | Combinator      | [Link](https://github.com/mysql/mysql-server/blob/e57893fe/sql/opt_explain_json.cc#L108) | Remove duplicate data.                                                                                    |
| eq_ref                     | Producer | [Link](https://github.com/mysql/mysql-server/blob/e57893fe/sql/opt_explain.cc#L115)      | Scan the table with the index and return one row only if joining with another table.                      |
| fulltext                   | Producer | [Link](https://github.com/mysql/mysql-server/blob/e57893fe/sql/opt_explain.cc#L116)      | Scan the table with the full-text index.                                                                  |
| grouping_operation         | Folder   | [Link](https://github.com/mysql/mysql-server/blob/e57893fe/sql/opt_explain_json.cc#L113) | Group data.                                                                                               |
| having_subqueries          | Producer | [Link](https://github.com/mysql/mysql-server/blob/e57893fe/sql/opt_explain_json.cc#L115) | Read the subquery from the having clause.                                                                 |
| index                      | Producer | [Link](https://github.com/mysql/mysql-server/blob/e57893fe/sql/opt_explain.cc#L116)      | It tries an index-only scan and executes a full table scan if the index contains all required data.       |
| index_merge                | Join     | [Link](https://github.com/mysql/mysql-server/blob/e57893fe/sql/opt_explain.cc#L116)      | The Index Merge access method retrieves rows with multiple range scans and merges their results into one. |
| index_subquery             | Producer | [Link](https://github.com/mysql/mysql-server/blob/e57893fe/sql/opt_explain.cc#L1506)     | Scan the data with indexes, but replaces the list in IN clause with a subquery.                           |
| materialized_from_subquery | Executor | [Link](https://github.com/mysql/mysql-server/blob/e57893fe/sql/opt_explain_json.cc#L120) | Materialize data from associated subqueries.                                                              |
| nested_loop                | Join     | [Link](https://github.com/mysql/mysql-server/blob/e57893fe/sql/opt_explain_json.cc#L123) | Performs a nested loop join.                                                                              |
| ordering_operation         | Combinator      | [Link](https://github.com/mysql/mysql-server/blob/e57893fe/sql/opt_explain_json.cc#L126) | Sort data by specific keys.                                                                               |
| range                      | Producer | [Link](https://github.com/mysql/mysql-server/blob/e57893fe/sql/opt_explain.cc#L116)      | Scan the table in a range.                                                                                |
| ref                        | Producer | [Link](https://github.com/mysql/mysql-server/blob/e57893fe/sql/opt_explain.cc#L115)      | All rows with matching index values are read from this table                                              |
| ref_or_null                | Producer | [Link](https://github.com/mysql/mysql-server/blob/e57893fe/sql/opt_explain.cc#L116)      | Similar to eq_ref, but does an extra search for rows that contain NULL values.                            |
| select_list_subqueries     | Producer | [Link](https://github.com/mysql/mysql-server/blob/e57893fe/sql/opt_explain_json.cc#L134) | Scan data from subqueries in the SELECT clause.                                                           |
| system                     | Producer | [Link](https://github.com/mysql/mysql-server/blob/e57893fe/sql/opt_explain.cc#L115)      | The table has only one row (= system table).                                                              |
| table                      | Producer | [Link](https://github.com/mysql/mysql-server/blob/e57893fe/sql/opt_explain_json.cc#L136) | Read data from a table.                                                                                   |
| union_result               | Combinator      | [Link](https://github.com/mysql/mysql-server/blob/e57893fe/sql/opt_explain_json.cc#L138) | Union results.                                                                                            |
| unique_subquery            | Producer | [Link](https://github.com/mysql/mysql-server/blob/e57893fe/sql/opt_explain.cc#L1506)     | Scan the data with unique indexes, but replaces the list in IN clause with a subquery.                    |


## References
* [MySQL WorkBench](https://www.mysql.com/products/workbench/)
* [MySQL Document](https://dev.mysql.com/doc/refman/8.0/en/explain-output.html)
* [MySQL Github Commit: e57893fe](https://github.com/mysql/mysql-server/blob/e57893fe/)
* [MySQL WorkBench Github Commit: 4e1ee296 ](https://github.com/mysql/mysql-workbench/blob/4e1ee296/plugins/wb.query.analysis/explain_renderer.py)