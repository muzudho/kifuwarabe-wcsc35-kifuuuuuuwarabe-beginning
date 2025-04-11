from ..layer_o1o0 import constants


class NegativeRuleModel():


    def __init__(self, id, label, basketball_court_model):
        self._id = id
        self._label = label
        self._basketball_court_model = basketball_court_model

        self._is_activate = False
        self._is_removed = False


    @property
    def id(self):
        """識別子。
        設定ファイルなどで利用する名前。
        """
        return self._label


    @property
    def label(self):
        """名前。
        人に読めるテキスト。
        """
        return self._label


    @property
    def is_enabled(self):
        return self._basketball_court_model.config_doc['gourei_commands'][self._id]


    @property
    def is_activate(self):
        """［アイドリング］状態にある［号令］が、
        ［オンゴーイング］状態に遷移するためのフラグです。
        """
        return self._is_activate


    @property
    def is_removed(self):
        return self._is_removed


    def after_best_moving_in_idling(self, move, table):
        """（アイドリング中の号令について）指す手の確定時。
        """
        pass


    def after_best_moving(self, move, table):
        """指す手の確定時。
        """
        pass


    def before_move_o1o1x(self, remaining_moves, table):
        if self.is_enabled:
            for i in range(len(remaining_moves))[::-1]:     # `[::-1]` - 逆順
                m = remaining_moves[i]
                mind = self.before_move(m, table)
                if mind == constants.mind.WILL_NOT:
                    del remaining_moves[i]

        return remaining_moves


    def before_move(self, move, table):
        """指す前に。
        """
        pass
