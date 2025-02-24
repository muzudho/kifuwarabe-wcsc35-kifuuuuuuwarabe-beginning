# 開発者向けドキュメント


## 持ち駒を数えるテスト

```
# 先手　飛1　角2　　　　　　桂3　香4　歩5　　後手　　　　　　　　　　　　　　　　歩13
position sfen 2sgkgsn1/1r7/9/9/9/9/9/9/2SGKGS2 b R2B3N4L5P13p 1

# 先手　　　　　　金3　銀4　　　　　　　　 　後手　飛1　角2　　　　　　　　　　　歩18
position sfen ln1gk2nl/1r7/9/9/9/9/9/9/LN2K2NL b 3G4Sr2b18p 1

# 先手　　　　　　　　　　　　　　　　1歩13　後手　　　　　　金1　銀2　桂3　香4　歩5
position sfen 3gk4/1r5b1/9/9/9/9/9/1B5R1/1NSGKGS2 b 13Pg2s3n4l5p 1
```


## 歩を突き捨てないテスト

```
lnsgkgsnl/1r5b1/ppppppppp/9/PPPPPPPPP/9/9/1B5R1/LNSGKGSNL w - 1
```
