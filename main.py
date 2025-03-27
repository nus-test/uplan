import argparse
import json
import sys

from pgformat import parse_postgresql
from tidbformat import parse_tidb
from mysqlformat import parse_mysql
from neo4jformat import parse_neo4j
from mongodbformat import parse_mongodb



parser = argparse.ArgumentParser(description='The convertor for the unified query plan format.')
parser.add_argument('-t', '--target', choices=['mongodb', 'mysql', 'neo4j', 'tidb', 'postgresql'], default='mysql',
                    help='the DBMS of the query plan')
parser.add_argument('-i', '--input', type=str, default='stdin', help='the file path of the query plan')
parser.add_argument('-o', '--output', type=str, default='stdout', help='the file path of the output')
parser.add_argument('-d', '--debug', action='store_true', default=True, help='enable debug mode')
parser.add_argument('-a', '--application', type=str, default='test', help='which application the uplan is used for')

args = parser.parse_args()
target = args.target
if args.input == 'stdin':
    input = sys.stdin
else:
    input = open(args.input, 'r')
if args.output == 'stdout':
    output = sys.stdout
else:
    output = open(args.output, 'w')

with input as f:
    raw_data = f.read()

parse_dbms = getattr(sys.modules[__name__], 'parse_'+target)
[root, global_properties] = parse_dbms(raw_data)

if args.application == 'test': 
    global_properties['Plan'] = root.to_json()
elif args.application == 'qpg':
    global_properties.clear()
    global_properties['Plan'] = root.to_json_qpg()
elif args.application == 'cert':
    with output as f:
        f.write(str(root.extract_cardinality_cert()))
    exit(0)
elif args.application == 'simplified_json':
    global_properties['Plan'] = root.to_simplified_json()
elif args.application == 'simplified':
    print(root)
    for key, value in global_properties.items():
        print(key + ": " + str(value[1]))
    exit(0)
else:
    raise Exception('Unknown application: %s' % args.application)

with output as f:
    json.dump(global_properties, f, indent=4)

