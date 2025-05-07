class TreeNode:


    @staticmethod
    def create_tree_node(parent_arg):
        return TreeNode(parent_arg=parent_arg)


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
