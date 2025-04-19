class StringResourcesModel:
    """文字列リソース・モデル。
    """


    @staticmethod
    def drop_kanji():
        return '打'
    

    _zenkaku_suji_list = ['０', '１', '２', '３', '４', '５', '６', '７', '８', '９']
    _kan_suji_list = ['〇', '一', '二', '三', '四', '五', '六', '七', '八', '九']


    @classmethod
    def zenkaku_suji_list(clazz):
        """全角数字リスト。１桁。
        """
        return clazz._zenkaku_suji_list


    @classmethod
    def kan_suji_list(clazz):
        """漢数字リスト。１桁。
        """
        return clazz._kan_suji_list
