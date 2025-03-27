---
title: Neo4j
layout: default
has_children: true
---

# Overview
[Neo4j](https://neo4j.com/) is a graph DBMS.

Neo4j supports a table format of query plans in the shell, and also supports JSON and graph formats of query plans in the official Web UI [Neo4j Browser](https://neo4j.com/developer/neo4j-browser/).

## Example

```cypher
create (n:table {name:'r1'}) return n;
create (n:table {name:'r2'}) return n;
create (n:table {name:'r3'}) return n;
match(m:table),(n:table) WHERE m.name='r1' AND n.name='r3' CREATE(m)-[r:relation]->(n) RETURN r;
```

### Table format of the query plan

```cypher
EXPLAIN MATCH (a:table)-[relation]->() RETURN a.name;
```
The fist column includes operations, and the other columns include associated properties. 

| Operator         | Id | Details                  | Estimated Rows |
|------------------|----|--------------------------|----------------|
| +ProduceResults  |  0 | `a.name`                 |              3 |
| +Projection      |  1 | a.name AS `a.name`       |              3 |
| +Expand(All)     |  2 | (a)-[relation]->(anon_0) |              3 |
| +NodeByLabelScan |  3 | a:table                  |             10 |


### JSON format of the query plan
This query plan is retrieved from Neo4j Browser. The query plan is in the fild `plan`, in which `operatorType` denotes the operations, and other keys denote properties.

```json
{
  "query": {
    "text": "EXPLAIN MATCH (a:table)-[relation]->() RETURN a.name;",
    "parameters": {}
  },
  "queryType": "r",
  "counters": {
    "_stats": {
      "nodesCreated": 0,
      "nodesDeleted": 0,
      "relationshipsCreated": 0,
      "relationshipsDeleted": 0,
      "propertiesSet": 0,
      "labelsAdded": 0,
      "labelsRemoved": 0,
      "indexesAdded": 0,
      "indexesRemoved": 0,
      "constraintsAdded": 0,
      "constraintsRemoved": 0
    },
    "_systemUpdates": 0
  },
  "updateStatistics": {
    "_stats": {
      "nodesCreated": 0,
      "nodesDeleted": 0,
      "relationshipsCreated": 0,
      "relationshipsDeleted": 0,
      "propertiesSet": 0,
      "labelsAdded": 0,
      "labelsRemoved": 0,
      "indexesAdded": 0,
      "indexesRemoved": 0,
      "constraintsAdded": 0,
      "constraintsRemoved": 0
    },
    "_systemUpdates": 0
  },
  "plan": {
    "operatorType": "ProduceResults@neo4j",
    "identifiers": [
      "`a.name`"
    ],
    "arguments": {
      "planner-impl": "IDP",
      "Details": "`a.name`",
      "planner-version": "5.6",
      "string-representation": "Planner COST\n\nRuntime SLOTTED\n\nRuntime version 5.6\n\n+------------------+----+--------------------------+----------------+\n| Operator         | Id | Details                  | Estimated Rows |\n+------------------+----+--------------------------+----------------+\n| +ProduceResults  |  0 | `a.name`                 |              3 |\n| |                +----+--------------------------+----------------+\n| +Projection      |  1 | a.name AS `a.name`       |              3 |\n| |                +----+--------------------------+----------------+\n| +Expand(All)     |  2 | (a)-[relation]->(anon_0) |              3 |\n| |                +----+--------------------------+----------------+\n| +NodeByLabelScan |  3 | a:table                  |             10 |\n+------------------+----+--------------------------+----------------+\n\nTotal database accesses: ?\n",
      "runtime-version": "5.6",
      "runtime": "SLOTTED",
      "Id": {
        "low": 0,
        "high": 0
      },
      "runtime-impl": "SLOTTED",
      "EstimatedRows": 2.9999999999999996,
      "planner": "COST"
    },
    "children": [
      {
        "operatorType": "Projection@neo4j",
        "identifiers": [
          "`a.name`"
        ],
        "arguments": {
          "Details": "a.name AS `a.name`",
          "Id": {
            "low": 1,
            "high": 0
          },
          "EstimatedRows": 2.9999999999999996
        },
        "children": [
          {
            "operatorType": "Expand(All)@neo4j",
            "identifiers": [
              "a",
              "relation",
              "anon_0"
            ],
            "arguments": {
              "Details": "(a)-[relation]->(anon_0)",
              "Id": {
                "low": 2,
                "high": 0
              },
              "EstimatedRows": 2.9999999999999996
            },
            "children": [
              {
                "operatorType": "NodeByLabelScan@neo4j",
                "identifiers": [
                  "a"
                ],
                "arguments": {
                  "Details": "a:table",
                  "Id": {
                    "low": 3,
                    "high": 0
                  },
                  "EstimatedRows": 10
                },
                "children": []
              }
            ]
          }
        ]
      }
    ]
  },
  "profile": false,
  "notifications": [],
  "server": {
    "address": "localhost:7687",
    "agent": "Neo4j/5.6.0",
    "protocolVersion": 5
  },
  "resultConsumedAfter": {
    "low": 0,
    "high": 0
  },
  "resultAvailableAfter": {
    "low": 3,
    "high": 0
  },
  "database": {
    "name": "neo4j"
  }
}
```


## References
* [Neo4j Document](https://neo4j.com/docs/cypher-manual/5/execution-plans/)
* [Neo4j Github Commit: 5ad4387e](https://github.com/neo4j/neo4j/blob/5ad4387e)