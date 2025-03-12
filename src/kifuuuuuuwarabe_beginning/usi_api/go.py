import cshogi
import datetime
import random
import sys

from .. import Mind
from ..march_operations import DoNotUpToRank6, DoNotUpToRank8, DoNotBuildRightWall, DoNotGoHorizontalRook, DoNotGoLeft, WillForThreeGoldAndSilverCoinsToGatherToTheRight, WillNotToBeCut88Bishop, WillNotToMove37Pawn, WillSwingingRook, WillToTakeThePieceWithoutLosingAnything


class Go():


    def __init__(self):
        self._march_operation_list = [
            DoNotBuildRightWall(),      # 行進［右壁を作るな］
            DoNotGoHorizontalRook(),    # 行進［きりんは横に行くな］  NOTE 飛車を振るまで有効になりません
            DoNotGoLeft(),      # 行進［左へ行くな］
            DoNotUpToRank6(),   # 行進［６段目に上がるな］
            DoNotUpToRank8(),   # 行進［８段目に上がるな］
            WillForThreeGoldAndSilverCoinsToGatherToTheRight(),     # ［金銀３枚が右に集まる］意志
            WillNotToMove37Pawn(),  # ［３七の歩を突かない］意志
            WillSwingingRook(),     # ［振り飛車をする］意志
            WillNotToBeCut88Bishop(),   # ［８八の角を素抜かれない］意志
            WillToTakeThePieceWithoutLosingAnything(),  #  ［駒取って損しない］意志
        ]


    def get_will_play_moves(self, will_play_moves, table, config_doc):

        match_operation_list_to_remove = []

        # 行進リスト
        for march_operation in self._march_operation_list:
            will_play_moves = march_operation.do_anything(
                    will_play_moves = will_play_moves,
                    table           = table,
                    config_doc      = config_doc)

            # 行進演算を、必要がなくなったら、リストから除外する操作
            if march_operation.is_removed:
                match_operation_list_to_remove.append(march_operation)

        for march_operation in match_operation_list_to_remove:
            self._march_operation_list.remove(march_operation)
            print('★ get_will_play_moves: 行進演算 削除')

        return will_play_moves


    def on_best_move_played(self, move, table, config_doc):
        """指す手の確定時。
        """

        match_operation_list_to_remove = []

        # 行進リスト
        for march_operation in self._march_operation_list:
            march_operation.on_best_move_played(
                    move        = move,
                    table       = table,
                    config_doc  = config_doc)

            # 行進演算を、必要がなくなったら、リストから除外する操作
            if march_operation.is_removed:
                match_operation_list_to_remove.append(march_operation)

        for march_operation in match_operation_list_to_remove:
            self._march_operation_list.remove(march_operation)
            print('★ on_best_move_played: 行進演算 削除')
