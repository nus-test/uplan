---
title: Properties
layout: default
parent: TiDB
---

Properties in TiDB are clearly stated in a [list](https://github.com/pingcap/tidb/blob/f54e63ba2/planner/core/common_plans.go#L658).


| Property            | Category      | Reference                                                                                | Description                                                                                            |
| ------------------- | ------------- | ---------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| accessObject        | Configuration | [Link](https://github.com/pingcap/tidb/blob/f54e63ba2/planner/core/common_plans.go#L663) | The objects, tables, indexes, or triggers, that are accessed.                                          |
| actRows             | Cardinality   | [Link](https://github.com/pingcap/tidb/blob/f54e63ba2/planner/core/common_plans.go#L661) | Actual rows returned by the associated operation.                                                      |
| costFormula         | Configuration | [Link](https://github.com/pingcap/tidb/blob/f54e63ba2/planner/core/common_plans.go#L667) | The models used for evaluating cost.                                                                   |
| diskInfo            | Cost          | [Link](https://github.com/pingcap/tidb/blob/f54e63ba2/planner/core/common_plans.go#L669) | Disk space occupied by the operator.                                                                   |
| estCost             | Cost          | [Link](https://github.com/pingcap/tidb/blob/f54e63ba2/planner/core/common_plans.go#L666) | Estimated cost.                                                                                        |
| estRows             | Cardinality   | [Link](https://github.com/pingcap/tidb/blob/f54e63ba2/planner/core/common_plans.go#L660) | Estimated number of rows returned.                                                                     |
| executeInfo         | Cost          | [Link](https://github.com/pingcap/tidb/blob/f54e63ba2/planner/core/common_plans.go#L664) | A mix of information on cost.                                                                          |
| id                  | Configuration | [Link](https://github.com/pingcap/tidb/blob/f54e63ba2/planner/core/common_plans.go#L659) | The unique id to distinguish associated operations.                                                    |
| memoryInfo          | Cost          | [Link](https://github.com/pingcap/tidb/blob/f54e63ba2/planner/core/common_plans.go#L668) | Estimated memory space occupied by the operator.                                                       |
| operatorInfo        | Configuration | [Link](https://github.com/pingcap/tidb/blob/f54e63ba2/planner/core/common_plans.go#L665) | A mix of information of the associated operator, including join type, predicate, and returned columns) |
| taskType            | Status        | [Link](https://github.com/pingcap/tidb/blob/f54e63ba2/planner/core/common_plans.go#L662) | The computation node that the associated operation executes.                                           |
| totalMemoryConsumed | Cost          | [Link](https://github.com/pingcap/tidb/blob/f54e63ba2/planner/core/common_plans.go#L670) | Similar to memoryInfo.                                                                                 |

## References
* [TiDB EXPLAIN Overview](https://docs.pingcap.com/tidb/stable/explain-overviewn)
* [TiDB EXPLAIN ANALYZE](https://docs.pingcap.com/tidb/v6.5/sql-statement-explain-analyze)
* [TiDB EXPLAIN](https://docs.pingcap.com/tidb/v6.5/sql-statement-explain)
* [TiDB Github: Commit 1e868bb6](https://github.com/pingcap/tidb/tree/f54e63ba)