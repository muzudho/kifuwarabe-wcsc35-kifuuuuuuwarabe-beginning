import cshogi

from ...layer_o1o0 import constants, SquareModel
from ...layer_o2o0.nine_rank_side_perspective_model import NineRankSidePerspectiveModel
from ..negative_rule_model import NegativeRuleModel


class DoNotLetDogClimb6RankModel(NegativeRuleModel):
    """号令［犬を６段目に登らせるな］
    意図：犬は自陣を守っていてほしい。
    """


    def __init__(self, basketball_court_model):
        super().__init__(
                id          = 'do_not_let_dog_climb_6_rank',
                label       = '犬を６段目に登らせるな',
                basketball_court_model  = basketball_court_model)


    def _remove_rule_on_node_entry_negative(self, remaining_moves, table):
        """ノード来訪時削除条件。
        真なら、このルールをリストから除外します。
        """
        np = NineRankSidePerspectiveModel(table)

        # TODO ［入城終了］フラグが欲しい。
        # （事前リムーブ分岐）自ライオンが２八にいる
        return table.piece(np.masu(28)) == np.ji_pc(cshogi.KING)


    def _on_node_exit_negative(self, move, table):
        """指す前に。
        """
        np = NineRankSidePerspectiveModel(table)

        src_sq_obj = SquareModel(cshogi.move_from(move))

        if cshogi.piece_to_piece_type(table.piece(src_sq_obj.sq)) != cshogi.GOLD:   # 動いた駒は［犬］ではない。
            return constants.mind.NOT_IN_THIS_CASE                                  # 対象外。

        if src_sq_obj.rank != np.dan(7):            # ［移動元］は７段目ではない。
            return constants.mind.NOT_IN_THIS_CASE  # 対象外。

        dst_sq_obj = SquareModel(cshogi.move_to(move))

        if dst_sq_obj.rank != np.dan(6):            # ［移動先］は６段目ではない。
            return constants.mind.NOT_IN_THIS_CASE  # 対象外。

        # 意志なし
        return constants.mind.WILL_NOT
