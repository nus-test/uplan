---
title: SQL Server
layout: default
has_children: true
---

# Overview

[SQL Server](https://www.microsoft.com/en-sg/sql-server) is a commercial relational DBMS developed by Microsoft.

SQL Server adopts graphical IDE [SQL Server Management [Studio](https://learn.microsoft.com/en-us/sql/relational-databases/performance/display-the-estimated-execution-plan?view=sql-server-ver16), which supports representing query plans in graph, text, table, XML formats. 

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
SET SHOWPLAN_ALL ON;
SELECT t1.c0 FROM t0 JOIN t1 ON t0.c0 = t1.c0 WHERE t0.c0 < 100 GROUP BY t1.c0 UNION SELECT c0 FROM t2 WHERE c0 < 10;
SET SHOWPLAN_ALL OFF;
```

Each line denotes an operation and associated properties. The column `StmtText` includes descriptions of the operations, the column `PhysicalOp` includes the names of the operations.

| StmtText                                                                                                                                        | StmtId | NodeId | Parent | PhysicalOp           | LogicalOp            | Argument                                                                                                        | DefinedValues                                                      | EstimateRows | EstimateIO | EstimateCPU | AvgRowSize | TotalSubtreeCost | OutputList                                         | Warnings | Type     | Parallel | EstimateExecutions |
| ----------------------------------------------------------------------------------------------------------------------------------------------- | ------ | ------ | ------ | -------------------- | -------------------- | --------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------ | ------------ | ---------- | ----------- | ---------- | ---------------- | -------------------------------------------------- | -------- | -------- | -------- | ------------------ |
| SELECT t1.c0 FROM t0 JOIN t1 ON t0.c0 = t1.c0 WHERE t0.c0 < 100 GROUP BY t1.c0 UNION SELECT c0 FROM t2 WHERE c0 < 10;                           | 1      | 1      | 0      | NULL                 | NULL                 | 1                                                                                                               | NULL                                                               | 9            | NULL       | NULL        | NULL       | 0.026885         | NULL                                               | NULL     | SELECT   | 0        | NULL               |
|   \|--Merge Join(Union)                                                                                                                          | 1      | 2      | 1      | Merge Join           | Union                | NULL                                                                                                            | [Union1008] = ([tempdb].[dbo].[t1].[c0], [tempdb].[dbo].[t2].[c0]) | 9            | 0          | 0.005605    | 11         | 0.026885         | [Union1008]                                        | NULL     | PLAN_ROW | 0        | 1                  |
|        \|--Stream Aggregate(GROUP BY:([tempdb].[dbo].[t1].[c0]))                                                                                 | 1      | 3      | 2      | Stream Aggregate     | Aggregate            | GROUP BY:([tempdb].[dbo].[t1].[c0])                                                                             | NULL                                                               | 1            | 0          | 1.00E-06    | 11         | 0.017988         | [tempdb].[dbo].[t1].[c0]                           | NULL     | PLAN_ROW | 0        | 1                  |
|        \|    \|--Nested Loops(Inner Join, WHERE:([tempdb].[dbo].[t1].[c0]=[tempdb].[dbo].[t0].[c0]))                                              | 1      | 4      | 3      | Nested Loops         | Inner Join           | WHERE:([tempdb].[dbo].[t1].[c0]=[tempdb].[dbo].[t0].[c0])                                                       | NULL                                                               | 1            | 0          | 4.18E-05    | 15         | 0.017987         | [tempdb].[dbo].[t0].[c0], [tempdb].[dbo].[t1].[c0] | NULL     | PLAN_ROW | 0        | 1                  |
|        \|         \|--Sort(ORDER BY:([tempdb].[dbo].[t1].[c0] ASC))                                                                               | 1      | 5      | 4      | Sort                 | Sort                 | ORDER BY:([tempdb].[dbo].[t1].[c0] ASC)                                                                         | NULL                                                               | 1            | 0.011261   | 0.0001      | 11         | 0.014645         | [tempdb].[dbo].[t1].[c0]                           | NULL     | PLAN_ROW | 0        | 1                  |
|        \|         \|    \|--Table Scan(OBJECT:([tempdb].[dbo].[t1]), WHERE:([tempdb].[dbo].[t1].[c0]<(100)))                                       | 1      | 6      | 5      | Table Scan           | Table Scan           | OBJECT:([tempdb].[dbo].[t1]), WHERE:([tempdb].[dbo].[t1].[c0]<(100))                                            | [tempdb].[dbo].[t1].[c0]                                           | 1            | 0.003125   | 0.000158    | 11         | 0.003283         | [tempdb].[dbo].[t1].[c0]                           | NULL     | PLAN_ROW | 0        | 1                  |
|        \|         \|--Table Scan(OBJECT:([tempdb].[dbo].[t0]), WHERE:([tempdb].[dbo].[t0].[c0]<(100)))                                            | 1      | 7      | 4      | Table Scan           | Table Scan           | OBJECT:([tempdb].[dbo].[t0]), WHERE:([tempdb].[dbo].[t0].[c0]<(100))                                            | [tempdb].[dbo].[t0].[c0]                                           | 10           | 0.003125   | 0.000168    | 11         | 0.003293         | [tempdb].[dbo].[t0].[c0]                           | NULL     | PLAN_ROW | 0        | 1                  |
|        \|--Clustered Index Seek(OBJECT:([tempdb].[dbo].[t2].[PK__t2__3213663A4590A185]), SEEK:([tempdb].[dbo].[t2].[c0] < (10)) ORDERED FORWARD) | 1      | 8      | 2      | Clustered Index Seek | Clustered Index Seek | OBJECT:([tempdb].[dbo].[t2].[PK__t2__3213663A4590A185]), SEEK:([tempdb].[dbo].[t2].[c0] < (10)) ORDERED FORWARD | [tempdb].[dbo].[t2].[c0]                                           | 9            | 0.003125   | 0.000167    | 11         | 0.003292         | [tempdb].[dbo].[t2].[c0]                           | NULL     | PLAN_ROW | 0        | 1                  |

### XML format of the query plan

```sql
SET SHOWPLAN_XML ON;
SELECT t1.c0 FROM t0 JOIN t1 ON t0.c0 = t1.c0 WHERE t0.c0 < 100 GROUP BY t1.c0 UNION SELECT c0 FROM t2 WHERE c0 < 10;
SET SHOWPLAN_XML OFF;
```

The query plan is in the `QueryPlan` field, in which operations are denoted in `PhysicalOp`, and properties are denoted by other keys.

```xml
<ShowPlanXML
	xmlns="http://schemas.microsoft.com/sqlserver/2004/07/showplan" Version="1.564" Build="16.0.4015.1">
	<BatchSequence>
		<Batch>
			<Statements>
				<StmtSimple StatementText="SELECT t1.c0 FROM t0 JOIN t1 ON t0.c0 = t1.c0 WHERE t0.c0 &lt; 100 GROUP BY t1.c0 UNION SELECT c0 FROM t2 WHERE c0 &lt; 10" StatementId="1" StatementCompId="1" StatementType="SELECT" RetrievedFromCache="true" StatementSubTreeCost="0.0268855" StatementEstRows="9" SecurityPolicyApplied="false" StatementOptmLevel="FULL" QueryHash="0x4253CC7A59748563" QueryPlanHash="0x1C3FC475FE4447C4" StatementOptmEarlyAbortReason="GoodEnoughPlanFound" CardinalityEstimationModelVersion="160">
					<StatementSetOptions QUOTED_IDENTIFIER="true" ARITHABORT="true" CONCAT_NULL_YIELDS_NULL="true" ANSI_NULLS="true" ANSI_PADDING="true" ANSI_WARNINGS="true" NUMERIC_ROUNDABORT="false"></StatementSetOptions>
					<QueryPlan CachedPlanSize="32" CompileTime="6" CompileCPU="6" CompileMemory="328">
						<MemoryGrantInfo SerialRequiredMemory="512" SerialDesiredMemory="544" GrantedMemory="0" MaxUsedMemory="0"></MemoryGrantInfo>
						<OptimizerHardwareDependentProperties EstimatedAvailableMemoryGrant="660003" EstimatedPagesCached="2640012" EstimatedAvailableDegreeOfParallelism="32" MaxCompileMemory="164294400"></OptimizerHardwareDependentProperties>
						<OptimizerStatsUsage>
							<StatisticsInfo LastUpdate="2023-05-12T05:25:38.47" ModificationCount="0" SamplingPercent="100" Statistics="[_WA_Sys_00000001_38996AB5]" Table="[t0]" Schema="[dbo]" Database="[tempdb]"></StatisticsInfo>
							<StatisticsInfo LastUpdate="2023-05-12T05:25:38.47" ModificationCount="0" SamplingPercent="100" Statistics="[PK__t2__3213663A4590A185]" Table="[t2]" Schema="[dbo]" Database="[tempdb]"></StatisticsInfo>
						</OptimizerStatsUsage>
						<RelOp NodeId="0" PhysicalOp="Merge Join" LogicalOp="Union" EstimateRows="9" EstimateIO="0" EstimateCPU="0.0056051" AvgRowSize="11" EstimatedTotalSubtreeCost="0.0268855" Parallel="0" EstimateRebinds="0" EstimateRewinds="0" EstimatedExecutionMode="Row">
							<OutputList>
								<ColumnReference Column="Union1008"></ColumnReference>
							</OutputList>
							<Merge>
								<DefinedValues>
									<DefinedValue>
										<ColumnReference Column="Union1008"></ColumnReference>
										<ColumnReference Database="[tempdb]" Schema="[dbo]" Table="[t1]" Column="c0"></ColumnReference>
										<ColumnReference Database="[tempdb]" Schema="[dbo]" Table="[t2]" Column="c0"></ColumnReference>
									</DefinedValue>
								</DefinedValues>
								<RelOp NodeId="1" PhysicalOp="Stream Aggregate" LogicalOp="Aggregate" EstimateRows="1" EstimateIO="0" EstimateCPU="1e-06" AvgRowSize="11" EstimatedTotalSubtreeCost="0.0179885" Parallel="0" EstimateRebinds="0" EstimateRewinds="0" EstimatedExecutionMode="Row">
									<OutputList>
										<ColumnReference Database="[tempdb]" Schema="[dbo]" Table="[t1]" Column="c0"></ColumnReference>
									</OutputList>
									<StreamAggregate>
										<DefinedValues></DefinedValues>
										<GroupBy>
											<ColumnReference Database="[tempdb]" Schema="[dbo]" Table="[t1]" Column="c0"></ColumnReference>
										</GroupBy>
										<RelOp NodeId="2" PhysicalOp="Nested Loops" LogicalOp="Inner Join" EstimateRows="1" EstimateIO="0" EstimateCPU="4.18e-05" AvgRowSize="15" EstimatedTotalSubtreeCost="0.0179875" Parallel="0" EstimateRebinds="0" EstimateRewinds="0" EstimatedExecutionMode="Row">
											<OutputList>
												<ColumnReference Database="[tempdb]" Schema="[dbo]" Table="[t0]" Column="c0"></ColumnReference>
												<ColumnReference Database="[tempdb]" Schema="[dbo]" Table="[t1]" Column="c0"></ColumnReference>
											</OutputList>
											<NestedLoops Optimized="0">
												<Predicate>
													<ScalarOperator ScalarString="[tempdb].[dbo].[t1].[c0]=[tempdb].[dbo].[t0].[c0]">
														<Compare CompareOp="EQ">
															<ScalarOperator>
																<Identifier>
																	<ColumnReference Database="[tempdb]" Schema="[dbo]" Table="[t1]" Column="c0"></ColumnReference>
																</Identifier>
															</ScalarOperator>
															<ScalarOperator>
																<Identifier>
																	<ColumnReference Database="[tempdb]" Schema="[dbo]" Table="[t0]" Column="c0"></ColumnReference>
																</Identifier>
															</ScalarOperator>
														</Compare>
													</ScalarOperator>
												</Predicate>
												<RelOp NodeId="3" PhysicalOp="Sort" LogicalOp="Sort" EstimateRows="1" EstimateIO="0.0112613" EstimateCPU="0.000100011" AvgRowSize="11" EstimatedTotalSubtreeCost="0.0146449" Parallel="0" EstimateRebinds="0" EstimateRewinds="0" EstimatedExecutionMode="Row">
													<OutputList>
														<ColumnReference Database="[tempdb]" Schema="[dbo]" Table="[t1]" Column="c0"></ColumnReference>
													</OutputList>
													<MemoryFractions Input="1" Output="1"></MemoryFractions>
													<Sort Distinct="0">
														<OrderBy>
															<OrderByColumn Ascending="1">
																<ColumnReference Database="[tempdb]" Schema="[dbo]" Table="[t1]" Column="c0"></ColumnReference>
															</OrderByColumn>
														</OrderBy>
														<RelOp NodeId="4" PhysicalOp="Table Scan" LogicalOp="Table Scan" EstimateRows="1" EstimatedRowsRead="1" EstimateIO="0.003125" EstimateCPU="0.0001581" AvgRowSize="11" EstimatedTotalSubtreeCost="0.0032831" TableCardinality="0" Parallel="0" EstimateRebinds="0" EstimateRewinds="0" EstimatedExecutionMode="Row">
															<OutputList>
																<ColumnReference Database="[tempdb]" Schema="[dbo]" Table="[t1]" Column="c0"></ColumnReference>
															</OutputList>
															<TableScan Ordered="0" ForcedIndex="0" ForceScan="0" NoExpandHint="0" Storage="RowStore">
																<DefinedValues>
																	<DefinedValue>
																		<ColumnReference Database="[tempdb]" Schema="[dbo]" Table="[t1]" Column="c0"></ColumnReference>
																	</DefinedValue>
																</DefinedValues>
																<Object Database="[tempdb]" Schema="[dbo]" Table="[t1]" IndexKind="Heap" Storage="RowStore"></Object>
																<Predicate>
																	<ScalarOperator ScalarString="[tempdb].[dbo].[t1].[c0]&lt;(100)">
																		<Compare CompareOp="LT">
																			<ScalarOperator>
																				<Identifier>
																					<ColumnReference Database="[tempdb]" Schema="[dbo]" Table="[t1]" Column="c0"></ColumnReference>
																				</Identifier>
																			</ScalarOperator>
																			<ScalarOperator>
																				<Const ConstValue="(100)"></Const>
																			</ScalarOperator>
																		</Compare>
																	</ScalarOperator>
																</Predicate>
															</TableScan>
														</RelOp>
													</Sort>
												</RelOp>
												<RelOp NodeId="5" PhysicalOp="Table Scan" LogicalOp="Table Scan" EstimateRows="10" EstimatedRowsRead="10" EstimateIO="0.003125" EstimateCPU="0.000168" AvgRowSize="11" EstimatedTotalSubtreeCost="0.003293" TableCardinality="10" Parallel="0" EstimateRebinds="0" EstimateRewinds="0" EstimatedExecutionMode="Row">
													<OutputList>
														<ColumnReference Database="[tempdb]" Schema="[dbo]" Table="[t0]" Column="c0"></ColumnReference>
													</OutputList>
													<TableScan Ordered="0" ForcedIndex="0" ForceScan="0" NoExpandHint="0" Storage="RowStore">
														<DefinedValues>
															<DefinedValue>
																<ColumnReference Database="[tempdb]" Schema="[dbo]" Table="[t0]" Column="c0"></ColumnReference>
															</DefinedValue>
														</DefinedValues>
														<Object Database="[tempdb]" Schema="[dbo]" Table="[t0]" IndexKind="Heap" Storage="RowStore"></Object>
														<Predicate>
															<ScalarOperator ScalarString="[tempdb].[dbo].[t0].[c0]&lt;(100)">
																<Compare CompareOp="LT">
																	<ScalarOperator>
																		<Identifier>
																			<ColumnReference Database="[tempdb]" Schema="[dbo]" Table="[t0]" Column="c0"></ColumnReference>
																		</Identifier>
																	</ScalarOperator>
																	<ScalarOperator>
																		<Const ConstValue="(100)"></Const>
																	</ScalarOperator>
																</Compare>
															</ScalarOperator>
														</Predicate>
													</TableScan>
												</RelOp>
											</NestedLoops>
										</RelOp>
									</StreamAggregate>
								</RelOp>
								<RelOp NodeId="6" PhysicalOp="Clustered Index Seek" LogicalOp="Clustered Index Seek" EstimateRows="9" EstimatedRowsRead="9" EstimateIO="0.003125" EstimateCPU="0.0001669" AvgRowSize="11" EstimatedTotalSubtreeCost="0.0032919" TableCardinality="10" Parallel="0" EstimateRebinds="0" EstimateRewinds="0" EstimatedExecutionMode="Row">
									<OutputList>
										<ColumnReference Database="[tempdb]" Schema="[dbo]" Table="[t2]" Column="c0"></ColumnReference>
									</OutputList>
									<IndexScan Ordered="1" ScanDirection="FORWARD" ForcedIndex="0" ForceSeek="0" ForceScan="0" NoExpandHint="0" Storage="RowStore">
										<DefinedValues>
											<DefinedValue>
												<ColumnReference Database="[tempdb]" Schema="[dbo]" Table="[t2]" Column="c0"></ColumnReference>
											</DefinedValue>
										</DefinedValues>
										<Object Database="[tempdb]" Schema="[dbo]" Table="[t2]" Index="[PK__t2__3213663A4590A185]" IndexKind="Clustered" Storage="RowStore"></Object>
										<SeekPredicates>
											<SeekPredicateNew>
												<SeekKeys>
													<EndRange ScanType="LT">
														<RangeColumns>
															<ColumnReference Database="[tempdb]" Schema="[dbo]" Table="[t2]" Column="c0"></ColumnReference>
														</RangeColumns>
														<RangeExpressions>
															<ScalarOperator ScalarString="(10)">
																<Const ConstValue="(10)"></Const>
															</ScalarOperator>
														</RangeExpressions>
													</EndRange>
												</SeekKeys>
											</SeekPredicateNew>
										</SeekPredicates>
									</IndexScan>
								</RelOp>
							</Merge>
						</RelOp>
					</QueryPlan>
				</StmtSimple>
			</Statements>
		</Batch>
	</BatchSequence>
</ShowPlanXML>
```


## References
* [SQL Server Document](https://learn.microsoft.com/en-us/sql/relational-databases/showplan-logical-and-physical-operators-reference?view=sql-server-ver16)
* [SQL Server Management Studio](https://learn.microsoft.com/en-us/sql/relational-databases/performance/display-the-estimated-execution-plan?view=sql-server-ver16)