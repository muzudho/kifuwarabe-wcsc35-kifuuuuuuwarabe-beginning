import cshogi

from ..models_o1x import constants, Square
from ..models_o2x.nine_rank_side_perspective_model import NineRankSidePerspectiveModel
from .negative_rule import NegativeRule


class DoNotUpToRank6(NegativeRule):
    """行進［６段目に上がるな］
    ［玉が２八に行くまで歩を突かない］意志
    """


    def __init__(self, config_doc):
        super().__init__(
                id          = 'do_not_up_to_rank_6',
                label       = '６段目に上がるな',
                config_doc  = config_doc)


    def before_move_o1o1x(self, remaining_moves, table):
        if self.is_enabled:

            np = NineRankSidePerspectiveModel(table)

            # 自ライオンが２八にいる
            if table.piece(np.masu(28)) == np.ji_pc(cshogi.KING):
                # このオブジェクトを除外
                self._is_removed = True

                # 対象外
                return remaining_moves

            for i in range(len(remaining_moves))[::-1]:     # `[::-1]` - 逆順
                m = remaining_moves[i]
                mind = self.before_move(m, table)
                if mind == constants.mind.WILL_NOT:
                    del remaining_moves[i]

        return remaining_moves


    def before_move(self, move, table):
        """指す前に。
        """
        np = NineRankSidePerspectiveModel(table)

        dst_sq_obj = Square(cshogi.move_to(move))

        # # 自キリンが２八にいる
        # if table.piece(np.masu(28)) != np.ji_pc(cshogi.ROOK):
        #     # そうでなければ対象外
        #     return constants.mind.NOT_IN_THIS_CASE

        # 移動先は６段目だ
        if dst_sq_obj.rank != np.dan(6):
            # そうでなければ意志を残している
            return constants.mind.WILL

        # 意志なし
        return constants.mind.WILL_NOT
