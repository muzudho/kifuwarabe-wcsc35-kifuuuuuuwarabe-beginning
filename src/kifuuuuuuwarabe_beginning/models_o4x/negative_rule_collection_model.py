from ..logics_o3x_negative_rules import \
    DoNotBack, DoNotBreakFamousFence, DoNotBuildRightWall, \
    DoNotDogAndCatSideBySide, \
    DoNotGoLeft, \
    DoNotUpToRank6, \
    DoNotMoveUntilRookMoves, DoNotMoveLeftLance, DoNotMoveRightLance, DoNotMoveRook, \
    WillForThreeGoldAndSilverCoinsToGatherToTheRight, WillNotToMove37Pawn, WillSwingingRook


class NegativeRuleCollectionModel():


    def __init__(self, config_doc):
        # 初期状態では、有効でない行進演算です。
        self._list_of_idle = [
            DoNotMoveRook(config_doc=config_doc),        # 行進［キリンは動くな］  NOTE 飛車を振るまで有効になりません
        ]

        self._list_of_active = [
            DoNotBack                                           (config_doc=config_doc),    # 行進［戻るな］
            DoNotBreakFamousFence                               (config_doc=config_doc),    # 行進［名の有る囲いを崩すな］
            DoNotBuildRightWall                                 (config_doc=config_doc),    # 行進［右壁を作るな］
            DoNotMoveLeftLance                                  (config_doc=config_doc),    # 行進［左のイノシシは動くな］
            DoNotMoveRightLance                                 (config_doc=config_doc),    # 行進［右のイノシシは動くな］
            DoNotGoLeft                                         (config_doc=config_doc),    # 行進［左へ行くな］
            DoNotDogAndCatSideBySide                            (config_doc=config_doc),    # 行進［イヌとネコを横並びに上げるな］
            DoNotUpToRank6                                      (config_doc=config_doc),    # 行進［６段目に上がるな］
            DoNotMoveUntilRookMoves                             (config_doc=config_doc),    # 行進［キリンが動くまで動くな］
            WillForThreeGoldAndSilverCoinsToGatherToTheRight    (config_doc=config_doc),    # ［金銀３枚が右に集まる］意志
            WillNotToMove37Pawn                                 (config_doc=config_doc),    # ［３七の歩を突かない］意志
            WillSwingingRook                                    (config_doc=config_doc),    # ［振り飛車をする］意志
        ]


    @property
    def list_of_idle(self):
        """初期状態では、有効でない行進演算です。
        """
        return self._list_of_idle


    @property
    def list_of_active(self):
        return self._list_of_active
