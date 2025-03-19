import cshogi
import datetime
import random
import sys

from ..march_operations import \
    DoNotBack, DoNotBreakFamousFence, DoNotBuildRightWall, \
    DoNotDogAndCatSideBySide, \
    DoNotGoLeft, \
    DoNotUpToRank6, \
    DoNotMoveUntilRookMoves, DoNotMoveLeftLance, DoNotMoveRightLance, DoNotMoveRook, \
    WillForThreeGoldAndSilverCoinsToGatherToTheRight, WillNotToMove37Pawn, WillSwingingRook
# 削除 WillNotToBeCut88Bishop, WillToTakeThePieceWithoutLosingAnything


class Go():


    def __init__(self, config_doc):
        # 初期状態では、有効でない行進演算です。
        self._march_operation_list_when_idling = [
            DoNotMoveRook(config_doc=config_doc),        # 行進［キリンは動くな］  NOTE 飛車を振るまで有効になりません
        ]

        self._march_operation_list = [
            DoNotBack                                           (config_doc=config_doc),    # 行進［戻るな］
            DoNotBreakFamousFence                               (config_doc=config_doc),    # 行進［名の有る囲いを崩すな］
            DoNotBuildRightWall                                 (config_doc=config_doc),    # 行進［右壁を作るな］
            DoNotMoveLeftLance                                  (config_doc=config_doc),    # 行進［左のイノシシは動くな］
            DoNotMoveRightLance                                 (config_doc=config_doc),    # 行進［右のイノシシは動くな］
            DoNotGoLeft                                         (config_doc=config_doc),    # 行進［左へ行くな］
            DoNotDogAndCatSideBySide                            (config_doc=config_doc),    # 行進［イヌとネコを横並びに上げるな］
            DoNotUpToRank6                                      (config_doc=config_doc),    # 行進［６段目に上がるな］
            DoNotMoveUntilRookMoves                             (config_doc=config_doc),    # 行進［キリンが動くまで動くな］
            WillForThreeGoldAndSilverCoinsToGatherToTheRight    (config_doc=config_doc),    # ［金銀３枚が右に集まる］意志
            WillNotToMove37Pawn                                 (config_doc=config_doc),    # ［３七の歩を突かない］意志
            WillSwingingRook                                    (config_doc=config_doc),    # ［振り飛車をする］意志
            # 削除 WillNotToBeCut88Bishop                              (config_doc=config_doc),    # ［８八の角を素抜かれない］意志
            # 削除 WillToTakeThePieceWithoutLosingAnything             (config_doc=config_doc),    # ［駒取って損しない］意志
        ]


    def get_will_play_moves(self, will_play_moves, table, config_doc):

        match_operation_list_to_remove = []

        # 行進リスト
        for march_operation in self._march_operation_list:
            will_play_moves = march_operation.do_anything(
                    will_play_moves = will_play_moves,
                    table           = table)

            # 行進演算を、必要がなくなったら、リストから除外する操作
            if march_operation.is_removed:
                match_operation_list_to_remove.append(march_operation)

        for march_operation in match_operation_list_to_remove:
            self._march_operation_list.remove(march_operation)
            print(f'★ get_will_play_moves: 行進演算 削除 {march_operation.label=}')

        return will_play_moves


    def on_best_move_played_when_idling(self, move, table):
        """（アイドリング中の行進演算について）指す手の確定時。
        """

        match_operation_list_to_activate = []
        match_operation_list_to_remove = []

        # 行進リスト
        for march_operation in self._march_operation_list_when_idling:
            march_operation.on_best_move_played_when_idling(
                    move        = move,
                    table       = table)

            if march_operation.is_activate:
                match_operation_list_to_activate.append(march_operation)

            # 行進演算を、必要がなくなったら、リストから除外する操作
            if march_operation.is_removed:
                match_operation_list_to_remove.append(march_operation)

        for march_operation in match_operation_list_to_activate:
            self._march_operation_list_when_idling.remove(march_operation)
            self._march_operation_list.append(march_operation)
            print(f'★ ｏn_best_move_played: 行進演算 有効化 {march_operation.label=}')

        for march_operation in match_operation_list_to_remove:
            self._march_operation_list.remove(march_operation)
            print(f'★ ｏn_best_move_played: 行進演算 削除 {march_operation.label=}')


    def on_best_move_played(self, move, table):
        """指す手の確定時。
        """

        match_operation_list_to_remove = []

        # 行進リスト
        for march_operation in self._march_operation_list:
            march_operation.on_best_move_played(
                    move        = move,
                    table       = table)

            # 行進演算を、必要がなくなったら、リストから除外する操作
            if march_operation.is_removed:
                match_operation_list_to_remove.append(march_operation)

        for march_operation in match_operation_list_to_remove:
            self._march_operation_list.remove(march_operation)
            print(f'★ ｏn_best_move_played: 行進演算 削除 {march_operation.label=}')
