from ..models import constants


class MatchOperation():


    def __init__(self, id, label, config_doc):
        self._id = id
        self._label = label
        self._config_doc = config_doc

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
        return self._config_doc['march_operations'][self._id]


    @property
    def is_activate(self):
        """［アイドリング］状態にある［行進演算］が、
        ［オンゴーイング］状態に遷移するためのフラグです。
        """
        return self._is_activate


    @property
    def is_removed(self):
        return self._is_removed


    def after_best_moving_when_idling(self, move, table):
        """（アイドリング中の行進演算について）指す手の確定時。
        """
        pass


    def after_best_moving(self, move, table):
        """指す手の確定時。
        """
        pass


    def before_move_o1(self, will_play_moves, table):
        if self.is_enabled:
            for i in range(len(will_play_moves))[::-1]:     # `[::-1]` - 逆順
                m = will_play_moves[i]
                mind = self.before_move(m, table)
                if mind == constants.mind.WILL_NOT:
                    del will_play_moves[i]

        return will_play_moves


    def before_move(self, move, table):
        """指す前に。
        """
        pass
