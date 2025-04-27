class LoggerRoutines():


    @staticmethod
    def DumpDiffError(dump_1, dump_2):
        with open(file='logs/error_in_game.log', mode='w') as f:
            f.write('dump error in search.')

        with open(file='logs/error_in_game_dump_1.log', mode='w') as f:
            f.write(dump_1)

        with open(file='logs/error_in_game_dump_2.log', mode='w') as f:
            f.write(dump_2)
