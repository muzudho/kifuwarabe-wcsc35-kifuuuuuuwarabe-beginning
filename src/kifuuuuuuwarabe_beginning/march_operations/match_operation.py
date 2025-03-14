class MatchOperation():


    def __init__(self):
        self._name = ''
        self._is_activate = False
        self._is_removed = False


    @property
    def name(self):
        """名前。
        人に読めるテキスト。
        """
        return self._name


    @property
    def is_activate(self):
        """［アイドリング］状態にある［行進演算］が、
        ［オンゴーイング］状態に遷移するためのフラグです。
        """
        return self._is_activate


    @property
    def is_removed(self):
        return self._is_removed


    def on_best_move_played_when_idling(self, move, table, config_doc):
        """（アイドリング中の行進演算について）指す手の確定時。
        """
        pass


    def on_best_move_played(self, move, table, config_doc):
        """指す手の確定時。
        """
        pass
