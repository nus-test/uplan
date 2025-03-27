---
title: MongoDB
layout: default
has_children: true
---

# Overview
[MongoDB](https://www.mongodb.com/) is a document DBMS. 

MongoDB supports a JSON format of query plans in the shell and a graph format of query plans in the official IDE [Compass](https://www.mongodb.com/docs/compass/current/query-plan/).

## Example

```sql
db.createCollection('t0')
db.t0.insertMany([{'c0':1},{'c0':2},{'c0':3},{'c0':4},{'c0':5},{'c0':6},{'c0':7},{'c0':8},{'c0':9},{'c0':10}])
```

### JSON format of the query plan 

```shell
db.t0.find({'c0':{$gte:5}}).explain()
```
The values of `stage` are operations, and others are properties.

```shell
{
  explainVersion: '1',
  queryPlanner: {
    namespace: 'test.t0',
    indexFilterSet: false,
    parsedQuery: { c0: { '$gte': 5 } },
    queryHash: '3C56EF48',
    planCacheKey: '3C56EF48',
    maxIndexedOrSolutionsReached: false,
    maxIndexedAndSolutionsReached: false,
    maxScansToExplodeReached: false,
    winningPlan: {
      stage: 'COLLSCAN',
      filter: { c0: { '$gte': 5 } },
      direction: 'forward'
    },
    rejectedPlans: []
  },
  command: { find: 't0', filter: { c0: { '$gte': 5 } }, '$db': 'test' },
  serverInfo: {
    host: 'soccf-plser3-10',
    port: 27017,
    version: '6.0.4',
    gitVersion: '44ff59461c1353638a71e710f385a566bcd2f547'
  },
  serverParameters: {
    internalQueryFacetBufferSizeBytes: 104857600,
    internalQueryFacetMaxOutputDocSizeBytes: 104857600,
    internalLookupStageIntermediateDocumentMaxSizeBytes: 104857600,
    internalDocumentSourceGroupMaxMemoryBytes: 104857600,
    internalQueryMaxBlockingSortMemoryUsageBytes: 104857600,
    internalQueryProhibitBlockingMergeOnMongoS: 0,
    internalQueryMaxAddToSetBytes: 104857600,
    internalDocumentSourceSetWindowFieldsMaxMemoryBytes: 104857600
  },
  ok: 1
}
```

## References
* [MongoDB Documents](https://docs.mongodb.com/manual/reference/explain-results/#explain-query-plans)
* [MongoDB Github Commit: a857380c](https://github.com/mongodb/mongo/blob/a857380c)