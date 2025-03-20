import cshogi

from ..models_o1x import constants, Square
from ..models_o2x.nine_rank_side_perspective import NineRankSidePerspective
from .negative_rule import NegativeRule


class DoNotMoveUntilRookMoves(NegativeRule):
    """行進［キリンが動くまで動くな］
    ［飛車道を開ける］意志
    """


    def __init__(self, config_doc):
        super().__init__(
                id          = 'do_not_move_until_rook_moves',
                label       = 'キリンが動くまで動くな',
                config_doc  = config_doc)


    def before_move(self, move, table):
        """指す前に。
        """
        pen = NineRankSidePerspective(table)

        dst_sq_obj = Square(cshogi.move_to(move))
        moved_pt = cshogi.move_from_piece_type(move)

        # キリンが２八にいる
        if table.piece(pen.masu(28)) != pen.ji_pc(cshogi.ROOK):
            # そうでなければ対象外
            return constants.mind.NOT_IN_THIS_CASE

        # 移動先は８段目だ
        if dst_sq_obj.rank != pen.dan(8):
            # そうでなければ対象外
            return constants.mind.NOT_IN_THIS_CASE

        # 動かした駒はキリン以外だ
        if moved_pt == cshogi.ROOK:
            # そうでなければ対象外
            return constants.mind.NOT_IN_THIS_CASE

        # 動かした駒がライオン、イヌ、ネコのいずれかなら
        if moved_pt in [cshogi.KING, cshogi.GOLD, cshogi.SILVER]:
            # 意志無し
            return constants.mind.WILL_NOT

        # # 動かした駒が金なら
        # if moved_pt == cshogi.GOLD:
        #     # ５筋以右にある金なら
        #     e1 = cmp.swap(src_sq_obj.file, pen.suji(5))
        #     if e1[0] <= e1[1]:
        #         # 動かしたら意志なし
        #         return constants.mind.WILL_NOT

        #     # それ以外の金なら、左の方以外に動かしたら意志なし
        #     e1 = cmp.swap(src_sq_obj.file, dst_sq_obj.file)
        #     if e1[0] < e1[1]:
        #         return constants.mind.WILL_NOT
            
        #     # 左の方に動かしたのなら、まあ、対象外
        #     return constants.mind.NOT_IN_THIS_CASE

        # # 動かした駒が銀なら
        # if moved_pt == cshogi.SILVER:
        #     # ５筋以右にある銀を動かしたなら
        #     e1 = cmp.swap(src_sq_obj.file, pen.suji(5))
        #     if e1[0] <= e1[1]:
        #         # 意志なし
        #         return constants.mind.WILL_NOT

        #     # それ以外の銀を、元位置より右の方に動かしたら意志なし
        #     e1 = cmp.swap(src_sq_obj.file, dst_sq_obj.file)
        #     if e1[0] > e1[1]:
        #         return constants.mind.WILL_NOT
            
        #     # 位左の方に動かしたのなら、まあ、対象外
        #     return constants.mind.NOT_IN_THIS_CASE

        # それ以外なら意志を残している
        return constants.mind.WILL
