class TreeNode(object):
    def __init__(self, nodeType, properties = None):
        self.nodeType = nodeType
        self.children = []
        self.parent = None

        # To avoid the issue: https://stackoverflow.com/questions/13389325/why-do-two-class-instances-appear-to-be-sharing-the-same-data
        if properties is None:
            self.properties = {}
        else:
            self.properties = properties

        #TODO: add properties: raw data

    def add_child(self, obj):
        if isinstance(obj, TreeNode):
            self.children.append(obj)
            obj.parent = self

    def add_children(self, objs):
        if objs is not None:
            assert isinstance(objs, list)
            for obj in objs:
                self.add_child(obj)

    def set_prop(self, dict, value):
        key = dict[1]
        category = dict[0]
        self.properties[key] = [category, value]

    def get_prop(self, key):
        return self.properties[key]

    def update_prop(self, prop):
        self.properties.update(prop)

    def __str__(self, level=0):
        ret = "\t"*level+str(self.nodeType[0])+"->"+str(self.nodeType[1])+"\n"
        if 'row' in self.properties:
            ret += "\t"*(level)+"row: "+str(self.properties['row'][1])+"\n"
        if 'name object' in self.properties:
            ret += "\t"*(level)+"name object: "+str(self.properties['name object'][1])+"\n"
        for child in self.children:
            ret += child.__str__(level+1)
        return ret

    def to_json(self):
        json_node = {}
        json_node['Operation'] = self.nodeType[0]+"->"+self.nodeType[1]
        for key in self.properties:
            json_node[self.properties[key][0]+"->"+key] = self.properties[key][1]
        json_node['children'] = []
        for child in self.children:
            json_node['children'].append(child.to_json())
        if json_node['children'] == []:
            del json_node['children']
        return json_node

    def to_simplified_json(self):
        json_node = {}
        json_node['Operation'] = self.nodeType[0]+"->"+self.nodeType[1]
        json_node['children'] = []
        for child in self.children:
            json_node['children'].append(child.to_simplified_json())
        if json_node['children'] == []:
            del json_node['children']
        return json_node
    
    def to_json_qpg(self):
        excluded_properties = ['cost', 'name object', 'filter', 'filtered', 'column used', 'cost read', 'cost eval', 'cost join', 'row', 'row read', 'id', 'information', 'column returned', 'alias', 'schema', 'width', 'cost startup']
        json_node = {}
        json_node['Operation'] = self.nodeType[0]+"->"+self.nodeType[1]
        for key in self.properties:
            if key not in excluded_properties:
                json_node[self.properties[key][0]+"->"+key] = self.properties[key][1]
        json_node['children'] = []
        for child in self.children:
            json_node['children'].append(child.to_json_qpg())
        if json_node['children'] == []:
            del json_node['children']
        return json_node
    
    def extract_cardinality_cert(self):
        # DFS search
        if 'row' in self.properties:
            return self.properties['row'][1]
        else:
            for child in self.children:
                row = child.extract_cardinality_cert()
                if row is not None:
                    return row
            return '0'