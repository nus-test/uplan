---
title: InfluxDB
layout: default
has_children: true
---

# Overview
[InfluxDB](https://www.influxdata.com/) is a time series DBMS.

InfluxDB supports a text format of query plans, and does not explicitly show operations being performed in query plans, so we examined properties only.



## Example

```sql
insert cpu,host=node1 value=10
```

### Text format of the query plan

```sql
explain select * from cpu
```
The query plan includes a list of key-value pairs, in which keys are property names and values are property values.
    
```shell
QUERY PLAN
----------
EXPRESSION: <nil>
AUXILIARY FIELDS: host::tag, value::float
NUMBER OF SHARDS: 1
NUMBER OF SERIES: 1
CACHED VALUES: 1
NUMBER OF FILES: 0
NUMBER OF BLOCKS: 0
SIZE OF BLOCKS: 0
```

## Reference
* [InfluxDB Document](https://docs.influxdata.com/influxdb/v2.7/reference/syntax/influxql/spec/#explain)