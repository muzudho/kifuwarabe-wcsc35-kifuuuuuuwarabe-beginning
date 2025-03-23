import os


class ThinkingLoggerModule():
    """指し手に関するロガー。
    """


    def __init__(self, file_name):
        self._file_name = file_name


    def delete_file(self):
        """ログ・ファイルの削除。
        """
        if os.path.exists(self._file_name): # ファイルの存在確認はしなくていいが、エラーメッセージを出したくないので確認している
            try:
                os.remove(self._file_name)
            except FileNotFoundError:   # ファイルが存在しなくても問題ない
                pass


    def append(self, message):
        with open(file=self._file_name, mode='a') as f:
            f.write(f"{message}\n")
