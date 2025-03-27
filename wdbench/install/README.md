# WDBench Installation for Neo4j


Please follow the official instructions in [WDBench](https://github.com/MillenniumDB/WDBench) to set up the environment.

Alternatively, you can directly load the key data files that we extracted from the WDBench for Neo4j.


1. Copy the database files into the correct folder.
```bash
sudo cp *.csv /var/lib/neo4j/import
```

2. Start Cypher Shell
```bash
cypher-shell -u neo4j -p 12345678
```


3. Load the data
```cypher
// Import entities nodes
LOAD CSV WITH HEADERS FROM 'file:///entities.csv' AS row
CREATE (:Entity {id: row.ID});

// Import literals nodes
LOAD CSV WITH HEADERS FROM 'file:///literals.csv' AS row
CREATE (:Literal {id: row.ID});

// Import relationships
LOAD CSV WITH HEADERS FROM 'file:///edges.csv' AS row
MATCH (startNode {id: row.START_ID}), (endNode {id: row.END_ID})
CREATE (startNode)-[:RELATIONSHIP_TYPE {type: row.TYPE}]->(endNode);
```

