import json
from uplan import *

nodetype_tidb = {
    'Aggregation': ['Folder', 'Aggregate'],
    'HashAgg': ['Folder', 'Aggregate Hash'],
    'StreamAgg': ['Folder', 'Aggregate Stream'],
    'ExchangeReceiver': ['Executor', 'Collect'],
    'ShuffleReceiver': ['Executor', 'Collect'],
    'TableReader': ['Executor', 'Collect'],
    'TiKVSingleGather': ['Executor', 'Collect'],
    'IndexLookUp': ['Executor', 'Collect Order'],
    'IndexMerge': ['Executor', 'Collect Order'],
    'IndexReader': ['Executor', 'Collect Order'],
    'TableDual': ['Producer', 'Constant'],
    'Delete': ['Consumer', 'Delete'],
    'ExchangeSender': ['Executor', 'Distribute'],
    'Shuffle': ['Executor', 'Distribute'],
    'Exists': ['Folder', 'Exist'],
    'CTE': ['Producer', 'Expression Scan'],
    'CTEFullScan': ['Producer', 'Expression Scan'],
    'CTETable': ['Producer', 'Expression Scan'],
    'Foreign_Key_Check': ['Consumer', 'Foreign Key Check'],
    'Foreign_Key_Cascade': ['Consumer', 'Foreign Key Update'],
    'DataSource': ['Producer', 'Full Table Scan'],
    'LoadData': ['Producer', 'Full Table Scan'],
    'TableFullScan': ['Producer', 'Full Table Scan'],
    'TableScan': ['Producer', 'Full Table Scan'],
    'HashJoin': ['Join', 'Hash Join'],
    'TableRowIDScan': ['Producer', 'Id Scan'],
    'IndexHashJoin': ['Join', 'Index Hash'],
    'IndexJoin': ['Join', 'Index Join'],
    'IndexMergeJoin': ['Join', 'Index Merge'],
    'IndexScan': ['Producer', 'Index Scan'],
    'IndexFullScan': ['Producer', 'Index-only Scan'],
    'Point_Get': ['Producer', 'Index-only Scan'],
    'Batch_Point_Get': ['Producer', 'Index-only Scan Range'],
    'IndexRangeScan': ['Producer', 'Index-only Scan Range'],
    'Insert': ['Consumer', 'Insert'],
    'Join': ['Join', 'Join'],
    'Limit': ['Combinator', 'Limit'],
    'MaxOneRow': ['Combinator', 'Limit'],
    'SelectLock': ['Executor', 'Lock'],
    'MergeJoin': ['Join', 'Merge'],
    'Apply': ['Join', 'Nested Loop'],
    'Projection': ['Projector', 'Project'],
    'TableRangeScan': ['Producer', 'Range Scan'],
    'TableSample': ['Producer', 'Sample Scan'],
    'Set': ['Executor', 'Configure'],
    'Show': ['Executor', 'Show'],
    'ShowDDLJobs': ['Executor', 'Show'],
    'Sort': ['Combinator', 'Sort'],
    'TopN': ['Combinator', 'Sort Part'],
    'ClusterMemTableReader': ['Producer', 'Temp Scan'],
    'MemTableScan': ['Producer', 'Temp Scan'],
    'Union': ['Combinator', 'Union'],
    'PartitionUnion': ['Combinator', 'Union Recursive'],
    'UnionScan': ['Producer', 'Union Scan'],
    'Update': ['Consumer', 'Update'],
    'Window': ['Folder', 'Window']
}

properties_tidb = {
    'accessObject': ['Configuration', 'name object'],
    'actRows': ['Cardinality', 'row actual'],
    'costFormula': ['Configuration', 'formula'],
    'diskInfo': ['Cost', 'disk'],
    'estCost': ['Cost', 'cost'],
    'estRows': ['Cardinality', 'row'],
    'executeInfo': ['Cost', 'information'],
    'id': ['Configuration', 'id'],
    'memoryInfo': ['Cost', 'memory'],
    'operatorInfo': ['Configuration', 'information'],
    'taskType': ['Status', 'location'],
    'totalMemoryConsumed': ['Cost', 'memory']
}

global_properties_tidb_result = {}

class TiDBTree:
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

    def handle(self, json_subPlan):
        nodeType = json_subPlan.get('id').rsplit('_', 1)[0]
        if nodeType in nodetype_tidb:
            nodeType = nodetype_tidb.get(nodeType)
        elif (nodeType == 'Selection'): # Operator Selection is merged into FILTER property of its child node which should only be one
            if len(json_subPlan.get('subOperators')) == 1:
                nodeType = nodetype_tidb.get(json_subPlan.get('subOperators')[0].get('id').rsplit('_', 1)[0])
                json_subPlan = json_subPlan.get('subOperators')[0]
            else:
                raise Exception('Unexpected Selection node')
        else:
            raise Exception('Unknown node type: %s' % nodeType)

        new_node_properties = {}
        for key, value in properties_tidb.items():
            if key in json_subPlan:
                new_node_properties[value[1]] = [value[0], json_subPlan.get(key)]

        newNode = TreeNode(nodeType, new_node_properties)

        for childPlan in json_subPlan.get('subOperators') or []:
            newNode.add_child(self.handle(childPlan))
        
        return newNode

# It accepts the query plan via `EXPLAIN FORMAT=tidb_json SELECT...`
def parse_tidb(raw_data):
    validated_data = raw_data.replace('\\n', '\n').replace('\\\\n', '\\n').replace('\\\\\\"', '\\\"').replace('\\\\"', '\\"').replace('\\\\t', '\\t').replace('\\\\r', '\\r')
    validated_data = validated_data[validated_data.find('['):validated_data.rfind(']')+1]
    
    json_data = json.loads(validated_data, strict=False)[0]
    root = TiDBTree(json_data).get_root()
    return [root, global_properties_tidb_result]

