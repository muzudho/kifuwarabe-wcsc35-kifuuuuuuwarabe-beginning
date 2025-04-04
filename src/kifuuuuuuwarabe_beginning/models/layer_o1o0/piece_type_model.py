class PieceTypeModel():
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
