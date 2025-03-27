# YCSB

YCSB is a dynamic workload generator for cloud databases, so we need to configure the framework to collect query plans. Compared to TPC-H and WDBench, YCSB includes non-query workloads.

1. Configure YCSB (Suppose MongoDB is running)
```bash
wget https://github.com/brianfrankcooper/YCSB/releases/download/0.17.0/ycsb-mongodb-binding-0.17.0.tar.gz
tar -zxvf ycsb-mongodb-binding-0.17.0.tar.gz
mv ycsb-mongodb-binding-0.17.0 ycsb
cd ycsb
./bin/ycsb.sh load mongodb -s -P workloads/workloada
```

2. Collect query plans
YCSB does not support logging executed queries, so we need to collect query plans by examining MongoDB logs. We can use the following script to collect query plans.

In mongo shell:
```javascript
use ycsb;
db.setProfilingLevel(2)
```
Execute the YCSB workload:
```bash
./bin/ycsb.sh run mongodb -s -P workloads/workloada
```

Run the python script to collect query plans:
```bash
pip3 install pymongo
python3 ycsb/obtain_plan.py
```

The raw query plans will be stored in the folder `queryplan_raw`.