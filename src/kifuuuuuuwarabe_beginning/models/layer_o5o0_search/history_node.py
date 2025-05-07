import cshogi

from .tree_node import TreeNode


class HistoryNode(TreeNode):
    """読み筋ノード。
    """


    def __init__(self, parent_arg):
        super().__init__(self, parent_arg=parent_arg)
        self._move_hn               = 0             # ［指し手］
        self._cap_hn                = cshogi.NONE   # ［取った駒の型種類］
        self._value_hn              = 0             # ［局面評価値］
        self._comment_hn            = ''            # ［指し手へのコメント］
        self._termination_model_hn  = None          # ［終端外］オブジェクト

