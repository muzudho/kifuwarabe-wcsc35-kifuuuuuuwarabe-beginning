import cshogi

from ...layer_o1o0 import constants, SquareModel
from ...layer_o1o0o_9o0_table_helper import TableHelper
from ...layer_o2o0.nine_rank_side_perspective_model import NineRankSidePerspectiveModel
from ..negative_rule_model import NegativeRuleModel


class DoNotUpDogAndCatSideBySideModel(NegativeRuleModel):
    """号令［イヌとネコを横並びに上げるな］
    ［イヌを９段目に留めておく］意志を含む
    """


    def __init__(self, basketball_court_model):
        super().__init__(
                id          = 'do_not_up_dog_and_cat_side_by_side',
                label       = 'イヌとネコを横並びに上げるな',
                basketball_court_model  = basketball_court_model)


    def _on_node_exit_negative(self, move, table):
        """指す前に。
        """
        np = NineRankSidePerspectiveModel(table)
        moving_pt = TableHelper.get_moving_pt_from_move(move)
        is_drop = cshogi.move_is_drop(move)
        src_sq_obj = SquareModel(cshogi.move_from(move))
        dst_sq_obj = SquareModel(cshogi.move_to(move))

        if is_drop:
            # 打は順法の対象外
            return constants.mind.NOT_IN_THIS_CASE


        def _get_piece(sq):
            if sq is None:
                return None
            return table.piece(sq)


        def _do_not_alice_and_bob_side_by_side(alice, bob, moving_pt):
            # アリスなら。
            if moving_pt == alice:
                # 移動方向が上でなければ、［保留］
                if dst_sq_obj.sq != np.top_of_sq(src_sq_obj.sq):
                    return None

                # 右上、または左上にボブがいる。
                if np.ji_pc(bob) in [
                    _get_piece(np.top_right_of_sq(src_sq_obj.sq)),    # 右上
                    _get_piece(np.top_left_of_sq(src_sq_obj.sq))      # 左上
                ]:
                    # ［順法の意志無し］
                    return constants.mind.WILL_NOT

                # ［順法の意志有り］
                return constants.mind.WILL

            # ［保留］
            return None


        # イヌなら。
        result = _do_not_alice_and_bob_side_by_side(
                alice       = cshogi.GOLD,
                bob         = cshogi.SILVER,
                moving_pt   = moving_pt)
        #print(f'Debug: DoNotDogAndCatSideBySide: {table.move_number=} Gold {result=}')

        if result is not None:
            return result

        # ネコなら。
        result = _do_not_alice_and_bob_side_by_side(
                alice       = cshogi.SILVER,
                bob         = cshogi.GOLD,
                moving_pt   = moving_pt)
        #print(f'Debug: DoNotDogAndCatSideBySide: {table.move_number=} Dog {result=}')

        if result is not None:
            return result

        # 順法の対象外
        return constants.mind.NOT_IN_THIS_CASE
