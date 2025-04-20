import cshogi

from .piece_moved_model import PieceMovedModel


class TableModel:
    """cshogi の Board に付いていない機能を付加するラッパー
    """


    @staticmethod
    def create_table():
        return TableModel(
                # 平手指定局面を明示
                designated_sfen='lnsgkgsnl/1r5b1/ppppppppp/9/9/9/PPPPPPPPP/1B5R1/LNSGKGSNL b - 1',
                piece_moved_list=[])


    def __init__(self, designated_sfen, piece_moved_list):
        self._designated_sfen = designated_sfen
        self._board = cshogi.Board(self._designated_sfen)

        # 局面の重複を調べるために、０手の SFEN をリストで持ちたい
        self._piece_moved_list = piece_moved_list


    @property
    def designated_sfen(self):
        """指定局面"""
        return self._designated_sfen


    ##################
    # MARK: 指し手関連
    ##################

    @property
    def legal_moves(self):
        return self._board.legal_moves


    ################
    # MARK: 指す関連
    ################

    def do_move_o1o1x(self, move):
        """一手指す。
        """

        result = self._board.push(move)

        # 指した後に記録
        self._piece_moved_list.append(PieceMovedModel(
                move=move,
                sfen_with_0_moves=self._board.sfen()))  # 指した後の sfen を記憶
        
        return result


    def undo_move_o1o1x(self):
        """一手戻す。
        """

        # 状態を戻す
        self._piece_moved_list.pop()

        return self._board.pop()


    ################
    # MARK: 局面関連
    ################

    def is_check(self):
        """王手している。
        """
        return self._board.is_check()


    def is_game_over(self):
        """投了図だ。
        """
        return self._board.is_game_over()


    def is_nyugyoku(self):
        """入玉宣言勝ちだ。
        """
        return self._board.is_nyugyoku()


    def mate_move_in_1ply(self):
        """一手詰め局面か。
        """
        return self._board.mate_move_in_1ply()


    ################
    # MARK: 盤面関連
    ################

    def king_square(self, turn):
        return self._board.king_square(turn)


    def piece(self, sq):
        """［先後付きの駒］
        NOTE sq がナン（盤外）にならないようにしてください。
        """
        return self._board.piece(sq)


    def piece_type(self, sq):
        return self._board.piece_type(sq)


    @property
    def pieces_in_hand(self):
        """持ち駒。
        値 = [
            # 先手
            [歩, 香, 桂, 銀, 金, 角, 飛],
            # 後手
            [歩, 香, 桂, 銀, 金, 角, 飛],
        ]
        """
        return self._board.pieces_in_hand


    def reset(self):
        return self._board.reset()


    def set_sfen(self, sfen):
        self._board.set_sfen(sfen)


    def sfen(self):
        """平手初期局面からの棋譜が付いていない。指定局面の１手目の形になっている
        """
        return self._board.sfen()


    @property
    def turn(self):
        """先手か後手か
        """
        return self._board.turn


    @property
    def is_gote(self):
        """後手か
        """
        return self._board.turn == cshogi.WHITE


    ########################
    # MARK: 指し手モデル関連
    ########################

    def move_from_usi(self, usi):
        return self._board.move_from_usi(usi = usi)
    

    @property
    def move_number(self):
        return self._board.move_number


    #########
    # MARK: C
    #########

    def copy_piece_moved_list(self):
        """［指し手のリスト］のコピー。
        """
        return list(self._piece_moved_list)


    def copy_table_with_0_moves(self):
        """テーブルのコピー。ただし、指定局面の１手目に戻っている"""
        return TableModel(
                designated_sfen=self.designated_sfen,
                piece_moved_list=self.copy_piece_moved_list())


    ##############
    # MARK: ダンプ
    ##############

    def dump(self):


        def _dump_piece_moved_list():
            items = []
            for piece_moved in self._piece_moved_list:
                items.append(f"{piece_moved=}")
            
            return ' '.join(items)

        return f"""
{self._designated_sfen=}
{self._board.sfen()=}
{_dump_piece_moved_list()=}
"""
