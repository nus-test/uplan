---
title: Properties
layout: default
parent: SQL Server
---

SQL Server is not open-source, and official documents do not include the explanation of properties, so we examined the properties in the real-world query plans output by SQL Server Management Studio (SSMS).



| Property                                    | Category      | Reference                                                                                                                                 | Description                                                   |
| ------------------------------------------- | ------------- | ----------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------- |
| Estimated CPU Cost                          | Cost          | [Link](https://learn.microsoft.com/en-us/sql/relational-databases/performance/display-the-estimated-execution-plan?view=sql-server-ver24) | Estimated CPU cost.                                           |
| Estimated Execution Mode                    | Configuration | [Link](https://learn.microsoft.com/en-us/sql/relational-databases/performance/display-the-estimated-execution-plan?view=sql-server-ver19) | Row or column read mode.                                      |
| Estimated I/O Cost                          | Cost          | [Link](https://learn.microsoft.com/en-us/sql/relational-databases/performance/display-the-estimated-execution-plan?view=sql-server-ver22) | Estimated IO cost.                                            |
| Estimated Number of Executions              | Status        | [Link](https://learn.microsoft.com/en-us/sql/relational-databases/performance/display-the-estimated-execution-plan?view=sql-server-ver25) | Estimated number of executions.                               |
| Estimated Number of Rows for All Executions | Cardinality   | [Link](https://learn.microsoft.com/en-us/sql/relational-databases/performance/display-the-estimated-execution-plan?view=sql-server-ver27) | Estimated number of rows returned.                            |
| Estimated Number of Rows Per Execution      | Cardinality   | [Link](https://learn.microsoft.com/en-us/sql/relational-databases/performance/display-the-estimated-execution-plan?view=sql-server-ver28) | Estimated number of rows returned for each execution.         |
| Estimated Number of Rows to be Read         | Cardinality   | [Link](https://learn.microsoft.com/en-us/sql/relational-databases/performance/display-the-estimated-execution-plan?view=sql-server-ver26) | Estimated number of rows read.                                |
| Estimated Operator Cost                     | Cost          | [Link](https://learn.microsoft.com/en-us/sql/relational-databases/performance/display-the-estimated-execution-plan?view=sql-server-ver21) | Estimated cost.                                               |
| Estimated Row Size                          | Cardinality   | [Link](https://learn.microsoft.com/en-us/sql/relational-databases/performance/display-the-estimated-execution-plan?view=sql-server-ver29) | Estimated width of returned rows.                             |
| Estimated Subtree Cost                      | Cost          | [Link](https://learn.microsoft.com/en-us/sql/relational-databases/performance/display-the-estimated-execution-plan?view=sql-server-ver23) | Estimated cost of children's operations.                      |
| Logical Operation                           | Configuration | [Link](https://learn.microsoft.com/en-us/sql/relational-databases/performance/display-the-estimated-execution-plan?view=sql-server-ver18) | The associated logical operations.                            |
| NodeId                                      | Configuration | [Link](https://learn.microsoft.com/en-us/sql/relational-databases/performance/display-the-estimated-execution-plan?view=sql-server-ver16) | The unique id to distinguish associated operations.           |
| Object                                      | Configuration | [Link](https://learn.microsoft.com/en-us/sql/relational-databases/performance/display-the-estimated-execution-plan?view=sql-server-ver31) | The objects, tables, indexes, or triggers, that are accessed. |
| Ordered                                     | Status        | [Link](https://learn.microsoft.com/en-us/sql/relational-databases/performance/display-the-estimated-execution-plan?view=sql-server-ver30) | Whether the data is ordered.                                  |
| OutputList                                  | Configuration | [Link](https://learn.microsoft.com/en-us/sql/relational-databases/performance/display-the-estimated-execution-plan?view=sql-server-ver31) | The output column list.                                       |
| Physical Operation                          | Configuration | [Link](https://learn.microsoft.com/en-us/sql/relational-databases/performance/display-the-estimated-execution-plan?view=sql-server-ver17) | The associated physical operations.                           |
| Predicate                                   | Configuration | [Link](https://learn.microsoft.com/en-us/sql/relational-databases/performance/display-the-estimated-execution-plan?view=sql-server-ver31) | The predicate used to filter out data.                        |
| Storage                                     | Status        | [Link](https://learn.microsoft.com/en-us/sql/relational-databases/performance/display-the-estimated-execution-plan?view=sql-server-ver20) | The data is row- or column-stored.                            |


## References
* [SQL Server Document](https://learn.microsoft.com/en-us/sql/relational-databases/showplan-logical-and-physical-operators-reference?view=sql-server-ver16)
* [SQL Server Management Studio](https://learn.microsoft.com/en-us/sql/relational-databases/performance/display-the-estimated-execution-plan?view=sql-server-ver16)