import cshogi

from ..models import constants, Square
from ..models_level_2.nine_rank_side_perspective import Ban
from .match_operation import MatchOperation


class WillNotToMove37Pawn(MatchOperation):
    """［３七の歩を突かない］意志
    """


    def __init__(self, config_doc):
        super().__init__(
                id          = 'will_not_to_move_37_pawn',
                label       = '３七の歩を突かない',
                config_doc  = config_doc)


    def before_move(self, move, table):
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
            return constants.mind.NOT_IN_THIS_CASE

        # 歩でなければ関係ない
        #print(f'D: {table.piece_type(src_sq_obj.sq)=} {cshogi.PAWN=}')
        if table.piece_type(src_sq_obj.sq) != cshogi.PAWN:
            #print('★ 歩でなければ関係ない')
            return constants.mind.NOT_IN_THIS_CASE

        # 歩が動くんだったらダメ
        return constants.mind.WILL_NOT
