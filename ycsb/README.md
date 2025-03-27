# YCSB


This folder contains the scripts to configure YCSB benchmark and experimental data for the third application: benchmarking.

## Structure
* [install.md](install.md): The scripts to configure the WDBench benchmark on Neo4j.
* [obtain_plan.py](obtain_plan.py): The script to collect query plans.
* [queryplan_raw](queryplan_raw): The query plans generated.
* [queryplan_unified](queryplan_unified): The unified query plans transferred by UPlan based on the query plans in the folder `queryplan_raw`.