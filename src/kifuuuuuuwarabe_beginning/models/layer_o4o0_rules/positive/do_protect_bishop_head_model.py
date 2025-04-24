import cshogi

from ...layer_o1o0 import constants, SquareModel
from ...layer_o2o0.nine_rank_side_perspective_model import NineRankSidePerspectiveModel
from ..positive_rule_model import PositiveRuleModel


class DoProtectBishopHeadModel(PositiveRuleModel):
    """訓令［ゾウの頭を守れ］

    ７六歩、７七角の２手を入れること。
    """


    def __init__(self, basketball_court_model):
        super().__init__(
                id          = 'do_protect_bishop_head',
                label       = 'ゾウの頭を守れ',
                basketball_court_model  = basketball_court_model)


    ##############################
    # MARK: オーバーライドメソッド
    ##############################

    def _remove_rule_before_branches_prm(self, remaining_moves, table):
        """枝前削除条件。
        真なら、このルールをリストから除外します。
        """
        np = NineRankSidePerspectiveModel(table)

        # 事前ケース分岐）［自ゾウが７七にいる］ならこのルールを消す。
        return table.piece(np.masu(77)) == np.ji_pc(cshogi.BISHOP)


    def _before_move_prm(self, move, table):
        """指す前にこの手に決める。

        Returns
        -------
        is_better_move : bool
            指させたい手なら真。
        """
        np = NineRankSidePerspectiveModel(table)

        src_sq_obj = SquareModel(cshogi.move_from(move))
        dst_sq_obj = SquareModel(cshogi.move_to(move))

        # NOTE 後ろ向き探索だからか、

        # ［７六歩］なら、それを選ぶ。
        # print(f"（２）［７六歩］があれば、それを選ぶ。： {np.masu(76)=} {table.piece(src_sq_obj.sq) == np.ji_pc(cshogi.PAWN) and dst_sq_obj.sq == np.masu(76)}")
        if table.piece(src_sq_obj.sq) == np.ji_pc(cshogi.PAWN) and dst_sq_obj.sq == np.masu(76):
            return True

        # # # FIXME ［７六歩］が指せる局面で、［６六歩］を指してしまう。なぜか両方のフラグが有効になっている。後ろ向き探索だから？
        # # # FIXME 歩を取られるのが嫌なのか、［６六歩］を指さないことがある。
        # # # # ［６六歩］なら、それを選ぶ。
        # # # # print(f"［７六歩］無し： {table.sfen()=}")
        # # # # print(f"（３）［６六歩］があれば、それを選ぶ。： {np.masu(66)=} {table.piece(src_sq_obj.sq) == np.ji_pc(cshogi.PAWN) and dst_sq_obj.sq == np.masu(66)}")
        # if table.piece(src_sq_obj.sq) == np.ji_pc(cshogi.PAWN) and dst_sq_obj.sq == np.masu(66):
        #     # print(f"［６六歩］有り： {table.sfen()=}")
        #     return True
        # # if table.piece(np.masu(34)) == np.mars_pc(cshogi.PAWN) and table.piece(src_sq_obj.sq) == np.ji_pc(cshogi.PAWN) and dst_sq_obj.sq == np.masu(66):
        # #     # print(f"［６六歩］有り： {table.sfen()=}")
        # #     return True

        # ［７七角］なら、それを選ぶ。
        # print(f"（１）［７七角］があれば、それを選ぶ。： {np.masu(77)=} {table.piece(src_sq_obj.sq) == np.ji_pc(cshogi.BISHOP) and dst_sq_obj.sq == np.masu(77)}")
        if table.piece(src_sq_obj.sq) == np.ji_pc(cshogi.BISHOP) and dst_sq_obj.sq == np.masu(77):
            return True
        
        # print(f"─")

        # それ以外は無視
        return False


    ##############################
    # MARK: オーバーライドメソッド
    ##############################

    def _remove_rule_before_branches_prm(self, remaining_moves, table):
        """枝前削除条件。
        真なら、このルールをリストから除外します。
        """

        np = NineRankSidePerspectiveModel(table)

        # 事前ケース分岐）［自ゾウが７七にいる］ならこのルールを消す。
        return table.piece(np.masu(77)) == np.ji_pc(cshogi.BISHOP)
