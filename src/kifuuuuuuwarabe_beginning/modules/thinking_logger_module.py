import os


class ThinkingLoggerModule():
    """指し手に関するロガー。
    """


    def __init__(self, file_name, earth_turn):
        self._file_name     = file_name
        self._earth_turn   = earth_turn


    @property
    def earth_turn(self):
        return self._earth_turn


    @earth_turn.setter
    def earth_turn(self, value):
        self._earth_turn = value


    def delete_file(self):
        """ログ・ファイルの削除。
        """
        if os.path.exists(self._file_name): # ファイルの存在確認はしなくていいが、エラーメッセージを出したくないので確認している
            try:
                os.remove(self._file_name)
            except FileNotFoundError:   # ファイルが存在しなくても問題ない
                pass


    def append_message(self, message):
        with open(file=self._file_name, mode='a', encoding='utf-8') as f:
            f.write(f"{message}\n")
