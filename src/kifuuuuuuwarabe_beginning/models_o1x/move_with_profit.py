class MoveWithProfit():


    @staticmethod
    def legal_moves_to_list(legal_moves):
        move_wp_list = []
        for move in list(legal_moves):
            move_wp_list.append(MoveWithProfit(
                    move    = move,
                    profit  = 0))
        return move_wp_list


    def __init__(self, move:int, profit:int):
        self._move = move
        self._profit = profit
    

    @property
    def move(self):
        return self._move
    

    @property
    def profit(self):
        return self._profit
