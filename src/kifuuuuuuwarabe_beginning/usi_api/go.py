import cshogi
import datetime
import random
import sys

from .. import Mind
from ..march_operations import DoNotUpToRank6, DoNotUpToRank8, DoNotBuildRightWall, DoNotGoLeft, WillForThreeGoldAndSilverCoinsToGatherToTheRight, WillNotToBeCut88Bishop, WillNotToMove37Pawn, WillSwingingRook, WillToTakeThePieceWithoutLosingAnything


class Go():


    def __init__(self):
        self._march_operation_list = [
            DoNotBuildRightWall(),   # 行進［右壁を作るな］
            DoNotGoLeft(),      # 行進［左へ行くな］
            DoNotUpToRank6(),   # 行進［６段目に上がるな］
            DoNotUpToRank8(),   # 行進［８段目に上がるな］
            WillForThreeGoldAndSilverCoinsToGatherToTheRight(),     # ［金銀３枚が右に集まる］意志
            WillNotToMove37Pawn(),  # ［３七の歩を突かない］意志
            WillSwingingRook(),     # ［振り飛車をする］意志
            WillNotToBeCut88Bishop(),   # ［８八の角を素抜かれない意志］
            WillToTakeThePieceWithoutLosingAnything(),  #  ［駒取って損しない意志］
        ]


    def get_will_play_moves(self, will_play_moves, table, config_doc):

        # 行進リスト
        for march_operation in self._march_operation_list:
            will_play_moves = march_operation.do_anything(
                    will_play_moves = will_play_moves,
                    table           = table,
                    config_doc      = config_doc)

        return will_play_moves
