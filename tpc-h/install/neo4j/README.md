# The steps to run TPC-H benchmark on Neo4j



You can directly use the database files generated for other databases. Then, you run 
```bash
sudo cp *.tbl /var/lib/neo4j/import
```
to copy the database files into the correct folder.

Then, you run 
```bash
cypher-shell -u neo4j -p 12345678
```
and execute the commands in the `ddl.cql` to create the database.

