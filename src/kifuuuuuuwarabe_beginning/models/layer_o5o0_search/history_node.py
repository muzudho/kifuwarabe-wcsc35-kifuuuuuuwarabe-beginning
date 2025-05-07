from .tree_node import TreeNode


class HistoryNode(TreeNode):
    """読み筋ノード。
    """


    def __init__(self, parent_arg):
        super().__init__(self, parent_arg=parent_arg)
