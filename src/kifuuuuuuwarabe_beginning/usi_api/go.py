import cshogi
import datetime
import random
import sys

from .. import Mind
from ..definitions_of_will import WillForThreeGoldAndSilverCoinsToGatherToTheRight, WillNotToBeCut88Bishop, WillNotToBuildRightWall, WillNotToMove37Pawn, WillSwingingRook, WillToClearWayOfRook, WillToTakeThePieceWithoutLosingAnything


class Go():


    @staticmethod
    def get_will_play_moves(config_doc, table, will_play_moves):
        will_play_moves = Go.get_will_for_three_gold_and_silver_coins_to_gather_to_the_right(
                config_doc=config_doc,
                table=table,
                will_play_moves=will_play_moves)

        will_play_moves = Go.get_will_not_to_move_37_pawn(
                config_doc=config_doc,
                table=table,
                will_play_moves=will_play_moves)

        will_play_moves = Go.get_will_not_to_build_right_wall(
                config_doc=config_doc,
                table=table,
                will_play_moves=will_play_moves)

        will_play_moves = Go.get_will_swinging_rook(
                config_doc=config_doc,
                table=table,
                will_play_moves=will_play_moves)

        will_play_moves = Go.get_will_not_to_be_cut_88_bishop(
                config_doc=config_doc,
                table=table,
                will_play_moves=will_play_moves)

        will_play_moves = Go.get_will_to_take_the_piece_without_losing_anything(
                config_doc=config_doc,
                table=table,
                will_play_moves=will_play_moves)

        return will_play_moves


    @staticmethod
    def get_will_for_three_gold_and_silver_coins_to_gather_to_the_right(config_doc, table, will_play_moves):
        """［金銀３枚が右に集まる意志］
        """

        if config_doc['will']['will_for_three_gold_and_silver_coins_to_gather_to_the_right']:
            for i in range(len(will_play_moves))[::-1]:
                m = will_play_moves[i]
                mind = WillForThreeGoldAndSilverCoinsToGatherToTheRight.will_before_move(m, table)
                if mind == Mind.WILL_NOT:
                    del will_play_moves[i]

        return will_play_moves


    @staticmethod
    def get_will_not_to_move_37_pawn(config_doc, table, will_play_moves):
        """［３七の歩を突かない意志］
        """
        # ［３七の歩を突かない意志］
        if config_doc['will']['will_not_to_move_37_pawn']:
            for i in range(len(will_play_moves))[::-1]:
                m = will_play_moves[i]
                mind = WillNotToMove37Pawn.will_on_move(m, table)
                if mind == Mind.WILL_NOT:
                    del will_play_moves[i]

        return will_play_moves


    @staticmethod
    def get_will_not_to_build_right_wall(config_doc, table, will_play_moves):
        """［右壁を作らない意志］
        """
        # ［右壁を作らない意志］
        if config_doc['will']['will_not_to_build_right_wall']:
            for i in range(len(will_play_moves))[::-1]:
                m = will_play_moves[i]
                mind = WillNotToBuildRightWall.will_play_before_move(m, table)
                if mind == Mind.WILL_NOT:
                    del will_play_moves[i]

        return will_play_moves


    @staticmethod
    def get_will_swinging_rook(config_doc, table, will_play_moves):
        """［振り飛車をする意志］
        """

        # ［振り飛車をする意志］
        if config_doc['will']['will_swinging_rook']:
            if Mind.WILL == WillSwingingRook.will_on_board(table):
                #print('★ go: 盤は［振り飛車する意志］を残しています', file=sys.stderr)

                for i in range(len(will_play_moves))[::-1]:
                    m = will_play_moves[i]

                    # ［飛車道を開ける意志］
                    if config_doc['will']['will_to_clear_way_of_rook']:
                        mind = WillToClearWayOfRook.will_before_move(m, table)
                        if mind == Mind.WILL_NOT:
                            del will_play_moves[i]

                    # ［振り飛車をする意志］
                    mind = WillSwingingRook.will_on_move(m, table)
                    if mind == Mind.WILL_NOT:
                        del will_play_moves[i]
            
            # else:
            #     print('★ go: 盤は［振り飛車する意志］はありません', file=sys.stderr)
            #     pass

        return will_play_moves


    @staticmethod
    def get_will_not_to_be_cut_88_bishop(config_doc, table, will_play_moves):
        """［８八の角を素抜かれない意志］
        """

        # １手指してから判定
        for i in range(len(will_play_moves))[::-1]:
            m = will_play_moves[i]
            table.push(m)   # １手指す

            # ［８八の角を素抜かれない意志］
            if config_doc['will']['will_not_to_be_cut_88_bishop']:
                mind = WillNotToBeCut88Bishop.have_will_after_moving_on_board(table)
                if mind == Mind.WILL_NOT:
                    del will_play_moves[i]

            table.pop() # １手戻す

        return will_play_moves


    @staticmethod
    def get_will_to_take_the_piece_without_losing_anything(config_doc, table, will_play_moves):
        """［駒取って損しない意志］
        """

        # １手指してから判定
        for i in range(len(will_play_moves))[::-1]:
            m = will_play_moves[i]

            # ［８八の角を素抜かれない意志］
            if config_doc['will']['will_to_take_the_piece_without_losing_anything']:
                mind = WillToTakeThePieceWithoutLosingAnything.will_move(m, table)
                if mind == Mind.WILL_NOT:
                    del will_play_moves[i]

        return will_play_moves
