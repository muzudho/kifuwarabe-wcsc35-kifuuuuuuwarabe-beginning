# インストール手順

Windows 11.  

## 手順１：

Power Shell ではなく、 Command Prompt を使う。  


## Python のインストール

以下のフォルダーに Python がインストールされる。  

* 📁 `C:\Users\muzud\`
    * 📁 `anaconda3`
    * 📁 `AppData\Local\Programs\Python`
        * 📁 `Python312`
        * 📁 `Python313`

これらのフォルダーにビルドパスが通されることにより、混線してしまう。  
分からなくなったら、思い切って Python をアンインストールして、Python はマシンに１つだけにしてください。  

また、以下のフォルダーには様々な一時ファイルが置かれる。  

* 📁 `C:\Users\muzud\AppData\Local\Temp`


```shell
# Python にパスを通す必要があれば使う。
# rem set PATH=%%PATH%%;C:\Users\muzud\anaconda3

# ビルドパスが通っている Python のバージョン確認。
python -V
# Python 3.11.7 🌟これで開発。Anaconda3 に入ってるやつ。
# Python 3.12.3
# Python 3.13.3

# 必要なら
# python.exe -m pip install --upgrade pip

# pip のバージョン確認。 19.0 以上が必要。
pip -V
# pip 25.0.1
# pip 25.1


# Python モジュールをインストール。
# インストール・コマンド１行で全部インストールするとエラーになるものがあったので分けた。

# numpy のバージョンは、cshogi に合わせる。
pip install numpy==1.26.4

# cshogi のインストールは、失敗するときがある。
pip install cshogi==0.8.9

pip install exshell==2025042901.0.1

pip install openpyxl
pip install pyxlart
pip install tomlkit
```
