import json
from uplan import *

nodetype_pg = {
    'Aggregate': ['Folder', 'Aggregate'],
    'WindowAgg': ['Folder', 'Aggregate Part'],
    'BitmapAnd': ['Executor', 'And Bitmap'],
    'Bitmap Heap Scan': ['Producer', 'Bitmap Heap Scan'],
    'Bitmap Index Scan': ['Producer', 'Bitmap Index Scan'],
    'Memoize': ['Executor', 'Cache'],
    'Gather': ['Executor', 'Collect'],
    'Gather Merge': ['Executor', 'Collect Order'],
    'Result': ['Producer', 'Constant'],
    'Custom Scan': ['Producer', 'Customized Scan'],
    'ProjectSet': ['Executor', 'Execute Function'],
    'CTE Scan': ['Producer', 'Expression Scan'],
    'Seq Scan': ['Producer', 'Full Table Scan'],
    'Function Scan': ['Producer', 'Function Scan'],
    'Table Function Scan': ['Producer', 'Function Scan Range'],
    'Group': ['Folder', 'Group'],
    'Hash Join': ['Join', 'Hash Join'],
    'Hash': ['Executor', 'Hash Row'],
    'Tid Scan': ['Producer', 'Id Scan'],
    'Tid Range Scan': ['Producer', 'Id Scan Range'],
    'Index Scan': ['Producer', 'Index Scan'],
    'Index Only Scan': ['Producer', 'Index-only Scan'],
    'Limit': ['Combinator', 'Limit'],
    'LockRows': ['Executor', 'Lock'],
    'Materialize': ['Executor', 'Materialize'],
    'Merge Join': ['Join', 'Merge'],
    'Nested Loop': ['Join', 'Nested Loop'],
    'BitmapOr': ['Executor', 'Or Bitmap'],
    'Foreign Scan': ['Producer', 'Remote Scan'],
    'Sample Scan': ['Producer', 'Sample Scan'],
    'SetOp': ['Combinator', 'Set Or'],
    'Sort': ['Combinator', 'Sort'],
    'Incremental Sort': ['Combinator', 'Sort Part'],
    'Subquery Scan': ['Producer', 'Subquery Scan'],
    'Named Tuplestore Scan': ['Producer', 'Temp Scan'],
    'WorkTable Scan': ['Producer', 'Temp Scan'],
    'Append': ['Combinator', 'Union'],
    'Merge Append': ['Combinator', 'Union Order'],
    'Recursive Union': ['Combinator', 'Union Recursive'],
    'Unique': ['Combinator', 'Unique'],
    'ModifyTable': ['Consumer', 'Update'],
    'Values Scan': ['Producer', 'Value Scan']
}

properties_pg = {
    'Actual Loops': ['Status', 'loop actual'],
    'Actual Rows': ['Cardinality', 'row actual'],
    'Actual Startup Time': ['Cost', 'time startup actual'],
    'Actual Total Time': ['Cost', 'time actual'],
    'Alias': ['Configuration', 'alias'],
    'Async Capable': ['Configuration', 'async'],
    'Average Sort Space Used': ['Cost', 'memory sort average'],
    'Cache Evictions': ['Status', 'cache evicition'],
    'Cache Hits': ['Status', 'cache hit'],
    'Cache Key': ['Configuration', 'cache key'],
    'Cache Misses': ['Status', 'cache miss'],
    'Cache Mode': ['Configuration', 'cache mode'],
    'Cache Overflows': ['Status', 'cache overflow'],
    'Calls': ['Status', 'call'],
    'Command': ['Configuration', 'command'],
    'Conflict Arbiter Indexes': ['Configuration', 'index conflict arbiter'],
    'Conflict Resolution': ['Status', 'conflict resolution'],
    'Conflicting Tuples': ['Status', 'conflict'],
    'Constraint Name': ['Configuration', 'constraint'],
    'CTE Name': ['Configuration', 'name CTE'],
    'Custom Plan Provider': ['Configuration', 'custom'],
    'Disk Usage': ['Cost', 'jit'],
    'Exact Heap Blocks': ['Cost', 'disk'],
    'Execution Time': ['Cost', 'heap actual'],
    'Filter': ['Configuration', 'filter'],
    'Foreign File': ['Configuration', 'time total actual'],
    'Foreign File Size': ['Configuration', 'foreign file'],
    'Foreign Program': ['Configuration', 'foreign file size'],
    'Group Count': ['Status', 'foreign program'],
    'Group Key': ['Configuration', 'group count'],
    'Hash Batches': ['Status', 'group key'],
    'Hash Buckets': ['Status', 'hash batch'],
    'Hash Key': ['Configuration', 'hash bucket'],
    'HashAgg Batches': ['Status', 'hash key'],
    'Heap Fetches': ['Status', 'aggregate batch'],
    'I/O Read Time': ['Cost', 'heap count'],
    'I/O Write Time': ['Cost', 'time read'],
    'Index Cond': ['Configuration', 'index'],
    'Index Name': ['Configuration', 'time write'],
    'Inner Unique': ['Status', 'index'],
    'JIT': ['Status', 'max one'],
    'Join Type': ['Configuration', 'join'],
    'Local Dirtied Blocks': ['Status', 'block dirty local'],
    'Local Hit Blocks': ['Status', 'block hit local'],
    'Local Read Blocks': ['Status', 'block read local'],
    'Local Written Blocks': ['Status', 'block written local'],
    'Lossy Heap Blocks': ['Cost', 'heap lossy actual'],
    'Operation': ['Configuration', 'command'],
    'Order By': ['Configuration', 'order'],
    'Original Hash Batches': ['Status', 'hash batch origin'],
    'Original Hash Buckets': ['Status', 'hash bucket origin'],
    'Output': ['Configuration', 'column returned'],
    'Parallel Aware': ['Status', 'parallel'],
    'Params Evaluated': ['Status', 'parallel parameter evaluated'],
    'Parent Relationship': ['Configuration', 'parent relationship'],
    'Partial Mode': ['Configuration', 'partial mode'],
    'Peak Memory Usage': ['Cost', 'memory peak'],
    'Peak Sort Space Used': ['Cost', 'memory sort peak'],
    'Plan Rows': ['Cardinality', 'row'],
    'Plan Width': ['Cardinality', 'width'],
    'Planned Partitions': ['Status', 'hash partition'],
    'Planning Time': ['Cost', 'time planning'],
    'Presorted Key': ['Configuration', 'presorted key'],
    'Query Identifier': ['Configuration', 'id'],
    'Query Text': ['Configuration', 'query'],
    'Recheck Cond': ['Configuration', 'condition redo'],
    'Relation': ['Configuration', 'name object'],
    'Relation Name': ['Configuration', 'name object'],
    'Remote SQL': ['Configuration', 'query remote'],
    'Repeatable Seed': ['Configuration', 'sample seed'],
    'Rows Removed by Conflict Filter': ['Cardinality', 'row dropped'],
    'Rows Removed by Filter': ['Cardinality', 'row dropped'],
    'Rows Removed by Index Recheck': ['Cardinality', 'row dropped'],
    'Rows Removed by Join Filter': ['Cardinality', 'row dropped'],
    'Sampling Method': ['Configuration', 'sample method'],
    'Sampling Parameters': ['Configuration', 'sample parameter'],
    'Scan Direction': ['Status', 'scan direction'],
    'Schema': ['Configuration', 'schema'],
    'Settings': ['Configuration', 'configuration'],
    'Shared Dirtied Blocks': ['Status', 'block dirty shared'],
    'Shared Hit Blocks': ['Status', 'block hit shared'],
    'Shared Read Blocks': ['Status', 'block read shared'],
    'Shared Written Blocks': ['Status', 'block written shared'],
    'Single Copy': ['Configuration', 'parallel single copy'],
    'Sort Key': ['Configuration', 'sort key'],
    'Sort Method': ['Status', 'sort method available'],
    'Sort Methods Used': ['Status', 'sort method'],
    'Sort Space Type': ['Status', 'sort space type'],
    'Sort Space Used': ['Cost', 'memory sort'],
    'Startup Cost': ['Cost', 'cost startup'],
    'Strategy': ['Status', 'aggregate strategy'],
    'Subplan Name': ['Configuration', 'name subplan'],
    'Subplans Removed': ['Status', 'eliminated'],
    'Table Function Name': ['Configuration', 'name table function'],
    'Temp Read Blocks': ['Status', 'block read temp'],
    'Temp Written Blocks': ['Status', 'block written temp'],
    'TID Cond': ['Configuration', 'condition CTE'],
    'Time': ['Cost', 'time'],
    'Total': ['Cost', 'time'],
    'Total Cost': ['Cost', 'cost'],
    'Trigger': ['Configuration', 'trigger'],
    'Tuples Inserted': ['Cardinality', 'row inserted'],
    'Tuplestore Name': ['Configuration', 'name tuplestore'],
    'WAL Bytes': ['Status', 'wal byte'],
    'WAL FPI': ['Status', 'wal fpi'],
    'WAL Records': ['Status', 'wal record'],
    'Workers': ['Status', 'worker']
}

global_properties_pg_result = {}

class PGTree:
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
        nodeType = json_subPlan.get('Node Type')
        if nodeType in nodetype_pg:
            nodeType = nodetype_pg.get(nodeType)
        else:
            raise Exception('Unknown node type: %s' % nodeType)

        new_node_properties = {}
        for key, value in properties_pg.items():
            if key in json_subPlan:
                new_node_properties[value[1]] = [value[0], json_subPlan.get(key)]

        newNode = TreeNode(nodeType, new_node_properties)

        for childPlan in json_subPlan.get('Plans') or []:
            newNode.add_child(self.handle(childPlan))
        
        return newNode


# It accepts the query plans via `EXPLAIN (FORMAT JSON, VERBOSE TRUE, SUMMARY TRUE) SELECT ...`
def parse_postgresql(raw_data):
    validated_data = raw_data.replace('+\n', '\n')
    validated_data = validated_data[validated_data.find('['):validated_data.rfind(']')+1]
    
    json_data = json.loads(validated_data)[0]
    root = None
    for key in json_data:
        if key == 'Plan':
            root = PGTree(json_data.get('Plan')).get_root()
        elif key in properties_pg:
            global_properties_pg_result[properties_pg[key][1]] = [properties_pg[key][0], json_data.get(key)]
        else:
            raise Exception('Unknown key: %s' % key)
    return [root, global_properties_pg_result]

