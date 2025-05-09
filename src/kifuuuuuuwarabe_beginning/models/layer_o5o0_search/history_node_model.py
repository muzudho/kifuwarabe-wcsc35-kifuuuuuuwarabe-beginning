import cshogi

from .tree_node_model import TreeNodeModel


class HistoryNodeModel(TreeNodeModel):
    """読み筋ノード。
    """


    def __init__(
            self,
            parent_arg,
            move_arg,
            cap_arg,
            value_arg,
            comment_arg):
        super().__init__(parent_arg=parent_arg)
        self._move_hn               = move_arg      # ［指し手］
        self._cap_hn                = cap_arg       # ［取った駒の型種類］
        self._value_hn              = value_arg     # ［局面評価値］
        self._comment_hn            = comment_arg   # ［指し手へのコメント］
        self._termination_model_hn  = None          # ［終端外］オブジェクト


    @property
    def move_hn(self):
        return self._move_hn


    @property
    def cap_hn(self):
        return self._cap_hn


    @property
    def value_hn(self):
        return self._value_hn


    @property
    def comment_hn(self):
        return self._comment_hn


    def set_node_hn(
            self,
            move_arg,
            cap_arg,
            value_arg,
            comment_arg):
        """枝を生やす。
        """
        self._move_hn       = move_arg
        self._cap_hn        = cap_arg
        self._value_hn      = value_arg
        self._comment_hn    = comment_arg
