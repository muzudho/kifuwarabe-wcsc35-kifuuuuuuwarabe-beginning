import cshogi
import exshell as xs
import traceback

from pathlib import Path
from src.kifuuuuuuwarabe_beginning.shogi_engine_with_usi import ShogiEngineCompatibleWithUSIProtocol


##########################
# MARK: コマンドから実行時
##########################

if __name__ == '__main__':
    try:
        shogi_engine = ShogiEngineCompatibleWithUSIProtocol()
        shogi_engine.start_usi_loop()

    except Exception as err:
        print(f"""\
おお、残念！　例外が投げられてしまった！
{type(err)=}  {err=}

以下はスタックトレース表示じゃ。
{traceback.format_exc()}
""")