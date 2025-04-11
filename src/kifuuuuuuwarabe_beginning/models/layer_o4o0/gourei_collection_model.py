from ..layer_o3o1o0_gourei_commands import \
    DoNotBackModel, DoNotBreakFamousFenceModel, DoNotBuildRightWallModel, \
    DoNotDogAndCatSideBySideModel, \
    DoNotGoLeftModel, \
    DoNotUpToRank6Model, \
    DoNotMoveUntilRookMovesModel, DoNotMoveLeftLanceModel, DoNotMoveRightLanceModel, DoNotMoveRookModel, \
    WillForThreeGoldAndSilverCoinsToGatherToTheRightModel, WillNotToMove37PawnModel, WillSwingingRookModel


class GoureiCollectionModel():
    """号令コレクション・モデル。
    """


    def __init__(self, basketball_court_model):
        # 初期状態では、有効でない号令です。
        self._list_of_idle = [
            DoNotMoveRookModel(basketball_court_model=basketball_court_model),        # 行進［キリンは動くな］  NOTE 飛車を振るまで有効になりません
        ]

        self._list_of_active = [
            DoNotBackModel                                           (basketball_court_model=basketball_court_model),    # 行進［戻るな］
            DoNotBreakFamousFenceModel                               (basketball_court_model=basketball_court_model),    # 行進［名の有る囲いを崩すな］
            DoNotBuildRightWallModel                                 (basketball_court_model=basketball_court_model),    # 行進［右壁を作るな］
            DoNotMoveLeftLanceModel                                  (basketball_court_model=basketball_court_model),    # 行進［左のイノシシは動くな］
            DoNotMoveRightLanceModel                                 (basketball_court_model=basketball_court_model),    # 行進［右のイノシシは動くな］
            DoNotGoLeftModel                                         (basketball_court_model=basketball_court_model),    # 行進［左へ行くな］
            DoNotDogAndCatSideBySideModel                            (basketball_court_model=basketball_court_model),    # 行進［イヌとネコを横並びに上げるな］
            DoNotUpToRank6Model                                      (basketball_court_model=basketball_court_model),    # 行進［６段目に上がるな］
            DoNotMoveUntilRookMovesModel                             (basketball_court_model=basketball_court_model),    # 行進［キリンが動くまで動くな］
            WillForThreeGoldAndSilverCoinsToGatherToTheRightModel    (basketball_court_model=basketball_court_model),    # ［金銀３枚が右に集まる］意志
            WillNotToMove37PawnModel                                 (basketball_court_model=basketball_court_model),    # ［３七の歩を突かない］意志
            WillSwingingRookModel                                    (basketball_court_model=basketball_court_model),    # ［振り飛車をする］意志
        ]


    @property
    def list_of_idle(self):
        """初期状態では、有効でない号令です。
        """
        return self._list_of_idle


    @property
    def list_of_active(self):
        return self._list_of_active


    def stringify(self):
        labels_of_idle_rule = []
        labels_of_active_rule = []

        for rule in self.list_of_idle:
            labels_of_idle_rule.append(rule.label)

        for rule in self.list_of_active:
            labels_of_active_rule.append(rule.label)

        return f"""\
IDLE RULES ({len(self.list_of_idle)})
----------
{'\n'.join(labels_of_idle_rule)}

ACTIVE RULES ({len(self.list_of_active)})
------------
{'\n'.join(labels_of_active_rule)}
"""
