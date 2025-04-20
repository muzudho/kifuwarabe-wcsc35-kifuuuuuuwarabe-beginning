import cshogi


class PlanetPieceTypeModel():
    """地球側と、火星側で分けた駒種類モデル。
    """


    # 地球側
    _earth_kanji_list = [
        ''  ,   # [ 0]
        'ひ',   # [ 1] 歩
        '猪',   # [ 2] 香
        '兎',   # [ 3] 桂
        '猫',   # [ 4] 銀
        '象',   # [ 5] 角
        '麒',   # [ 6] 飛
        '犬',   # [ 7] 金
        '獅',   # [ 8] 玉
        '鶏',   # [ 9] と
        'イ',   # [10] 杏
        'ウ',   # [11] 圭
        'ネ',   # [12] 全
        'ゾ',   # [13] 馬
        'キ',   # [14] 竜
    ]

    # 火星側
    _mars_kanji_list = [
        '',     # [ 0]
        '歩',   # [ 1] 歩
        '香',   # [ 2] 香
        '桂',   # [ 3] 桂
        '銀',   # [ 4] 銀
        '角',   # [ 5] 角
        '飛',   # [ 6] 飛
        '金',   # [ 7] 金
        '玉',   # [ 8] 玉
        'と',   # [ 9] と
        '杏',   # [10] 杏
        '圭',   # [11] 圭
        '全',   # [12] 全
        '馬',   # [13] 馬
        '竜',   # [14] 竜
    ]


    @classmethod
    def kanji_on_board(clazz, piece_type, is_mars, is_gote):
        if piece_type == cshogi.NONE:
            kanji = '　'
        else:
            kanji = PlanetPieceTypeModel.kanji(piece_type=piece_type, is_mars=is_mars)
        
        if is_gote:
            return f"v{kanji}"
        return f" {kanji}"  # 半角空白を頭に付ける


    @classmethod
    def kanji_on_text(clazz, piece_type, is_mars, is_gote):
        kanji = PlanetPieceTypeModel.kanji(piece_type=piece_type, is_mars=is_mars)
        if is_gote:
            return f"v{kanji}"
        return kanji        # 半角空白を頭に付けない


    @classmethod
    def kanji(clazz, piece_type, is_mars):
        if is_mars:
            return PlanetPieceTypeModel.mars_kanji(piece_type=piece_type)
        return PlanetPieceTypeModel.earth_kanji(piece_type=piece_type)


    @classmethod
    def earth_kanji(clazz, piece_type):
        return clazz._earth_kanji_list[piece_type]


    @classmethod
    def mars_kanji(clazz, piece_type):
        return clazz._mars_kanji_list[piece_type]
