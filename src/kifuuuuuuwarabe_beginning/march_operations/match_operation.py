class MatchOperation():


    def __init__(self):
        self._name = ''
        self._is_removed = False
        self._is_disabled = False


    @property
    def name(self):
        """名前。
        人に読めるテキスト。
        """
        return self._name


    @property
    def is_removed(self):
        return self._is_removed


    @property
    def is_disabled(self):
        return self._is_disabled


    def on_best_move_played(self, move, table, config_doc):
        """指す手の確定時。
        """
        pass
