class ResultOfGo():


    def __init__(self, search_result_state_model, alice_s_profit, best_move, length_by_cshogi, length_of_quiescence_search_by_kifuwarabe, length_by_kifuwarabe):
        """［初期化］

        Parameters
        ----------
        search_result_state_model : SearchResultStateModel
            ［探索結果の状態］
        alice_s_profit : int
            ［アリスの得］
        best_move : int
            ［最善手］無ければ［ナン］
        length_by_cshogi : int
            cshogi が示した［合法手の数］
        length_of_quiescence_search_by_kifuwarabe : int
            きふわらべ が静止探索で絞り込んだ［指し手の数］
        length_by_kifuwarabe : int
            きふわらべ が最終的に絞り込んだ［指し手の数］
        """
        self._search_result_state_model = search_result_state_model
        self._alice_s_profit            = alice_s_profit
        self._best_move                 = best_move
        self._length_by_cshogi          = length_by_cshogi
        self._length_of_quiescence_search_by_kifuwarabe = length_of_quiescence_search_by_kifuwarabe
        self._length_by_kifuwarabe      = length_by_kifuwarabe


    @property
    def search_result_state_model(self):
        return self._search_result_state_model
    

    @property
    def alice_s_profit(self):
        return self._alice_s_profit
    

    @property
    def best_move(self):
        return self._best_move
    

    @property
    def length_by_cshogi(self):
        return self._length_by_cshogi
    

    @property
    def length_of_quiescence_search_by_kifuwarabe(self):
        return self._length_of_quiescence_search_by_kifuwarabe


    @property
    def length_by_kifuwarabe(self):
        return self._length_by_kifuwarabe
