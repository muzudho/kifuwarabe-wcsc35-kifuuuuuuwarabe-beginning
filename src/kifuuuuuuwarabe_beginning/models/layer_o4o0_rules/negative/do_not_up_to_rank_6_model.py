import cshogi

from ...layer_o1o0 import constants, SquareModel
from ...layer_o2o0.nine_rank_side_perspective_model import NineRankSidePerspectiveModel
from ..negative_rule_model import NegativeRuleModel


class DoNotUpToRank6Model(NegativeRuleModel):
    """号令［６段目に上がるな］
    ［玉が２八に行くまで歩を突かない］意志。
    ただし、７六に歩を突くのはＯｋ。
    """


    def __init__(self, basketball_court_model):
        super().__init__(
                id          = 'do_not_up_to_rank_6',
                label       = '６段目に上がるな',
                basketball_court_model  = basketball_court_model)


    def _remove_rule_before_branches_nrm(self, remaining_moves, table):
        """枝前削除条件。
        真なら、このルールをリストから除外します。
        """
        np = NineRankSidePerspectiveModel(table)

        # TODO ［入城終了］フラグが欲しい。
        # （事前リムーブ分岐）自ライオンが２八にいる
        return table.piece(np.masu(28)) == np.ji_pc(cshogi.KING)


    def _before_move_nrm(self, move, table):
        """指す前に。
        """
        np = NineRankSidePerspectiveModel(table)

        src_sq_obj = SquareModel(cshogi.move_from(move))
        dst_sq_obj = SquareModel(cshogi.move_to(move))

        # 移動先は６段目ではない。
        if dst_sq_obj.rank != np.dan(6):
            # そうでなければ意志を残している
            return constants.mind.WILL

        # （角道を止める手）７六歩はポジティブ・ルールの方でやるから、ここではやらない。
        if (
                dst_sq_obj.sq == np.masu(66)    # 動いた先は６六で。
            and cshogi.piece_to_piece_type(table.piece(src_sq_obj.sq)) == cshogi.PAWN   # 動いた駒は歩だ。
            and (table.piece(np.masu(77)) == np.ji_pc(cshogi.BISHOP) or table.piece(np.masu(88)) == np.ji_pc(cshogi.BISHOP))    # 自ゾウが７七または８八にいる。
            ):
            # ６六に歩を突くのはＯｋ。
            return constants.mind.WILL

        # 意志なし
        return constants.mind.WILL_NOT
