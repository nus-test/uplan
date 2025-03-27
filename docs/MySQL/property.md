---
title: Properties
layout: default
parent: MySQL
---

The properties of MySQL query plans are defined together with operations. Please refer to the [MySQL operation](operation) page for more details.


| Property               | Category      | Reference                                                                                | Description                                                        |
| ---------------------- | ------------- | ---------------------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| access_type            |               | [Link](https://github.com/mysql/mysql-server/blob/e57893fe/sql/opt_explain_json.cc#L102) | The operation of how to read a table. We map it into an operation. |
| attached_condition     | Configuration | [Link](https://github.com/mysql/mysql-server/blob/e57893fe/sql/opt_explain_json.cc#L103) | The condition to filter out data.                                  |
| cacheable              | Status        | [Link](https://github.com/mysql/mysql-server/blob/e57893fe/sql/opt_explain_json.cc#L106) | Whether the result is cacheable.                                   |
| cost_info              | Cost          | [Link](https://github.com/mysql/mysql-server/blob/e57893fe/sql/opt_explain_json.cc#L157) | Estimated cost.                                                    |
| data_read_per_join     | Cardinality   | [Link](https://github.com/mysql/mysql-server/blob/e57893fe/sql/opt_explain_json.cc#L163) | Estimated number of rows read per join.                            |
| dependent              | Status        | [Link](https://github.com/mysql/mysql-server/blob/e57893fe/sql/opt_explain_json.cc#L107) | Whether the operation depends on another operation.                |
| eval_cost              | Cost          | [Link](https://github.com/mysql/mysql-server/blob/e57893fe/sql/opt_explain_json.cc#L160) | Estimated cost of evaluating an expression or function.            |
| filtered               | Status        | [Link](https://github.com/mysql/mysql-server/blob/e57893fe/sql/opt_explain_json.cc#L109) | How much percentage of rows filtered out.                          |
| key                    | Status        | [Link](https://github.com/mysql/mysql-server/blob/e57893fe/sql/opt_explain_json.cc#L118) | The indexes used.                                                  |
| key_length             | Status        | [Link](https://github.com/mysql/mysql-server/blob/e57893fe/sql/opt_explain_json.cc#L119) | The length of indexes.                                             |
| possible_keys          | Status        | [Link](https://github.com/mysql/mysql-server/blob/e57893fe/sql/opt_explain_json.cc#L129) | The possible indexes in the accessed tables.                       |
| prefix_cost            | Cost          | [Link](https://github.com/mysql/mysql-server/blob/e57893fe/sql/opt_explain_json.cc#L159) | Estimated cost to join data.                                       |
| query_cost             | Cost          | [Link](https://github.com/mysql/mysql-server/blob/e57893fe/sql/opt_explain_json.cc#L162) | Estimated cost of querying.                                        |
| read_cost              | Cost          | [Link](https://github.com/mysql/mysql-server/blob/e57893fe/sql/opt_explain_json.cc#L158) | Estimated cost to read data.                                       |
| ref                    | Configuration | [Link](https://github.com/mysql/mysql-server/blob/e57893fe/sql/opt_explain_json.cc#L132) | The columns that are compared with the used indexes.               |
| rows_examined_per_scan | Cardinality   | [Link](https://github.com/mysql/mysql-server/blob/e57893fe/sql/opt_explain_json.cc#L154) | Estimated number of rows read.                                     |
| rows_produced_per_join | Cardinality   | [Link](https://github.com/mysql/mysql-server/blob/e57893fe/sql/opt_explain_json.cc#L155) | Estimated number of rows returned.                                 |
| sort_cost              | Cost          | [Link](https://github.com/mysql/mysql-server/blob/e57893fe/sql/opt_explain_json.cc#L161) | Estimated cost of sorting.                                         |
| table_name             | Configuration | [Link](https://github.com/mysql/mysql-server/blob/e57893fe/sql/opt_explain_json.cc#L137) | The name of the accessed table.                                    |
| used_columns           | Status        | [Link](https://github.com/mysql/mysql-server/blob/e57893fe/sql/opt_explain_json.cc#L164) | The columns used in this operation.                                |
| used_key_parts         | Status        | [Link](https://github.com/mysql/mysql-server/blob/e57893fe/sql/opt_explain_json.cc#L143) | The used keys.                                                     |
| using_filesort         | Status        | [Link](https://github.com/mysql/mysql-server/blob/e57893fe/sql/opt_explain_json.cc#L144) | Whether uses the filesort.                                         |
| using_temporary_table  | Status        | [Link](https://github.com/mysql/mysql-server/blob/e57893fe/sql/opt_explain_json.cc#L147) | Whether the table is temp.                                         |


## References
* [MySQL WorkBench](https://www.mysql.com/products/workbench/)
* [MySQL Document](https://dev.mysql.com/doc/refman/8.0/en/explain-output.html)
* [MySQL Github Commit: e57893fe](https://github.com/mysql/mysql-server/blob/e57893fe/)
* [MySQL WorkBench Github Commit: 4e1ee296 ](https://github.com/mysql/mysql-workbench/blob/4e1ee296/plugins/wb.query.analysis/explain_renderer.py)