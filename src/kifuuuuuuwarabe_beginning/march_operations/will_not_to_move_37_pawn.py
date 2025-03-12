import cshogi
import sys

from .. import Mind
from ..models import Square
from ..sente_perspective import Ban, Helper
from .match_operation import MatchOperation


class WillNotToMove37Pawn(MatchOperation):
    """［３七の歩を突かない］意志
    """


    @staticmethod
    def will_on_move(move, table):
        """指し手は［３七の歩を突かない］意志を残しているか？
        """
        ban = Ban(table)

        src_sq_obj = Square(cshogi.move_from(move))
        # print(f'★ {src_sq_obj.sq=} ', end='')
        # print(f'{Helper.sq_to_masu(src_sq_obj.sq)=} ', end='')
        # print(f'{table.piece_type(src_sq_obj.sq)=}')


        # ３七以外にある駒は関係ない
        #print(f'D: {Helper.turn_name(table.turn)=} {Helper.sq_to_masu(ban.masu(37))=} {Helper.sq_to_masu(src_sq_obj.sq)=}')
        if src_sq_obj.sq != ban.masu(37):
            #print('★ ３七以外にある駒は関係ない')
            return Mind.NOT_IN_THIS_CASE

        # 歩でなければ関係ない
        #print(f'D: {table.piece_type(src_sq_obj.sq)=} {cshogi.PAWN=}')
        if table.piece_type(src_sq_obj.sq) != cshogi.PAWN:
            #print('★ 歩でなければ関係ない')
            return Mind.NOT_IN_THIS_CASE

        # 歩が動くんだったらダメ
        return Mind.WILL_NOT


    def __init__(self):
        super().__init__()
        self._name = '３七の歩を突かない'


    def do_anything(self, will_play_moves, table, config_doc):
        if config_doc['march']['will_not_to_move_37_pawn']:
            for i in range(len(will_play_moves))[::-1]:     # `[::-1]` - 逆順
                m = will_play_moves[i]
                mind = WillNotToMove37Pawn.will_on_move(m, table)
                if mind == Mind.WILL_NOT:
                    del will_play_moves[i]

        return will_play_moves
