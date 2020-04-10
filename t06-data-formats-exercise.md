# 継続トレーニング #6：さまざまなデータフォーマットとファイル操作 [演習]

## 準備：今回の教材を手に入れる

第1回と同じリポジトリ（ https://github.com/weathernews/dit-training-FY34 から最新の変更を取り込む。

1. 変更を一時的に退避し、masterブランチに移動
2. masterブランチにupstreamから変更を取り込む
3. masterから適当なブランチ（t06-workなど）を作り、移動
4. t06ディレクトリに移動

（Gitに関して、
コマンドからでなくVSCodeなど自分の環境からのほうが楽にバージョン管理の操作ができる場合は、
それでもOKです（フォローはできませんが……）。）

参考：

* [第1回の演習](t01-version-control-exercise.md)
* [第2回](t02-program-lifecycle.md) のdocker-composeの説明
* [第2回の演習](t02-program-lifecycle-exercise.md)


## 演習1：バッファリングとflushを感じてみる（print()編）

下記をやってみる。何も提出しなくてよい（提出してもよい）。

1. `python3 src/flush-stdout-sample-1.py`を実行する（10秒ほど待っても何も表示されないことを期待）。しばらくしたら`control + C`で止める（一気に表示されるはず）。
2. `python3 src/flush-stdout-sample-2.py`を実行する（きちんと1秒おきに表示されるはず）。しばらくしたら`control + C`で止める。

## 演習2：バッファリングとflushを感じてみる（write()編）

下記をやってみる。何も提出しなくてよい（提出してもよい）。

1. ターミナルを2つ開く。
2. ターミナル1で`python3 src/flush-file-sample-1.py`を実行する。
3. ターミナル2で`tail -f out.txt`を実行する（10秒ほど待っても何も表示されないことを期待）。
4. ターミナル1のプロセスを`control + C`で止める（その瞬間にターミナル2に一気に表示されることを期待）。
5. ターミナル2のプロセスを`control + C`で止める。
6. ターミナル1で`python3 src/flush-file-sample-2.py`を実行する。
7. ターミナル2で`tail -f out.txt`を実行する（きちんと1秒おきに表示されるはず）。
8. ターミナル1のプロセスを`control + C`で止める。
9. ターミナル2のプロセスを`control + C`で止める。
10. `rm out.txt`で出力ファイルを削除しておく。

## 演習3：1行目を無視するプログラム

ヘッダーである1行目を無視して表示するプログラムを書いてください。

読み込むべきファイル：`'data/sample1.csv'`

## 演習4：コメント行を除去するプログラム

コメント行（`'#'`で始まる行）を除去して表示するプログラムを書いてください。

読み込むべきファイル：`'data/sample2.csv'`

## 演習5：最初に現れる空行までを無視するプログラム

最初に現れる空行までを無視するプログラムを書いてください。

読み込むべきファイル：`'data/http_response'`

## 演習6：AMeDAS地点テーブルの緯度経度をKMLで表示してみる

Google Earthを入れていない人はGoogle Earthを入れておこう。
KML化してGoogle Earthで確認するというのは、手軽で何かと便利。
必要に応じてズームもできるので、
ちょっと緯度経度の値がズレていたりしてもわかる（きちんと確認する気があれば）。

1. http://pd.wni.co.jp/cgi-bin/cvsweb.cgi/TABLES/YUBIN_ALL_WNI.CSV から最新（HEAD）のYUBIN_ALL_WNI.CSVをダウンロードする。
2. CSVを読み込み、その中の緯度経度をKMLとしてプロットしよう。
3. KMLはGoogle Earthで開いて確認する。

なお、このCSVは文字コードがShift_JISなので、
以下のように一度openで開いてからcsv.readerで読み込むという特殊な方法で開く必要がある。

```
import csv

with open('YUBIN_ALL_WNI.txt', newline='', encoding='shift_jis') as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)
```

KMLについてはこちらを参照
https://developers.google.com/kml/documentation/kml_tut?hl=ja
