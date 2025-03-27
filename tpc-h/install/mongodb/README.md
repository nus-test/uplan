# The steps to run TPC-H benchmark on MongoDB



You can directly use the database files generated for other databases. Then, you run 
```bash
javac -cp "lib/*" DenormalizedExampleModel.java
```
to create the database.

For debugging, you can directly press F5 in the tpc-h/mongodb folder, as the VS would directly search the `lib` subforder for the dependencies.

All the queries are in queries/mql folder.


Log in the shell:
```bash
mongosh
```