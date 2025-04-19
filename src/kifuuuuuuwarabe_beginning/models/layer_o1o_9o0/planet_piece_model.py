class PlanetPieceModel():
    """地球側と、火星側で分けた駒表記。

    TODO あまり使わない？
    """

    _kanji_list = [
        # 地球側
        '',     # [ 0] 
        'ひ',   # [ 1]  歩
        '猪',   # [ 2]  香
        '兎',   # [ 3]  桂
        '猫',   # [ 4]  銀
        '象',   # [ 5]  角
        '麒',   # [ 6]  飛
        '犬',   # [ 7]  金
        '獅',   # [ 8]  玉
        '鶏',   # [ 9]  と
        'イ',   # [10]  杏
        'ウ',   # [11]  圭
        'ネ',   # [12]  全
        'ゾ',   # [13]  馬
        'キ',   # [14]  竜
        '',     # [15]

        # 火星側
        '',     # [16]          16 + 0
        '歩',   # [17]  歩      16 + 1
        '香',   # [18]  香
        '桂',   # [19]  桂
        '銀',   # [20]  銀
        '角',   # [21]  角
        '飛',   # [22]  飛
        '金',   # [23]  金
        '玉',   # [24]  玉
        'と',   # [25]  と
        '杏',   # [26]  杏
        '圭',   # [27]  圭
        '全',   # [28]  全
        '馬',   # [29]  馬
        '竜',   # [30]  竜      16 + 14

        # # FIXME 駒台。以下の並びは勘
        # '',     # [31]          16 + 15
        # 'ひ',   # [31]  歩
        # '猪',   # [32]  香
        # '兎',   # [33]  桂
        # '猫',   # [34]  銀
        # '犬',   # [37]  金
        # '象',   # [35]  角
        # '麒',   # [36]  飛
    ]


    @classmethod
    def kanji(clazz, piece, is_gote):
        """
        Parameters
        ----------
        piece : int
            先後付きの駒種類。
            打を指定しないように注意してください。
        """

        try:
            token = clazz._kanji_list[piece]
        except IndexError as ex:
            # 36 が入っていることがある。何で？ 持ち駒か？
            print(f"E-48: {piece=} {is_gote=} {ex=}")
            raise

        # 後手なら左側に `v` を付けます。
        if is_gote:
            return f"v{token}"
        return token


    @classmethod
    def on_board(clazz, piece, is_gote):
        token = clazz._kanji_list[piece]

        # 後手なら左側に `v` を付けます。
        if is_gote:
            return f"v{token}"
        
        # 先手なら左側に１つ半角スペースを入れます。
        return f" {token}"
