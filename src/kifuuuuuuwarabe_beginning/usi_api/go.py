import cshogi
import datetime
import random
import sys

from .. import Mind
from ..definitions_of_will import WillNotToBeCut88Bishop, WillNotToBuildRightWall, WillNotToMove37Pawn, WillSwingingRook, WillToClearWayOfRook


class Go():


    @staticmethod
    def will_play_moves(config_doc, board):
        will_play_moves = list(board.legal_moves)


        # ［３七の歩を突かない意志］
        if config_doc['will']['will_not_to_move_37_pawn']:
            for i in range(len(will_play_moves))[::-1]:
                m = will_play_moves[i]
                mind = WillNotToMove37Pawn.will_on_move(board=board, move=m)
                if mind == Mind.WILL_NOT:
                    del will_play_moves[i]


        # ［右壁を作らない意志］
        if config_doc['will']['will_not_to_build_right_wall']:
            for i in range(len(will_play_moves))[::-1]:
                m = will_play_moves[i]
                mind = WillNotToBuildRightWall.will_on_move(board=board, move=m)
                if mind == Mind.WILL_NOT:
                    del will_play_moves[i]

        #print(f'★ go: ［振り飛車する意志］を残してるか尋ねる前の指し手数={len(will_play_moves)}', file=sys.stderr)


        # ［振り飛車をする意志］
        if config_doc['will']['will_swinging_rook']:
            if Mind.WILL == WillSwingingRook.will_on_board(board=board):
                print('★ go: 盤は［振り飛車する意志］を残しています', file=sys.stderr)

                for i in range(len(will_play_moves))[::-1]:
                    m = will_play_moves[i]

                    # ［飛車道を開ける意志］
                    if config_doc['will']['will_to_clear_way_of_rook']:
                        mind = WillToClearWayOfRook.will_on_move(board=board, move=m)
                        if mind == Mind.WILL_NOT:
                            del will_play_moves[i]

                    # ［振り飛車をする意志］
                    mind = WillSwingingRook.will_on_move(board=board, move=m)
                    if mind == Mind.WILL_NOT:
                        del will_play_moves[i]
            
            else:
                print('★ go: 盤は［振り飛車する意志］はありません', file=sys.stderr)
                pass

        # #print(f'★ go: ［振り飛車する意志］を残してるか尋ねた後の指し手数={len(will_play_moves)}', file=sys.stderr)


        print(f'★ go: ［８八の角を素抜かれない意志］を残してるか尋ねる前の指し手数={len(will_play_moves)}', file=sys.stderr)

        # １手指してから判定
        for i in range(len(will_play_moves))[::-1]:
            m = will_play_moves[i]
            board.push(m)   # １手指す

            # ［８八の角を素抜かれない意志］
            if config_doc['will']['will_not_to_be_cut_88_bishop']:
                mind = WillNotToBeCut88Bishop.have_will_after_moving_on_board(board)
                if mind == Mind.WILL_NOT:
                    del will_play_moves[i]

            board.pop() # １手戻す

        print(f'★ go: ［８八の角を素抜かれない意志］を残してるか尋ねた後の指し手数={len(will_play_moves)}', file=sys.stderr)

        return will_play_moves
