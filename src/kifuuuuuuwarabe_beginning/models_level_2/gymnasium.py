import cshogi

from ..march_operations import \
    DoNotBack, DoNotBreakFamousFence, DoNotBuildRightWall, \
    DoNotDogAndCatSideBySide, \
    DoNotGoLeft, \
    DoNotUpToRank6, \
    DoNotMoveUntilRookMoves, DoNotMoveLeftLance, DoNotMoveRightLance, DoNotMoveRook, \
    WillForThreeGoldAndSilverCoinsToGatherToTheRight, WillNotToMove37Pawn, WillSwingingRook
from ..models import Table
from ..models.table_access_object import PieceValueTAO


class Gymnasium():
    """体育館。きふわらべはなぜか体育館で将棋をしている。
    """


    def __init__(self, config_doc):
        """初期化します。
        """

        # 設定
        self._config_doc = config_doc

        # 盤
        self._table = Table.create_table()

        # この将棋エンジンの手番
        self._engine_turn = None

        # 盤へアクセスする関連のオブジェクト
        self._piece_value_tao = PieceValueTAO(table = self._table)

        # ９段目に近い方の対局者から見た駒得評価値。
        self._nine_rank_side_value = 0

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
    def engine_turn(self):
        """この将棋エンジンの手番。
        """
        return self._engine_turn


    @property
    def engine_value(self):
        """この将棋エンジンの評価値。
        """
        if self._engine_turn == cshogi.BLACK:
            return self.nine_rank_side_value
        return -self.nine_rank_side_value



    @engine_turn.setter
    def engine_turn(self, value):
        self._engine_turn = value


    @property
    def piece_value_tao(self):
        return self._piece_value_tao


    @property
    def nine_rank_side_value(self):
        """９段目に近い方の対局者から見た駒得評価値。
        """
        return self._nine_rank_side_value


    @property
    def list_of_idle_negative_rules(self):
        """初期状態では、有効でない行進演算です。
        """
        return self._list_of_idle_negative_rules


    @property
    def list_of_negative_rules(self):
        return self._list_of_negative_rules
    

    @nine_rank_side_value.setter
    def nine_rank_side_value(self, value):
        self._nine_rank_side_value = value


    def on_new_game(self):
        self._nine_rank_side_value = 0  # ９段目に近い方の対局者から見た駒得評価値。


    def do_move_o1x(self, move):
        """一手指す。
        """
        return self._table.do_move_o1o1x(move = move)


    def undo_move_o1x(self):
        """一手戻す。
        """
        return self._table.undo_move_o1o1x()


    def dump(self):
        return f"""\
{self._table.dump()}
{self._nine_rank_side_value=}
{len(self._list_of_idle_negative_rules)=}
{len(self._list_of_negative_rules)=}
"""
