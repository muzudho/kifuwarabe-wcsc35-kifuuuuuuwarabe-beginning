from ..march_operations import \
    DoNotBack, DoNotBreakFamousFence, DoNotBuildRightWall, \
    DoNotDogAndCatSideBySide, \
    DoNotGoLeft, \
    DoNotUpToRank6, \
    DoNotMoveUntilRookMoves, DoNotMoveLeftLance, DoNotMoveRightLance, DoNotMoveRook, \
    WillForThreeGoldAndSilverCoinsToGatherToTheRight, WillNotToMove37Pawn, WillSwingingRook
# 削除 WillNotToBeCut88Bishop, WillToTakeThePieceWithoutLosingAnything

from ..models import Table
from ..models.table_access_object import PieceValueTAO


class Gymnasium():
    """体育館。きふわらべはなぜか体育館で将棋をしている。
    """


    def __init__(self, config_doc):
        """初期化します。
        """

        # 盤
        self._table = Table.create_table()

        # 盤へアクセスする関連のオブジェクト
        self._piece_value_tao = PieceValueTAO(table = self._table)

        # ９段目に近い方の対局者から見た駒得評価値。
        self._nine_rank_side_value = 0

        # 初期状態では、有効でない行進演算です。
        self._march_operation_list_when_idling = [
            DoNotMoveRook(config_doc=config_doc),        # 行進［キリンは動くな］  NOTE 飛車を振るまで有効になりません
        ]


    @property
    def table(self):
        """［盤］。
        """
        return self._table


    @property
    def piece_value_tao(self):
        return self._piece_value_tao


    @property
    def nine_rank_side_value(self):
        """９段目に近い方の対局者から見た駒得評価値。
        """
        return self._nine_rank_side_value


    @property
    def march_operation_list_when_idling(self):
        """初期状態では、有効でない行進演算です。
        """
        return self._march_operation_list_when_idling


    @nine_rank_side_value.setter
    def nine_rank_side_value(self, value):
        self._nine_rank_side_value = value


    def on_new_game(self):
        self._nine_rank_side_value = 0  # ９段目に近い方の対局者から見た駒得評価値。
