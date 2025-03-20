import cshogi


class PieceType():
    """駒種類
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
    ]

    @classmethod
    def kanji(clazz, piece):
        return clazz._kanji_list[piece]


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
