import cshogi

from datetime import datetime

from ..models_o1x import TableModel, TurnModel
from ..models_o1x.table_access_object import PieceValueTAO
from ..modules import ThinkingLoggerModule
from .health_check_model import HealthCheckModel
from .negative_rule_collection_model import NegativeRuleCollectionModel


class GymnasiumModel():
    """体育館。きふわらべはなぜか体育館で将棋をしている。
    """


    def __init__(self, config_doc):
        """初期化します。
        """

        # 設定
        self._config_doc = config_doc

        # 思考のログ・ファイル
        self._thinking_logger_module = None

        # 盤
        self._table = TableModel.create_table()

        # この将棋エンジンの手番
        self._engine_turn = None

        # 盤へアクセスする関連のオブジェクト
        self._piece_value_tao = PieceValueTAO(table = self._table)

        # ９段目に近い方の対局者から見た駒得評価値。
        self._np_value = 0

        self._negative_rule_collection_model = NegativeRuleCollectionModel(config_doc=config_doc)

        self._health_check = None   # 健康診断


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


    @engine_turn.setter
    def engine_turn(self, value):
        self._engine_turn = value


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


    @property
    def piece_value_tao(self):
        return self._piece_value_tao
    

    @np_value.setter
    def np_value(self, value):
        self._np_value = value


    @property
    def negative_rule_collection_model(self):
        return self._negative_rule_collection_model


    @property
    def health_check(self):
        return self._health_check


    ########################
    # MARK: イベントハンドラ
    ########################

    def on_new_game(self):
        """［新規対局開始］
        """
        self._health_check = HealthCheckModel()  # 健康診断
        self._thinking_logger_module = None     # 初期化の準備
        self._np_value = 0  # ９段目に近い方の対局者から見た駒得評価値。


    def on_position(self, command):
        #print(f"★ [gymnasium.py > on_position] start.")
        self.engine_turn = self._table.turn     # この将棋エンジンの手番を記録。

        if self._thinking_logger_module is None:
            #print(f"★ [gymnasium.py > on_position] initialize thinking_logger_module.")
            now = datetime.now()
            self._thinking_logger_module = ThinkingLoggerModule(
                    file_name   = f"logs/thinking_[{now.strftime('%Y%m%d_%H%M%S')}]_{TurnModel.code(self.engine_turn)}.log",
                    engine_turn = self.engine_turn)
            
            self._thinking_logger_module.delete_file()  # ログファイル　＞　削除。

        self._thinking_logger_module.append(command)
        #print(f"★ [gymnasium.py > on_position] end.")


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
{len(self._negative_rule_collection_model.list_of_idle)=}
{len(self._negative_rule_collection_model.list_of_active)=}
"""
