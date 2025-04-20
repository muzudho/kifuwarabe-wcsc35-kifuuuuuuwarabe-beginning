import cshogi


class PieceModel():
    """先後付きの駒

    TODO PlanetPieceModel に移行したい。
    """


    _kanji_list = [
        '',     # 0
        '歩',   # 1
        '香',   # 2
        '桂',   # 3
        '銀',   # 4
        '角',   # 5
        '飛',   # 6
        '金',   # 7
        '玉',   # 8
        'と',   # 9
        '杏',   # 10
        '圭',   # 11
        '全',   # 12
        '馬',   # 13
        '竜',   # 14
        '',     # 15

        '',     # 16    ※ 16 + 0
        'v歩',  # 17    ※ 16 + 1
        'v香',  # 18
        'v桂',  # 19
        'v銀',  # 20
        'v角',  # 21
        'v飛',  # 22
        'v金',  # 23
        'v玉',  # 24
        'vと',  # 25
        'v杏',  # 26
        'v圭',  # 27
        'v全',  # 28
        'v馬',  # 29
        'v竜',  # 16 + 14   #30
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
        # FIXME cshogi.NONE をエラーとしたい。
        if piece <= 16:
            return cshogi.BLACK
        
        return cshogi.WHITE
