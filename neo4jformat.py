import os
import json
from uplan import *

nodetype_neo4j = {
    'OrderedAggregation': ['Folder', 'Aggregate Order'],
    'Argument': ['Executor', 'Argument'],
    'ProduceResults': ['Executor', 'Argument'],
    'CacheProperties': ['Executor', 'Cache'],
    'CartesianProduct': ['Join', 'CartesianProduct'],
    'EmptyRow': ['Producer', 'Constant'],
    'Optional': ['Producer', 'Constant'],
    'Create': ['Consumer', 'Create'],
    'CreateConstraint': ['Consumer', 'Create'],
    'CreateIndex': ['Consumer', 'Create'],
    'Merge': ['Consumer', 'Create'],
    'Delete': ['Consumer', 'Delete'],
    'DetachDelete': ['Consumer', 'Delete'],
    'DropConstraint': ['Consumer', 'Delete'],
    'DropIndex': ['Consumer', 'Delete'],
    'RemoveLabels': ['Consumer', 'Delete'],
    'Eager': ['Executor', 'Eager'],
    'EagerAggregation': ['Executor', 'Eager'],
    'EmptyResult': ['Executor', 'Eager'],
    'ProcedureCall': ['Projector', 'Project'],
    'Anti': ['Folder', 'Exist'],
    'DoNothingIfExists(CONSTRAINT)': ['Folder', 'Exist'],
    'DoNothingIfExists(INDEX)': ['Folder', 'Exist'],
    'AllNodesScan': ['Producer', 'Full Table Scan'],
    'NodeHashJoin': ['Join', 'Hash Join'],
    'NodeLeftOuterHashJoin': ['Join', 'Hash Join'],
    'NodeRightOuterHashJoin': ['Join', 'Hash Join'],
    'ValueHashJoin': ['Join', 'Hash Join'],
    'NodeByIdSeek': ['Producer', 'Id Scan'],
    'IntersectionNodeByLabelsScan': ['Producer', 'Index Scan'],
    'MultiNodeIndexSeek': ['Producer', 'Index Scan'],
    'NodeIndexSeek': ['Producer', 'Index Scan'],
    'NodeIndexSeekByRange': ['Producer', 'Index Scan'],
    'NodeIndexScan': ['Producer', 'Index-only Scan'],
    'NodeUniqueIndexSeek': ['Producer', 'Index-only Scan'],
    'NodeIndexContainsScan': ['Producer', 'Index-only Scan Range'],
    'NodeIndexEndsWithScan': ['Producer', 'Index-only Scan Range'],
    'NodeUniqueIndexSeekByRange': ['Producer', 'Index-only Scan Range'],
    'SetLabels': ['Consumer', 'Insert'],
    'ExhaustiveLimit': ['Combinator', 'Limit'],
    'Limit': ['Combinator', 'Limit'],
    'LockingMerge': ['Join', 'Merge'],
    'AntiSemiApply': ['Join', 'Nested Loop'],
    'Apply': ['Join', 'Nested Loop'],
    'Foreach': ['Join', 'Nested Loop'],
    'LetAntiSemiApply': ['Join', 'Nested Loop'],
    'LetSelectOrAntiSemiApply': ['Join', 'Nested Loop'],
    'LetSelectOrSemiApply': ['Join', 'Nested Loop'],
    'LetSemiApply': ['Join', 'Nested Loop'],
    'RollUpApply': ['Join', 'Nested Loop'],
    'SelectOrAntiSemiApply': ['Join', 'Nested Loop'],
    'SelectOrSemiApply': ['Join', 'Nested Loop'],
    'SemiApply': ['Join', 'Nested Loop'],
    'ProjectEndpoints': ['Projector', 'Project'],
    'Projection': ['Projector', 'Project'],
    'NodeByLabelScan': ['Producer', 'Range Scan'],
    'UnionNodeByLabelsScan': ['Producer', 'Range Scan'],
    'DirectedAllRelationshipsScan': ['Join', 'Relation'],
    'DirectedRelationshipByIdSeek': ['Join', 'Relation'],
    'DirectedRelationshipIndexContainsScan': ['Join', 'Relation'],
    'DirectedRelationshipIndexEndsWithScan': ['Join', 'Relation'],
    'DirectedRelationshipIndexScan': ['Join', 'Relation'],
    'DirectedRelationshipIndexSeek': ['Join', 'Relation'],
    'DirectedRelationshipIndexSeekByRange': ['Join', 'Relation'],
    'DirectedRelationshipTypeScan': ['Join', 'Relation'],
    'DirectedUnionRelationshipTypesScan': ['Join', 'Relation'],
    'Expand(All)': ['Join', 'Relation'],
    'Expand(Into)': ['Join', 'Relation'],
    'OptionalExpand(All)': ['Join', 'Relation'],
    'OptionalExpand(Into)': ['Join', 'Relation'],
    'UndirectedAllRelationshipsScan': ['Join', 'Relation'],
    'UndirectedRelationshipByIdSeek': ['Join', 'Relation'],
    'UndirectedRelationshipIndexContainsScan': ['Join', 'Relation'],
    'UndirectedRelationshipIndexEndsWithScan': ['Join', 'Relation'],
    'UndirectedRelationshipIndexScan': ['Join', 'Relation'],
    'UndirectedRelationshipIndexSeek': ['Join', 'Relation'],
    'UndirectedRelationshipIndexSeekByRange': ['Join', 'Relation'],
    'UndirectedRelationshipTypeScan': ['Join', 'Relation'],
    'UndirectedUnionRelationshipTypesScan': ['Join', 'Relation'],
    'VarLengthExpand(All)': ['Join', 'Relation'],
    'VarLengthExpand(Into)': ['Join', 'Relation'],
    'VarLengthExpand(Pruning)': ['Join', 'Relation'],
    'VarLengthExpand(Pruning,BFS)': ['Join', 'Relation'],
    'LoadCSV': ['Producer', 'Remote Scan'],
    'ShortestPath': ['Folder', 'Shortest Path'],
    'ShowConstraints': ['Executor', 'Show'],
    'ShowFunctions': ['Executor', 'Show'],
    'ShowIndexes': ['Executor', 'Show'],
    'ShowProcedures': ['Executor', 'Show'],
    'ShowSettings': ['Executor', 'Show'],
    'ShowTransactions': ['Executor', 'Show'],
    'Skip': ['Executor', 'Skip'],
    'Sort': ['Combinator', 'Sort'],
    'PartialSort': ['Combinator', 'Sort Part'],
    'PartialTop': ['Combinator', 'Sort Part'],
    'Top': ['Combinator', 'Sort Part'],
    'TerminateTransactions': ['Executor', 'Terminate'],
    'TriadicBuild': ['Executor', 'Triadic'],
    'TriadicFilter': ['Executor', 'Triadic'],
    'TriadicSelection': ['Executor', 'Triadic'],
    'Union': ['Combinator', 'Union'],
    'AssertingMultiNodeIndexSeek': ['Combinator', 'Unique'],
    'AssertSameNode': ['Combinator', 'Unique'],
    'Distinct': ['Combinator', 'Unique'],
    'OrderedDistinct': ['Combinator', 'Unique'],
    'Unwind': ['Folder', 'Unwind'],
    'SetNodePropertiesFromMap': ['Consumer', 'Update'],
    'SetProperty': ['Consumer', 'Update'],
    'SetRelationshipPropertiesFromMap': ['Consumer', 'Update'],
    'NodeCountFromCountStore': ['Producer', 'Value Scan'],
    'RelationshipCountFromCountStore': ['Producer', 'Value Scan']
}

properties_neo4j = {
    'batch-size': ['Cardinality', 'width'],
    'bytecode': ['Status', 'bytecode'],
    'dbHits': ['Status', 'block hit local'],
    'Details': ['Configuration', 'information'],
    'EstimatedRows': ['Cardinality', 'row'],
    'GlobalMemory': ['Cost', 'memory'],
    'Id': ['Configuration', 'id'],
    'identifiers': ['Configuration', 'variable'],
    'Memory': ['Cost', 'memory'],
    'Order': ['Configuration', 'order'],
    'pageCacheHitRatio': ['Status', 'cache ratio'],
    'pageCacheHits': ['Status', 'cache hit'],
    'pageCacheMisses': ['Status', 'cache miss'],
    'PipelineInfo': ['Status', 'pipeline'],
    'rows': ['Cardinality', 'row actual'],
    'source': ['Configuration', 'name object'],
    #'string-representation': ['Stat', 'string representation'], # Disable it as it is too long and redundant
    'time': ['Cost', 'time'],
    'version': ['Configuration', 'version'],
    # Customized parameters
    'filter': ['Filter', 'filter']
}

global_properties_neo4j = {
    'planner': ['Configuration', 'cost model'],
    'planner-impl': ['Configuration', 'cost model'],
    'planner-version': ['Configuration', 'version'],
    'runtime': ['Configuration', 'version'],
    'runtime-impl': ['Configuration', 'version'],
    'runtime-version': ['Configuration', 'version']
}

global_properties_neo4j_result = {}

class Neo4jTree:
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
        nodeType = json_subPlan.get('operatorType').split('@')[0]
        new_node_properties = {}

        if nodeType in nodetype_neo4j:
            nodeType = nodetype_neo4j.get(nodeType)
        elif nodeType == 'Filter':
        # Operator FILTER is merged into FILTER property of its child node which should only be one
            if len(json_subPlan.get('children')) == 1:
                nodeType = nodetype_neo4j.get(json_subPlan.get('children')[0].get('operatorType').split('@')[0])
                details = None
                if json_subPlan.get('arguments'):
                    details = json_subPlan.get('arguments').get('Details')
                else:
                    details = json_subPlan.get('Details')
                new_node_properties[properties_neo4j['filter'][1]] = [properties_neo4j['filter'][0], details]
                json_subPlan = json_subPlan.get('children')[0]
            else:
                raise Exception('Unexpected: More than one child for Filter node: %s\n' % nodeType)
        else:
            raise Exception('Unknown node type: %s' % nodeType)

        if json_subPlan.get('arguments'):
            for key, value in properties_neo4j.items():
                if key in json_subPlan.get('arguments'):
                    new_node_properties[value[1]] = [value[0], json_subPlan.get('arguments').get(key)]
            for key, value in global_properties_neo4j.items():
                if key in json_subPlan.get('arguments'):
                    global_properties_neo4j_result[value[1]] = [value[0], json_subPlan.get('arguments').get(key)]

        newNode = TreeNode(nodeType, new_node_properties)

        for childPlan in json_subPlan.get('children') or []:
            newNode.add_child(self.handle(childPlan))
        
        return newNode


# It accepts query plans from `summary.plan` field of the result for execution `EXPLAIN <query>` in Neo4j Web-UI `http://localhost:7474/browser/`.
def parse_neo4j(raw_data):
    json_data = json.loads(raw_data)
    root = Neo4jTree(json_data).get_root()
    return [root, global_properties_neo4j_result]