class TreeNodeModel:


    @staticmethod
    def create_tree_node_model(parent_arg):
        return TreeNodeModel(parent_arg=parent_arg)


    def __init__(self, parent_arg):
        self._parent_tn = parent_arg
        self._children_tn = []


    @property
    def parent_tn(self):
        return self._parent_tn


    @property
    def children_tn(self):
        return self._children_tn


    def append_child_tn(self, value):
        self._children_tn.append(value)


    def get_depth_tn(self):
        if self._parent_tn is None:
            return 1
        return self._parent_tn.get_depth_tn() + 1
