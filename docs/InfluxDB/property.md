---
title: Properties
layout: default
parent: InfluxDB
---

InfluxDB only includes plan-level properties and shows an example in its [official documents](https://docs.influxdata.com/influxdb/v2.7/reference/syntax/influxql/spec/#explain), so we examined its documents to study properties.

| Property         | Category    | Reference                                                                                 | Description                     |
| ---------------- | ----------- | ----------------------------------------------------------------------------------------- | ------------------------------- |
| CACHED VALUES    | Status      | [Link](https://docs.influxdata.com/influxdb/v2.7/reference/syntax/influxql/spec/#explain) | The cached values               |
| NUMBER OF BLOCKS | Cardinality | [Link](https://docs.influxdata.com/influxdb/v2.7/reference/syntax/influxql/spec/#explain) | Estimated number of blocks read |
| NUMBER OF FILES  | Cardinality | [Link](https://docs.influxdata.com/influxdb/v2.7/reference/syntax/influxql/spec/#explain) | Estimated number of files read  |
| NUMBER OF SERIES | Cardinality | [Link](https://docs.influxdata.com/influxdb/v2.7/reference/syntax/influxql/spec/#explain) | Estimated number of series      |
| NUMBER OF SHARDS | Cardinality | [Link](https://docs.influxdata.com/influxdb/v2.7/reference/syntax/influxql/spec/#explain) | Estimated number of shards      |
| SIZE OF BLOCKS   | Cardinality | [Link](https://docs.influxdata.com/influxdb/v2.7/reference/syntax/influxql/spec/#explain) | Estimated size of blocks read   |



## Reference
* [InfluxDB Document](https://docs.influxdata.com/influxdb/v2.7/reference/syntax/influxql/spec/#explain)