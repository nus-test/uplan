import json
from uplan import *

import re  
  
def fix_unquoted_json(json_string):  
    return re.sub(r'(?<!:)\s*([a-zA-Z0-9_]+)(?=\s*:)', r'"\1"', json_string)  

nodetype_mongo = {
    'COUNT': ['Folder', 'Aggregate'],
    'RECORD_STORE_FAST_COUNT': ['Folder', 'Aggregate'],
    'PROJECTION_SIMPLE': ['Projector', 'Collect Project'],
    'FETCH': ['Executor', 'Convert'],
    'BATCHED_DELETE': ['Consumer', 'Delete'],
    'DELETE': ['Consumer', 'Delete'],
    'COLLSCAN': ['Producer', 'Full Table Scan'],
    'UNPACK_TIMESERIES_BUCKET': ['Producer', 'Full Table Scan'],
    'GROUP': ['Folder', 'Group'],
    'PROJECTION_COVERED': ['Projector', 'Index Project'],
    'MULTI_ITERATOR': ['Producer', 'Index Scan'],
    'COLUMN_IXSCAN': ['Producer', 'Index-only Scan'],
    'COUNT_SCAN': ['Producer', 'Index-only Scan'],
    'DISTINCT_SCAN': ['Producer', 'Index-only Scan'],
    'IDHACK': ['Producer', 'Index-only Scan'],
    'RETURN_KEY': ['Producer', 'Index-only Scan'],
    'IXSCAN': ['Producer', 'Index-only Scan Range'],
    'AND_HASH': ['Combinator', 'Intersect'],
    'AND_SORTED': ['Combinator', 'Intersect Order'],
    'LIMIT': ['Combinator', 'Limit'],
    'PROJECTION_DEFAULT': ['Projector', 'Project'],
    'EQ_LOOKUP': ['Producer', 'Range Scan'],
    'TEXT_MATCH': ['Producer', 'Range Scan'],
    'CACHED_PLAN': ['Executor', 'Replan'],
    'MULTI_PLAN': ['Executor', 'Replan'],
    'SUBPLAN': ['Executor', 'Replan'],
    'TRIAL': ['Executor', 'Replan'],
    'SAMPLE_FROM_TIMESERIES_BUCKET': ['Producer', 'Sample Scan'],
    'GEO_NEAR_2D': ['Folder', 'Shortest Path'],
    'GEO_NEAR_2DSPHERE': ['Folder', 'Shortest Path'],
    'SKIP': ['Executor', 'Skip'],
    'SORT_DEFAULT': ['Combinator', 'Sort'],
    'SORT_KEY_GENERATOR': ['Combinator', 'Sort'],
    'SORT_SIMPLE': ['Combinator', 'Sort'],
    'QUEUED_DATA': ['Producer', 'Temp Scan'],
    'VIRTUAL_SCAN': ['Producer', 'Temp Scan'],
    'EOF': ['Executor', 'Terminate'],
    'MOCK': ['Executor', 'Test'],
    'SENTINEL': ['Executor', 'Test'],
    'UNKNOWN': ['Executor', 'Test'],
    'OR': ['Combinator', 'Union'],
    'TEXT_OR': ['Combinator', 'Union'],
    'SORT_MERGE': ['Combinator', 'Union Order'],
    'UPDATE': ['Consumer', 'Update']
}

properties_mongo = {
    'advanced': ['Status', 'call'],
    'alreadyHasObj': ['Configuration', 'name object'],
    'chunkSkips': ['Status', 'block hit local'],
    'collation': ['Configuration', 'collation'],
    'direction': ['Status', 'scan direction'],
    'docsExamined': ['Cardinality', 'row read'],
    'docsRejected': ['Cardinality', 'row dropped'],
    'dupsDropped': ['Cardinality', 'row duplicated'],
    'dupsTested': ['Status', 'test'],
    'executionTimeMillisEstimate': ['Cost', 'time'],
    'failed': ['Cardinality', 'row dropped'],
    'filter': ['Configuration', 'filter'],
    'indexBounds': ['Configuration', 'index'],
    'indexName': ['Configuration', 'index'],
    'indexPrefix': ['Configuration', 'index'],
    'indexVersion': ['Configuration', 'version'],
    'isEOF': ['Status', 'end'],
    'isMultiKey': ['Configuration', 'information'],
    'isPartial': ['Configuration', 'information'],
    'isSparse': ['Configuration', 'information'],
    'isUnique': ['Configuration', 'information'],
    'keyPattern': ['Configuration', 'group key'],
    'keysExamined': ['Status', 'index used'],
    'limitAmount': ['Cardinality', 'count'],
    'memLimit': ['Cost', 'memory peak'],
    'memUsage': ['Cost', 'memory'],
    'nBucketsDiscarded': ['Cardinality', 'row dropped'],
    'nBucketsUnpacked': ['Cardinality', 'row read'],
    'nCounted': ['Cardinality', 'row'],
    'needTime': ['Cost', 'time'],
    'needYield': ['Configuration', 'information'],
    'nMatched': ['Cardinality', 'count'],
    'nReturned': ['Cardinality', 'row'],
    'nSkipped': ['Cardinality', 'row read'],
    'nWouldDelete': ['Cardinality', 'row dropped'],
    'nWouldModify': ['Cardinality', 'row read'],
    'nWouldUpsert': ['Cardinality', 'row read'],
    'parsedTextQuery': ['Status', 'string representation'],
    'restoreState': ['Status', 'recovered'],
    'saveState': ['Status', 'suspended'],
    'seeks': ['Status', 'index used'],
    'skipAmount': ['Cardinality', 'row read'],
    'sortPattern': ['Configuration', 'sort key'],
    'spills': ['Status', 'block hit local'],
    'textIndexVersion': ['Configuration', 'version'],
    'totalDataSizeSorted': ['Cardinality', 'memory sort'],
    'transformBy': ['Configuration', 'information'],
    'type': ['Configuration', 'sort key'],
    'usedDisk': ['Cost', 'disk'],
    'warning': ['Configuration', 'information'],
    'works': ['Status', 'worker']
}

global_properties_mongo_result = {}

class MongoTree:
    def __init__(self, json):
        self._json = json
        node = self.handle(json)
        if not node:
            raise Exception("Could not process JSON data\n")
        else:
            self._root = node

    def get_root(self):
        return self._root

    def unexpected(self, node, context=""):
        if context:
            raise Exception("Unexpected: While parsing JSON output: unexpected node in %s: %s\n" % (context, node))
        else:
            raise Exception("Unexpected: While parsing JSON output: unexpected node: %s\n" % node)

    def handle_input_stage(self, sub_plan):
        new_properties = {}
        for key in sub_plan:
            if key in ['stage', 'inputStage']:
                continue
            elif key in properties_mongo:
                new_properties[properties_mongo[key][1]] = [properties_mongo[key][0], sub_plan[key]]
            else:
                raise Exception("Unknown property: %s\n" % key)

        newNode = TreeNode(nodetype_mongo[sub_plan['stage']], new_properties)
        if 'inputStage' in sub_plan:
            newNode.add_child(self.handle_input_stage(sub_plan['inputStage']))
        return newNode

    def handle_cursor(self, stage):
        sub_plan = stage['executionStats']['executionStages']
        return self.handle_input_stage(sub_plan)

    def handle_operator(self, stage):
        new_properties = {}
        new_properties[properties_mongo['executionTimeMillisEstimate']] = stage['executionTimeMillisEstimate']
        new_properties[properties_mongo['nReturned']] = stage['nReturned']
        for key in stage:
            if key in nodetype_mongo:
                newNode = TreeNode(nodetype_mongo[key], new_properties)
                return newNode

    def handle(self, json_subPlan):
        nodeList = []
        stages = json_subPlan.get('stages')

        if stages:
            for stage in stages:
                if '$cursor' in stage:
                    nodeList.append(self.handle_cursor(stage['$cursor']))
        else:
            nodeList.append(self.handle_cursor(json_subPlan))

        return nodeList[0]


# It accepts the query plans from executing the queries in the Compass GUI.
def parse_mongodb(raw_data):
    if not "\"explainVersion\": \"1\"," in raw_data:
        raise Exception("Invalid MongoDB query plans.\n")
    json_data = json.loads(raw_data)
    tree = MongoTree(json_data)
    root = tree.get_root()
    return [root, global_properties_mongo_result]