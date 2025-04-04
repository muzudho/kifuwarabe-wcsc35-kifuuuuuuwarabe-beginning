import cshogi
import exshell as xs
import sys
import traceback

from tomlkit import parse as toml_parse

from src.kifuuuuuuwarabe_beginning.models.layer_o4o0 import GymnasiumModel
from src.kifuuuuuuwarabe_beginning.shogi_engine_with_usi import ShogiEngineCompatibleWithUSIProtocol


##########################
# MARK: コマンドから実行時
##########################

if __name__ == '__main__':
    try:
        # エンジン名は別ファイルから読込。pythonファイルはよく差し替えるのでデータは外に出したい
        try:
            path_to_config = 'config.toml'
            with open(path_to_config, mode='r', encoding='utf-8') as f:
                # NOTE 標準出力は将棋GUIが対局プロトコルとして読込むので、関係ないものはエラー出力に出します
                print(f'🔧　Read 📄［ {path_to_config} ］config file...', file=sys.stderr)
                config_doc = toml_parse(f.read())

        except FileNotFoundError as ex:
            #print(f"ERROR: '{path_to_config}' file not found.")
            raise

        shogi_engine = ShogiEngineCompatibleWithUSIProtocol(
                gymnasium = GymnasiumModel(
                        config_doc = config_doc))
        shogi_engine.start_usi_loop()

    except Exception as err:
        print(f"""\
おお、残念！　例外が投げられてしまった！
{type(err)=}  {err=}

以下はスタックトレース表示じゃ。
{traceback.format_exc()}
""")