import cshogi
import sys

from ..models import constants, Square
from ..sente_perspective import Ban, Comparison, Helper, Ji
from .match_operation import MatchOperation


class WillSwingingRook(MatchOperation):
    """［振り飛車をする］意志
    """


    @staticmethod
    def will_on_board(table):
        """盤は［振り飛車をする］意志を残しているか？

        ４０手目までは振り飛車の意志を残しているとします。
        ４１手目以降は振り飛車の意志はありません
        """
        #print(f'★ is_there_will_on_board: {table.move_number=}', file=sys.stderr)
        if table.move_number < 41:
            return constants.mind.WILL
        
        return constants.mind.WILL_NOT


    def __init__(self):
        super().__init__()
        self._label = '振り飛車をする'


    @staticmethod
    def will_on_move(move, table):
        """指し手は［振り飛車をする］意志を残しているか？
        """
        ban = Ban(table)
        cmp = Comparison(table)
        ji = Ji(table)

        src_sq_obj = Square(cshogi.move_from(move))
        dst_sq_obj = Square(cshogi.move_to(move))


        # 玉
        if cshogi.move_from_piece_type(move) == cshogi.KING:
            # 飛車が２八にいるか？
            if table.piece(ban.masu(28)) == ji.pc(cshogi.ROOK):
                # この駒は動いてはいけない
                return constants.mind.WILL_NOT

            #print(f'★ will_on_move: 玉', file=sys.stderr)            
            # 元位置位右に移動するなら、意志あり
            e1 = cmp.swap(dst_sq_obj.file, src_sq_obj.file)
            if e1[0] <= e1[1]:
                return constants.mind.WILL
            
            return constants.mind.WILL_NOT


        # 飛
        if cshogi.move_from_piece_type(move) == cshogi.ROOK:
            k_sq_obj = Square(table.king_square(table.turn))
            # 飛車は４筋より左に振る。かつ、玉と同じ筋または玉より左の筋に振る
            e1 = cmp.swap(dst_sq_obj.file, ban.suji(4))
            e2 = cmp.swap(dst_sq_obj.file, k_sq_obj.file)

            if e1[0] > e1[1] and e2[0] >= e2[1]:
                return constants.mind.WILL
            
            return constants.mind.WILL_NOT


        return constants.mind.NOT_IN_THIS_CASE


    def do_anything(self, will_play_moves, table, config_doc):
        # ［振り飛車をする］意志
        if config_doc['march_operations']['will_swinging_rook']:
            if constants.mind.WILL == WillSwingingRook.will_on_board(table):
                #print('★ go: 盤は［振り飛車をする］意志を残しています', file=sys.stderr)

                for i in range(len(will_play_moves))[::-1]:     # `[::-1]` - 逆順
                    m = will_play_moves[i]

                    # ［振り飛車をする］意志
                    mind = WillSwingingRook.will_on_move(m, table)
                    if mind == constants.mind.WILL_NOT:
                        del will_play_moves[i]
            
            # else:
            #     print('★ go: 盤は［振り飛車をする］意志はありません', file=sys.stderr)
            #     pass

        return will_play_moves
