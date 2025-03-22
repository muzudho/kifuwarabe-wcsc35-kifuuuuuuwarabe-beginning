import cshogi


class PieceType():
    """駒種類
    """


    _kanji_list = [
        '',     # [ 0]
        '歩',   # [ 1]
        '香',   # [ 2]
        '桂',   # [ 3]
        '銀',   # [ 4]
        '角',   # [ 5]
        '飛',   # [ 6]
        '金',   # [ 7]
        '玉',   # [ 8]
        'と',   # [ 9]
        '杏',   # [10]
        '圭',   # [11]
        '全',   # [12]
        '馬',   # [13]
        '竜',   # [14]
    ]

    _alphabet_list = [
        ''  ,   # [ 0]
        'P' ,   # [ 1] 歩
        'L' ,   # [ 2] 香
        'N' ,   # [ 3] 桂
        'S' ,   # [ 4] 銀
        'B' ,   # [ 5] 角
        'R' ,   # [ 6] 飛
        'G' ,   # [ 7] 金
        'K' ,   # [ 8] 玉
        '+P',   # [ 9] と
        '+L',   # [10] 杏
        '+N',   # [11] 圭
        '+S',   # [12] 全
        '+B',   # [13] 馬
        '+R',   # [14] 竜
    ]


    @classmethod
    def kanji(clazz, piece_type):
        return clazz._kanji_list[piece_type]


    @classmethod
    def alphabet(clazz, piece_type):
        return clazz._alphabet_list[piece_type]


class Piece():
    """駒
    """


    _kanji_list = [
        '',     # 0
        '歩',   # 1
        '香',
        '桂',
        '銀',
        '角',
        '飛',
        '金',
        '玉',
        'と',
        '杏',
        '圭',
        '全',
        '馬',
        '竜',   # 14
        '',
        '',

        'v歩',  # 16 + 1
        'v香',
        'v桂',
        'v銀',
        'v角',
        'v飛',
        'v金',
        'v玉',
        'vと',
        'v杏',
        'v圭',
        'v全',
        'v馬',
        'v竜',  # 16 + 14
    ]


    _on_board_list = [
        '   ',     # 0
        ' 歩',   # 1
        ' 香',
        ' 桂',
        ' 銀',
        ' 角',
        ' 飛',
        ' 金',
        ' 玉',
        ' と',
        ' 杏',
        ' 圭',
        ' 全',
        ' 馬',
        ' 竜',   # 14
        '   ',
        '   ',

        'v歩',  # 16 + 1
        'v香',
        'v桂',
        'v銀',
        'v角',
        'v飛',
        'v金',
        'v玉',
        'vと',
        'v杏',
        'v圭',
        'v全',
        'v馬',
        'v竜',  # 16 + 14
    ]


    @classmethod
    def kanji(clazz, piece):
        return clazz._kanji_list[piece]


    @classmethod
    def on_board(clazz, piece):
        return clazz._on_board_list[piece]


    @staticmethod
    def turn(piece):
        if piece <= 16:
            return cshogi.BLACK
        
        return cshogi.WHITE


class Turn:


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
        return table.turn != Piece.turn(piece=piece)
