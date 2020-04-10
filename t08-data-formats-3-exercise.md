# 継続トレーニング #8：さまざまなデータフォーマットとファイル操作 (3) [演習]

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


## 演習1：JSONをバイナリデータとして眺めてみる

下記をやってみよう。

`t08/32bit-int.json`というJSONファイルを、
バイナリとして眺めてみよう。

## 演習2：pickleを使ってみる

演習4をやった後でやってみよう。

1. 演習4でアメダスのRUを読み込んだら、そのデータをpickle化して、保存してみよう。
2. そのpickleファイルを別のプログラムから読み込んでみよう。
3. 速度はどうだろうか？

## 演習3：さまざまなRUを眺めてみる

下記をやってみよう。

さまざまなRUをバイナリとして眺めてみよう。

## 演習4：アメダスのRUをKMLに変換してみる

前回同様に、KMLを用いて可視化してみよう、という問題。

1. http://data-catalog.wni.co.jp/data_catalog/view.cgi?tagid=402100915 の一番下にあるstockへのリンクをたどり、適当な日時のアメダスのRUをダウンロードする。
2. 各アメダスの気温の値と経緯度を使って、KMLとしてプロットしよう。気温はアイコンの色を変えられるとbetter。
3. KMLはGoogle Earthで開いて確認する。

[データの仕様書](http://ioc.wni.com/GlobalInfra/D-Corner/puki/pukiwiki.php?cmd=read&page=%BF%B7%B7%C1%BC%B0%A5%A2%A5%E1%A5%C0%A5%B9&word=%BF%B7%B7%C1%BC%B0)

（KMLを使っているのは、
今のところ絵を描く手段や環境として、この場ではKMLしか教えていないためです。
他の手段で絵を描ける場合は、そちらの手段でもかまいません。）
