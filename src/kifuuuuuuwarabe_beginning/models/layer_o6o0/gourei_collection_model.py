from ..layer_o4o0_rules.negative import \
    DoNotBackModel, DoNotBreakFamousFenceModel, DoNotBuildRightWallModel, \
    DoNotDepromotionModel, DoNotUpDogAndCatSideBySideModel, \
    DoNotGoLeftModel, \
    DoNotUpToRank6Model, \
    DoNotMoveUntilRookMovesModel, DoNotMoveLeftLanceModel, DoNotMoveRightLanceModel, DoNotMoveRookModel, \
    WillForThreeGoldAndSilverCoinsToGatherToTheRightModel, WillNotToMove37PawnModel, WillSwingingRookModel
from ..layer_o4o0_rules.positive import \
    DoProtectBishopHeadModel


class GoureiCollectionModel():
    """号令コレクション・モデル。
    """


    def __init__(self, basketball_court_model):

        self._positive_rule_list_of_active = [
            DoProtectBishopHeadModel(basketball_court_model=basketball_court_model),    # 訓令［ゾウの頭を守れ］
        ]

        # 初期状態では、有効でない号令です。
        self._negative_rule_list_of_idle = [
            DoNotMoveRookModel(basketball_court_model=basketball_court_model),        # 号令［キリンは動くな］  NOTE 飛車を振るまで有効になりません
        ]

        self._negative_rule_list_of_active = [
            DoNotBackModel                                          (basketball_court_model=basketball_court_model),    # 号令［戻るな］
            DoNotBreakFamousFenceModel                              (basketball_court_model=basketball_court_model),    # 訓令［名の有る囲いを崩すな］
            DoNotBuildRightWallModel                                (basketball_court_model=basketball_court_model),    # 号令［右壁を作るな］
            DoNotDepromotionModel                                   (basketball_court_model=basketball_court_model),    # 号令［成らないということをするな］
            DoNotMoveLeftLanceModel                                 (basketball_court_model=basketball_court_model),    # 号令［左のイノシシは動くな］
            DoNotMoveRightLanceModel                                (basketball_court_model=basketball_court_model),    # 号令［右のイノシシは動くな］
            DoNotGoLeftModel                                        (basketball_court_model=basketball_court_model),    # 号令［左へ行くな］
            DoNotUpDogAndCatSideBySideModel                           (basketball_court_model=basketball_court_model),    # 号令［イヌとネコを横並びに上げるな］
            DoNotUpToRank6Model                                     (basketball_court_model=basketball_court_model),    # 号令［６段目に上がるな］
            DoNotMoveUntilRookMovesModel                            (basketball_court_model=basketball_court_model),    # 号令［キリンが動くまで動くな］
            WillForThreeGoldAndSilverCoinsToGatherToTheRightModel   (basketball_court_model=basketball_court_model),    # ［金銀３枚が右に集まる］意志
            WillNotToMove37PawnModel                                (basketball_court_model=basketball_court_model),    # ［３七の歩を突かない］意志
            WillSwingingRookModel                                   (basketball_court_model=basketball_court_model),    # ［振り飛車をする］意志
        ]


    @property
    def positive_rule_list_of_active(self):
        return self._positive_rule_list_of_active


    @property
    def negative_rule_list_of_idle(self):
        """初期状態では、有効でない号令です。
        """
        return self._negative_rule_list_of_idle


    @property
    def negative_rule_list_of_active(self):
        return self._negative_rule_list_of_active


    def stringify(self):
        labels_of_active_positive_rule = []
        labels_of_idle_negative_rule = []
        labels_of_active_negative_rule = []

        for rule in self.positive_rule_list_of_active:
            labels_of_active_positive_rule.append(rule.label)

        for rule in self.negative_rule_list_of_idle:
            labels_of_idle_negative_rule.append(rule.label)

        for rule in self.negative_rule_list_of_active:
            labels_of_active_negative_rule.append(rule.label)

        return f"""\
ACTIVE POSITIVE RULES ({len(self.positive_rule_list_of_active)})
---------------------
{'\n'.join(labels_of_active_positive_rule)}

IDLE NEGATIVE RULES ({len(self.negative_rule_list_of_idle)})
-------------------
{'\n'.join(labels_of_idle_negative_rule)}

ACTIVE NEGATIVE RULES ({len(self.negative_rule_list_of_active)})
---------------------
{'\n'.join(labels_of_active_negative_rule)}
"""
