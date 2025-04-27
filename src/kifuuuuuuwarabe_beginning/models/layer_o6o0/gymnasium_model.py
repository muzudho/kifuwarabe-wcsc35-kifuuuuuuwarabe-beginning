import cshogi

from datetime import datetime

from ...modules import ThinkingLoggerModule
from ..layer_o1o0 import PtolemaicTheoryModel, TableModel, TurnModel
from ..layer_o1o0.table_access_object import PieceValueTAO
from ..layer_o2o0 import BasketballCourtModel
from ..layer_o7o0_health import HealthCheckGoModel, HealthCheckQsModel
from .gourei_collection_model import GoureiCollectionModel


class GymnasiumModel():
    """体育館。きふわらべはなぜか体育館で将棋をしている。
    """


    def __init__(self, config_doc):
        """初期化します。
        """
        
        self._config_doc = config_doc           # 設定
        self._thinking_logger_module = None     # 思考のログ・ファイル
        self._table = TableModel.create_table() # 盤
        self._exshell = None                    # エクシェル
        self._earth_turn = None                 # この将棋エンジンの手番
        self._piece_value_tao = PieceValueTAO(table = self._table)  # 盤へアクセスする関連のオブジェクト
        self._np_value = 0                      # ９段目に近い方の対局者から見た駒得評価値。
        self._basketball_court_model = None     # バスケットボール・コート
        self._gourei_collection_model = None    # 号令
        self._health_check_go_model = None      # 健康診断
        self._health_check_qs_model = None      # 健康診断
        self._ptolemaic_theory_model  = PtolemaicTheoryModel(gymnasium=self)    # ［天動説］


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
    def exshell(self):
        """［エクシェル］
        """
        return self._exshell


    @exshell.setter
    def exshell(self, value):
        """［エクシェル］
        """
        self._exshell = value


    @property
    def thinking_logger_module(self):
        """思考についてのロガー。
        """
        return self._thinking_logger_module


    @property
    def earth_turn(self):
        """この将棋エンジンの手番。
        """
        return self._earth_turn


    @earth_turn.setter
    def earth_turn(self, value):
        self._earth_turn = value


    @property
    def is_mars(self):
        """火星か。
        """
        return self._earth_turn != self._table.turn


    @property
    def np_value(self):
        """９段目に近い方の対局者から見た駒得評価値。
        """
        return self._np_value


    # @property
    # def engine_value(self):
    #     """この将棋エンジンの評価値。
    #     """
    #     if self._earth_turn == cshogi.BLACK:
    #         return self.np_value
    #     return -self.np_value


    @property
    def piece_value_tao(self):
        return self._piece_value_tao
    

    @np_value.setter
    def np_value(self, value):
        self._np_value = value


    @property
    def basketball_court_model(self):
        return self._basketball_court_model


    @property
    def gourei_collection_model(self):
        return self._gourei_collection_model


    @property
    def health_check_go_model(self):
        return self._health_check_go_model


    @property
    def health_check_qs_model(self):
        return self._health_check_qs_model


    @property
    def ptolemaic_theory_model(self):
        return self._ptolemaic_theory_model


    ########################
    # MARK: イベントハンドラ
    ########################

    def on_new_game(self):
        """［新規対局開始］
        """
        self._thinking_logger_module = None     # 初期化の準備
        self._np_value = 0  # ９段目に近い方の対局者から見た駒得評価値。

        self._basketball_court_model = BasketballCourtModel(
                config_doc = self._config_doc)
        self._gourei_collection_model = GoureiCollectionModel(
                basketball_court_model  = self._basketball_court_model)


    def on_position(self, command):
        #print(f"★ [gymnasium.py > on_position] start.")
        self.earth_turn = self._table.turn          # この将棋エンジンの手番を記録。
        self._health_check_go_model  = HealthCheckGoModel(     # 健康診断をクリアー。
                gymnasium   = self)
        self._health_check_qs_model  = HealthCheckQsModel(     # 健康診断をクリアー。
                gymnasium   = self)

        if self._thinking_logger_module is None:
            #print(f"★ [gymnasium.py > on_position] initialize thinking_logger_module.")
            now = datetime.now()
            self._thinking_logger_module = ThinkingLoggerModule(
                    file_name   = f"logs/thinking_[{now.strftime('%Y%m%d_%H%M%S')}]_{TurnModel.code(self.earth_turn)}.log",
                    earth_turn = self.earth_turn)
            
            self._thinking_logger_module.delete_file()  # ログファイル　＞　削除。

        self._thinking_logger_module.append_message(command)
        #print(f"★ [gymnasium.py > on_position] end.")


    ##################
    # MARK: 指し手関連
    ##################

    def do_move_o1x(self, move):
        """一手指す。
        """

        exchange_value = self.piece_value_tao.before_move_pvt(
                move = move)

        if self.earth_turn == cshogi.WHITE:
            exchange_value *= -1

        self.np_value += exchange_value

        return self._table.do_move_o1o1x(move = move)


    def undo_move_o1x(self):
        """一手戻す。
        """

        move = self._table.undo_move_o1o1x()

        exchange_value = self.piece_value_tao.before_undo_move(
                move = move)

        if self.earth_turn == cshogi.WHITE:
            exchange_value *= -1

        self.np_value -= exchange_value

        return move


    def dump(self):
        return f"""\
{self._table.dump()}
{self._np_value=}
{len(self._gourei_collection_model.positive_rule_list_of_active)=}
{len(self._gourei_collection_model.negative_rule_list_of_idle)=}
{len(self._gourei_collection_model.negative_rule_list_of_active)=}
"""
