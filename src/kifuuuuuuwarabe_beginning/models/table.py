import cshogi

from .piece_moved import PieceMoved


class Table():
    """cshogi の Board に付いていない機能を付加するラッパー
    """


    @staticmethod
    def create_table():
        return Table(
                # 平手指定局面を明示
                designated_sfen='lnsgkgsnl/1r5b1/ppppppppp/9/9/9/PPPPPPPPP/1B5R1/LNSGKGSNL b - 1',
                move_list_as_usi=[])


    def __init__(self, designated_sfen, move_list_as_usi):
        self._designated_sfen = designated_sfen
        self._board = cshogi.Board(self._designated_sfen)

        # 指し手のリスト
        self._move_list_as_usi = move_list_as_usi

        # 局面の重複を調べるために、０手の SFEN をリストで持ちたい
        self._piece_moved_list = []


    @property
    def designated_sfen(self):
        """指定局面"""
        return self._designated_sfen


    # #########
    # # MARK: C
    # #########

    def copy_piece_moved_list(self):
        return list(self._piece_moved_list)


    def copy_move_list_as_usi(self):
        return list(self._move_list_as_usi)


    def copy_table_with_0_moves(self):
        """テーブルのコピー。ただし、指定局面の１手目に戻っている"""
        return Table(
                designated_sfen=self.designated_sfen,
                move_list_as_usi=self.copy_move_list_as_usi())


    #########
    # MARK: I
    #########

    def is_check(self):
        return self._board.is_check()


    def is_game_over(self):
        return self._board.is_game_over()


    def is_nyugyoku(self):
        return self._board.is_nyugyoku()


    #########
    # MARK: I
    #########

    def king_square(self, turn):
        return self._board.king_square(turn)


    #########
    # MARK: L
    #########

    @property
    def legal_moves(self):
        return self._board.legal_moves


    #########
    # MARK: M
    #########

    def mate_move_in_1ply(self):
        return self._board.mate_move_in_1ply()


    @property
    def move_number(self):
        return self._board.move_number


    #########
    # MARK: P
    #########

    def piece(self, sq):
        return self._board.piece(sq)


    def piece_type(self, sq):
        return self._board.piece_type(sq)


    @property
    def pieces_in_hand(self):
        return self._board.pieces_in_hand


    def pop(self):
        self._move_list_as_usi.pop()
        self._piece_moved_list.pop()

        return self._board.pop()


    def push(self, move):
        self._move_list_as_usi.append(cshogi.move_to_usi(move))
        self._piece_moved_list.append(PieceMoved(
                move_as_usi=cshogi.move_to_usi(move),
                sfen_with_0_moves=None))

        return self._board.push(move)


    def push_usi(self, usi):
        self._move_list_as_usi.append(usi)
        self._piece_moved_list.append(PieceMoved(
                move_as_usi=usi,
                sfen_with_0_moves=None))

        return self._board.push_usi(usi)


    #########
    # MARK: R
    #########

    def reset(self):
        return self._board.reset()


    #########
    # MARK: S
    #########

    def set_sfen(self, sfen):
        self._board.set_sfen(sfen)


    def sfen(self):
        """平手初期局面からの棋譜が付いていない。指定局面の１手目の形になっている
        """
        return self._board.sfen()


    #########
    # MARK: T
    #########

    @property
    def turn(self):
        return self._board.turn
