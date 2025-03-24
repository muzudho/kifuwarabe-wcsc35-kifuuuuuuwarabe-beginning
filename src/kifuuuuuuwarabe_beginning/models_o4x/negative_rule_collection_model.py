from ..models_o3x_negative_rules import \
    DoNotBackModel, DoNotBreakFamousFenceModel, DoNotBuildRightWallModel, \
    DoNotDogAndCatSideBySideModel, \
    DoNotGoLeftModel, \
    DoNotUpToRank6Model, \
    DoNotMoveUntilRookMovesModel, DoNotMoveLeftLanceModel, DoNotMoveRightLanceModel, DoNotMoveRookModel, \
    WillForThreeGoldAndSilverCoinsToGatherToTheRightModel, WillNotToMove37PawnModel, WillSwingingRookModel


class NegativeRuleCollectionModel():


    def __init__(self, config_doc):
        # 初期状態では、有効でない行進演算です。
        self._list_of_idle = [
            DoNotMoveRookModel(config_doc=config_doc),        # 行進［キリンは動くな］  NOTE 飛車を振るまで有効になりません
        ]

        self._list_of_active = [
            DoNotBackModel                                           (config_doc=config_doc),    # 行進［戻るな］
            DoNotBreakFamousFenceModel                               (config_doc=config_doc),    # 行進［名の有る囲いを崩すな］
            DoNotBuildRightWallModel                                 (config_doc=config_doc),    # 行進［右壁を作るな］
            DoNotMoveLeftLanceModel                                  (config_doc=config_doc),    # 行進［左のイノシシは動くな］
            DoNotMoveRightLanceModel                                 (config_doc=config_doc),    # 行進［右のイノシシは動くな］
            DoNotGoLeftModel                                         (config_doc=config_doc),    # 行進［左へ行くな］
            DoNotDogAndCatSideBySideModel                            (config_doc=config_doc),    # 行進［イヌとネコを横並びに上げるな］
            DoNotUpToRank6Model                                      (config_doc=config_doc),    # 行進［６段目に上がるな］
            DoNotMoveUntilRookMovesModel                             (config_doc=config_doc),    # 行進［キリンが動くまで動くな］
            WillForThreeGoldAndSilverCoinsToGatherToTheRightModel    (config_doc=config_doc),    # ［金銀３枚が右に集まる］意志
            WillNotToMove37PawnModel                                 (config_doc=config_doc),    # ［３七の歩を突かない］意志
            WillSwingingRookModel                                    (config_doc=config_doc),    # ［振り飛車をする］意志
        ]


    @property
    def list_of_idle(self):
        """初期状態では、有効でない行進演算です。
        """
        return self._list_of_idle


    @property
    def list_of_active(self):
        return self._list_of_active


    def dump(self):
        return f"""\
{len(self.list_of_idle)=}
{len(self.list_of_active)=}
"""
