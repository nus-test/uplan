---
title: UPlan
layout: default
nav_order: 4
---

# UPlan
We provide the source code of the prototype UPlan for maintaining the unified query plan representations here: [https://github.com/unifiedqueryplan/unifiedqueryplan.github.io](https://github.com/unifiedqueryplan/unifiedqueryplan.github.io)

## Quick Start
To transfer an original TiDB query plan into the unified representation, run:
```bash
python3 main.py -t tidb -i tpc-h/queryplan_raw/1.tidb
```
The unified query plan in the text format will be printed on the console.