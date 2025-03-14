import cshogi
import datetime
import random
import sys

from ..march_operations import DoNotBack, DoNotUpToRank6, DoNotMoveUntilRookMoves, DoNotBuildRightWall, DoNotMoveLeftLance, DoNotMoveRightLance, DoNotMoveRook, DoNotGoLeft, WillForThreeGoldAndSilverCoinsToGatherToTheRight, WillNotToBeCut88Bishop, WillNotToMove37Pawn, WillSwingingRook, WillToTakeThePieceWithoutLosingAnything


class Go():


    def __init__(self):
        # 初期状態では、有効でない行進演算です。
        self._march_operation_list_when_idling = [
            DoNotMoveRook(),        # 行進［きりんは動くな］  NOTE 飛車を振るまで有効になりません
        ]

        self._march_operation_list = [
            DoNotBack(),            # 行進［戻るな］
            DoNotBuildRightWall(),  # 行進［右壁を作るな］
            DoNotMoveLeftLance(),   # 行進［左のイノシシは動くな］
            DoNotMoveRightLance(),  # 行進［右のイノシシは動くな］
            DoNotGoLeft(),          # 行進［左へ行くな］
            DoNotUpToRank6(),       # 行進［６段目に上がるな］
            DoNotMoveUntilRookMoves(),   # 行進［キリンが動くまで動くな］
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
            print(f'★ get_will_play_moves: 行進演算 削除 {march_operation.name=}')

        return will_play_moves


    def on_best_move_played_when_idling(self, move, table, config_doc):
        """（アイドリング中の行進演算について）指す手の確定時。
        """

        match_operation_list_to_activate = []
        match_operation_list_to_remove = []

        # 行進リスト
        for march_operation in self._march_operation_list_when_idling:
            march_operation.on_best_move_played_when_idling(
                    move        = move,
                    table       = table,
                    config_doc  = config_doc)

            if march_operation.is_activate:
                match_operation_list_to_activate.append(march_operation)

            # 行進演算を、必要がなくなったら、リストから除外する操作
            if march_operation.is_removed:
                match_operation_list_to_remove.append(march_operation)

        for march_operation in match_operation_list_to_activate:
            self._march_operation_list_when_idling.remove(march_operation)
            self._march_operation_list.append(march_operation)
            print(f'★ ｏn_best_move_played: 行進演算 有効化 {march_operation.name=}')

        for march_operation in match_operation_list_to_remove:
            self._march_operation_list.remove(march_operation)
            print(f'★ ｏn_best_move_played: 行進演算 削除 {march_operation.name=}')


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
            print(f'★ ｏn_best_move_played: 行進演算 削除 {march_operation.name=}')
