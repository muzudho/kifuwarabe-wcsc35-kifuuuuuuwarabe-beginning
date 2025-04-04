import cshogi

from .piece_and_piece_type_model import PieceModel


class TurnModel:


    _codes = [
        'black',
        'white'
    ]


    @classmethod
    def code(clazz, color):
        return clazz._codes[color]


    @staticmethod
    def reverse(color):
        if color == cshogi.BLACK:
            return cshogi.WHITE
        return cshogi.BLACK


    @staticmethod
    def is_opponent_pc(piece, table):
        """相手の駒か？
        """
        if piece == cshogi.NONE:
            return False
        return table.turn != PieceModel.turn(piece=piece)
