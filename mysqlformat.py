import os
import json
from uplan import *

nodetype_mysql = {
    'buffer_result': ['Executor', 'Cache'],
    'const': ['Producer', 'Constant'],
    'system': ['Producer', 'Constant'],
    'ALL': ['Producer', 'Full Table Scan'],
    'table': ['Producer', 'Full Table Scan'],
    'grouping_operation': ['Folder', 'Group'],
    'index_merge': ['Join', 'Index Merge'],
    'eq_ref': ['Producer', 'Index Scan'],
    'fulltext': ['Producer', 'Index Scan'],
    'index_subquery': ['Producer', 'Index Scan'],
    'ref': ['Producer', 'Index Scan'],
    'ref_or_null': ['Producer', 'Index Scan'],
    'unique_subquery': ['Producer', 'Index Scan'],
    'index': ['Producer', 'Index-Only Scan'],
    'materialized_from_subquery': ['Executor', 'Materialize'],
    'nested_loop': ['Join', 'Nested Loop'],
    'range': ['Producer', 'Range Scan'],
    'ordering_operation': ['Combinator', 'Sort'],
    'attached_subqueries': ['Producer', 'Subquery Scan'],
    'having_subqueries': ['Producer', 'Subquery Scan'],
    'select_list_subqueries': ['Producer', 'Subquery Scan'],
    'optimized_away_subqueries': ['Producer', 'Subquery Scan'],
    'union_result': ['Combinator', 'Union'],
    'duplicates_removal': ['Combinator', 'Unique']
}

properties_mysql = {
    'attached_condition': ['Configuration', 'filter'],
    'cacheable': ['Status', 'cachable'],
    'cost_info': ['Cost', 'cost'],
    'data_read_per_join': ['Cardinality', 'row read'],
    'dependent': ['Status', 'depend'],
    'eval_cost': ['Cost', 'cost eval'],
    'filtered': ['Status', 'filtered'],
    'key': ['Status', 'index used'],
    'key_length': ['Status', 'index length'],
    'possible_keys': ['Status', 'index available'],
    'prefix_cost': ['Cost', 'cost join'],
    'query_cost': ['Cost', 'cost'],
    'read_cost': ['Cost', 'cost read'],
    'ref': ['Configuration', 'index'],
    'rows_examined_per_scan': ['Cardinality', 'row read'],
    'rows_produced_per_join': ['Cardinality', 'row'],
    'sort_cost': ['Cost', 'cost sort'],
    'table_name': ['Configuration', 'name object'],
    'used_columns': ['Status', 'column used'],
    'used_key_parts': ['Status', 'index used'],
    'using_filesort': ['Status', 'filesort'],
    'using_temporary_table': ['Status', 'temp table']
}

global_properties_mysql_result = {}

# Reference: https://github.com/mysql/mysql-workbench/blob/8.0/plugins/wb.query.analysis/explain_renderer.py
# handle_**(） return a list of TreeNode
# generate_**(） return a TreeNode
class MySQLTree:
    def __init__(self, json):
        self._json = json
        nodes = self.handle(json)
        if not nodes:
            nodes.append(TreeNode(['Error', 'Not valid query plan']))
        self._root = nodes[0]

    def get_root(self):
        return self._root

    def unexpected(self, node, context=""):
        if context:
            raise Exception("Unexpected: While parsing JSON output: unexpected node in %s: %s\n" % (context, node))
        else:
            raise Exception("Unexpected: While parsing JSON output: unexpected node: %s\n" % node)
 
    def generate_table_node(self, table):
        newNode = TreeNode(nodetype_mysql[table.get('access_type')])

        for key in table:
            if key == 'cost_info':
                for cost_key in table[key]:
                    newNode.set_prop(properties_mysql[cost_key], table[key][cost_key])
            elif key not in ('access_type', 'materialized_from_subquery', 'attached_subqueries'):
                if key in properties_mysql:
                    newNode.set_prop(properties_mysql[key], table[key])

        return newNode

    def generate_subquery_node(self, name, subqueries, properties):
        newNode = TreeNode(nodetype_mysql[name], properties)
        newNode.add_children(subqueries)

        return newNode

    def generate_nested_loop_node(self, children, row):
        newNode = TreeNode(nodetype_mysql['nested_loop'])
        newNode.add_children(children)
        newNode.set_prop(properties_mysql['rows_produced_per_join'], row)
        
        return newNode

    def generate_materialized_join_node(self, name, nested_loop, cost_info, properties):
        newNode = TreeNode(nodetype_mysql[name])
        if properties.get("using_temporary_table"):
            newNode.set_prop(properties_mysql['using_temporary_table'], True)

        newNode.add_child(nested_loop)
        if cost_info:
            newNode.set_prop(properties_mysql["cost_info"], float(cost_info.get("read_cost", 0)) + float(cost_info.get("eval_cost", 0)))
        return newNode

    def generate_operation_node(self, name, children, cost_info = None, properties = None):
        if name in ("grouping_operation", "duplicates_removal", "ordering_operation"):
            newNode = TreeNode(nodetype_mysql[name])
            newNode.add_children(children)
        else:
            self.unexpected("Unknown operation: %s\n" % name)

        if cost_info:
            cost_sum = 0.0
            for key in cost_info:
                cost_sum += float(cost_info[key])
            newNode.set_prop(properties_mysql["cost_info"], cost_sum)

        if properties.get("using_temporary_table", False):
            newNode.set_prop(properties_mysql['using_temporary_table'], True)
        if properties.get("using_filesort", False):
            newNode.set_prop(properties_mysql['using_filesort'], True)

        return newNode

    def handle_table(self, table):
        newNodes = []

        # rows_examined_per_scan: how many rows are examined per scan of the table.
        # rows_produced_per_join: how many rows are produced after filter or join.
        if 'rows_examined_per_scan' not in table:
            table['rows_examined_per_scan'] = (table.get('rows') or 0)
        if 'rows_produced_per_join' not in table:
            table['rows_produced_per_join'] = (table.get('rows') or 0) * int(float(table.get('filtered', 0))) / 100

        newTable = self.generate_table_node(table)
        newNodes.append(newTable)

        # Put subqueries into a sibling node.
        materialized_from_subquery = table.get("materialized_from_subquery")
        if materialized_from_subquery:
            materialized_from_subquery_node = self.handle_materialized_from_subquery(materialized_from_subquery)
            newNodes.extend(materialized_from_subquery_node)

        attached_subqueries_ = table.get("attached_subqueries")
        if attached_subqueries_:
            attached_subqueries = self.handle_attached_subqueries("attached_subqueries", attached_subqueries_)
            newNodes.extend(attached_subqueries)

        return newNodes

    def handle_nested_loop(self, data):
        newNodes = []

        # For all children of the nested loop, we generate a nested node for any pair of children.
        for node in data:
            if type(node) is dict and len(node) == 1 and 'table' in node:
                newNodes.extend(self.handle_table(node['table']))
            elif type(node) is dict and len(node) == 1 and 'duplicates_removal' in node:
                newNodes.extend(self.handle_query_block('duplicates_removal', node['duplicates_removal']))
            else:
                self.unexpected(node, "nested_loop")

            if len(newNodes) >= 2:
                row = node['table']['rows_produced_per_join'] # the number of produced rows in the right table is the nubmer of rows after the join
                loop_node = self.generate_nested_loop_node(newNodes, row)
                newNodes = [loop_node]

        return newNodes

    def handle_attached_subqueries(self, name, subquery_list):
        subqueries = []
        for data in subquery_list:
            qblock = []
            properties = {}
            for key, value in list(data.items()):
                if key == "query_block":
                    qblock = self.handle_query_block(key, value)
                    if "query_cost" in value:
                        properties[properties_mysql["query_cost"][1]] = [properties_mysql["query_cost"][0], value['cost_info']['query_cost']]   # merge the cost info in the query block into the subquery node
                elif key in ("dependent", "cacheable", "using_temporary_table"):
                    properties[properties_mysql[key][1]] = [properties_mysql[key][0], value]
                elif key == "table": # handles bug #18997475
                    qblock = self.handle_table(value)
                else:
                    self.unexpected(key, name)
            subqueries.extend(qblock)
        return [self.generate_subquery_node(name, subqueries, properties)]

    def handle_materialized_from_subquery(self, data):
        newNodes = []
        properties = {}
        for key, value in list(data.items()):
            if key == "query_block":
                inner_qblock = self.handle_query_block(key, value)
                newNodes.extend(inner_qblock)
            elif key in ("dependent", "cacheable", "using_temporary_table"):
                properties[properties_mysql[key][1]] = [properties_mysql[key][0], value]
            else:
                self.unexpected(key, "materialized_from_subquery")
        
        newNode = TreeNode(nodetype_mysql["materialized_from_subquery"], properties)
        newNode.add_children(newNodes)
        return [newNode]

    def handle_union_result(self, name, data):
        properties = {}
        qblocks = []
        for key, value in list(data.items()):
            if key in ("using_temporary_table", "access_type", "table_name"):
                properties[key] = value
            elif key == "query_specifications":
                for qspec in value:
                    qblocks.extend(self.handle_query_block("query_block", qspec.get("query_block")))
            else:
                self.unexpected(key, name)
        return [self.generate_subquery_node(name, qblocks, properties)]

    # Normally, we ignore the node of query block, and show its children dircetly.
    # Other nodes, such as aggregation, buffer_result, are also applicable for this function.
    def handle_query_block(self, name, data):
        newNodes = []
        cost_info = None
        properties = {}

        # Parse the children of query block
        for key, value in list(data.items()):
            if key == "nested_loop":
                newNodes.extend(self.handle_nested_loop(value))
            elif key == "table":
                newNodes.extend(self.handle_table(value))            
            elif key in ("grouping_operation", "ordering_operation", "duplicates_removal"):
                value['cost_info'] = cost_info
                newNodes.extend(self.handle_query_block(key, value))
            elif key in ("using_temporary_table", "using_filesort", "dependent"):
                properties[key] = value
            elif key == "cost_info":
                cost_info = value
            elif key == "union_result":
                newNodes.extend(self.handle_union_result(key, value))
            elif key == "select_list_subqueries":
                newNodes.extend(self.handle_attached_subqueries(key, value)) # select (select ...) from ...
            elif key == "having_subqueries":
                newNodes.extend(self.handle_attached_subqueries(key, value))
            elif key == "buffer_result":
                newNodes.extend(self.handle_query_block(key, value)) # buffer_result is a materialized JOIN
            elif key == "select_id":
                pass
            elif key == "message":
                pass
            elif key == "optimized_away_subqueries":
                pass
            else:
                self.unexpected(key, name)

        # Handle the other nodes
        if name == "query_block":
            return newNodes
        elif name in ("grouping_operation", "ordering_operation", "duplicates_removal"):
            return [self.generate_operation_node(name, newNodes, cost_info, properties)]
        elif name == "buffer_result":
            return [self.generate_materialized_join_node(name, data, cost_info, properties)]
        else:
            raise Exception("Unexpected query_block name: " + name)
            

    def handle(self, json_data):
        output = []
        for key, value in list(json_data.items()):
            if key == "query_block":
                output.extend(self.handle_query_block(key, value))
        return output


# It accepts the query plans via `EXPLAIN FORMAT=JSON SELECT ...`.
def parse_mysql(raw_data):
    validated_data = raw_data.replace('\\n', '\n')
    validated_data = validated_data[validated_data.find('{'):validated_data.rfind('}')+1]
    
    json_data = json.loads(validated_data)
    root = MySQLTree(json_data).get_root()
    return [root, global_properties_mysql_result]
