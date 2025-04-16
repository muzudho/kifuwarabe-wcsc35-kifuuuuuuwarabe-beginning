# Kifuuuuuuwarabe Beginning

第３５回世界コンピュータ将棋選手権に出るつもりのきふわらべ  

* 情報
    * 📖 [第35回世界コンピュータ将棋選手権](http://www2.computer-shogi.org/wcsc35/)
* Kifuuuuuuwarabe Beginning 説明書
    * 📖 [インストール手順](./docs/how_to_install.md)
    * 📖 [実行手順](./docs/how_to_start.md)


## 雑記

| 用語 | 読み方 | 意味               | 席                 |
|------|--------|--------------------|--------------------|
| 先手 | せんて | 平手で先に指す方   | 将棋盤の９段目の方 |
| 後手 | ごて   | 平手で後に指す方   | 将棋盤の１段目の方 |
| 上手 | うわて | 駒落ちで先に指す方 | 将棋盤の１段目の方 |
| 下手 | したて | 駒落ちで後に指す方 | 将棋盤の９段目の方 |

平手、駒落ちに関わらず、将棋盤の９段目の方に座っているプレイヤーを指す言葉が欲しいが、無い。  
［９段目の方］ `nine_rank_side_perspective` 略して `np` という単語を造語して使う。NumPyの略ではない。  
いわゆる先手視点だが、紛れを無くしておく。  

この　きふわらべ　では、常に［９段目の方］の視点でプログラミングしていく。  
これは大盤解説の視点と同じ。  

| きふわらべ用語 | 読み方 | 本来の意味 | 意味     |
|----------------|--------|------------|----------|
| Earth          | イース | 地球       | 自分     |
| Mars           | マーズ | 火星       | 対戦相手 |


### TODO 駒表記

TODO 地球はどうぶつ将棋、火星は将棋表記。

|地球|火星|
|----|----|
|ひ  |歩  |
|猪  |香  |
|兎  |桂  |
|猫  |銀  |
|犬  |金  |
|獅  |玉  |
|象  |角  |
|麒  |飛  |
|鶏  |と  |
|イ  |杏  |
|ウ  |圭  |
|ネ  |全  |
|ゾ  |馬  |
|キ  |竜  |


### TODO

* [ ] **FIXME** 駒の取り合いは［後ろ向き］ではなく［前向き］で探索しないとおかしくなるのでは？ 後ろの方で実現しない枝を選んでる。
* [ ] 静止探索の中で、１手目が駒を取らない手のときには、２手目も駒を取らない手（打を含みたい）も探索対象にしたい。
* [ ] 静止探索に時間がかかりすぎている。ノード数を調べたい。
    * [ ] 打つ手は、駒１つ調べれば他の駒種類も同様なのでは？
* [ ] ひとまず、指し手について、ログに残してはどうか。
* [x] 一手詰めを BackwardsPlotModel に入れたい。
* [ ] ベータカット
* [ ] 駒を打つ手は、３手目に駒が取れるとか、そういう駒取りに絡む手を指してほしい。
* [ ] **FIXME** 落ちてる歩を守るより、自陣に駒を打たせない方が得、というのが見えてない。
* [ ] 入玉宣言勝ちしてない
* [ ] 金が三角形の動きをする手待ちを止めさせたい。
* [ ] 放置していると、ただで他の駒を取られる状況を評価してない。
* [ ] 地球と火星の区別を無くす PtolemaicTheoryModel が欲しい。
* [ ] **FIXME** 質駒があるとき、駒を取ることを過小評価してしまう？
* [ ] xs_board コマンド作成
