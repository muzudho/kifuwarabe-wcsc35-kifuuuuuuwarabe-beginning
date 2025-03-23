import cshogi

from datetime import datetime

from ..logics_o3x_negative_rules import \
    DoNotBack, DoNotBreakFamousFence, DoNotBuildRightWall, \
    DoNotDogAndCatSideBySide, \
    DoNotGoLeft, \
    DoNotUpToRank6, \
    DoNotMoveUntilRookMoves, DoNotMoveLeftLance, DoNotMoveRightLance, DoNotMoveRook, \
    WillForThreeGoldAndSilverCoinsToGatherToTheRight, WillNotToMove37Pawn, WillSwingingRook
from ..models_o1x import Table
from ..models_o1x.table_access_object import PieceValueTAO
from ..modules import ThinkingLoggerModule


class Gymnasium():
    """体育館。きふわらべはなぜか体育館で将棋をしている。
    """


    def __init__(self, config_doc):
        """初期化します。
        """

        # 設定
        self._config_doc = config_doc

        # 思考のログ・ファイル
        now = datetime.now()
        self._thinking_logger_module = ThinkingLoggerModule(
                file_name=f"logs/thinking_[{now.strftime('%Y%m%d_%H%M%S')}].log")

        # 盤
        self._table = Table.create_table()

        # この将棋エンジンの手番
        self._engine_turn = None

        # 盤へアクセスする関連のオブジェクト
        self._piece_value_tao = PieceValueTAO(table = self._table)

        # ９段目に近い方の対局者から見た駒得評価値。
        self._np_value = 0

        # 初期状態では、有効でない行進演算です。
        self._list_of_idle_negative_rules = [
            DoNotMoveRook(config_doc=config_doc),        # 行進［キリンは動くな］  NOTE 飛車を振るまで有効になりません
        ]

        self._list_of_negative_rules = [
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
        ]


    @property
    def config_doc(self):
        """［設定］
        """
        return self._config_doc


    @property
    def table(self):
        """［盤］
        """
        return self._table


    @property
    def thinking_logger_module(self):
        """思考についてのロガー。
        """
        return self._thinking_logger_module


    @property
    def engine_turn(self):
        """この将棋エンジンの手番。
        """
        return self._engine_turn


    @property
    def np_value(self):
        """９段目に近い方の対局者から見た駒得評価値。
        """
        return self._np_value


    # @property
    # def engine_value(self):
    #     """この将棋エンジンの評価値。
    #     """
    #     if self._engine_turn == cshogi.BLACK:
    #         return self.np_value
    #     return -self.np_value


    @engine_turn.setter
    def engine_turn(self, value):
        self._engine_turn = value


    @property
    def piece_value_tao(self):
        return self._piece_value_tao


    @property
    def list_of_idle_negative_rules(self):
        """初期状態では、有効でない行進演算です。
        """
        return self._list_of_idle_negative_rules


    @property
    def list_of_negative_rules(self):
        return self._list_of_negative_rules
    

    @np_value.setter
    def np_value(self, value):
        self._np_value = value


    ########################
    # MARK: イベントハンドラ
    ########################

    def on_new_game(self):
        """［新規対局開始］
        """
        self._thinking_logger_module.delete_file()  # ログファイル　＞　削除。
        self._np_value = 0  # ９段目に近い方の対局者から見た駒得評価値。


    ##################
    # MARK: 指し手関連
    ##################

    def do_move_o1x(self, move):
        """一手指す。
        """

        exchange_value = self.piece_value_tao.before_move(
                move = move)

        if self.engine_turn == cshogi.WHITE:
            exchange_value *= -1

        self.np_value += exchange_value

        return self._table.do_move_o1o1x(move = move)


    def undo_move_o1x(self):
        """一手戻す。
        """

        move = self._table.undo_move_o1o1x()

        exchange_value = self.piece_value_tao.before_undo_move(
                move = move)

        if self.engine_turn == cshogi.WHITE:
            exchange_value *= -1

        self.np_value -= exchange_value

        return move


    def dump(self):
        return f"""\
{self._table.dump()}
{self._np_value=}
{len(self._list_of_idle_negative_rules)=}
{len(self._list_of_negative_rules)=}
"""
