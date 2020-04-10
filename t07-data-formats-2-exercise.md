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


## 演習1：演習1：strftimeで任意のフォーマットで出力してみる

下記をやってみよう。

[datetimeモジュール](https://docs.python.org/ja/3/library/datetime.html)を使って、
現在時刻をRFC 5322とISO 8610フォーマットで出してみよう。
`.isoformat()`というメソッドはあるけど、折角なので、`.strftime()`でやってみよう。

## 演習2：dateコマンドで日時のファイルを作ってみる

下記のようなコマンドをシェルで叩いてみて、
どんなファイルができているか確認してみよう。

```
echo testes > hogehoge-`date '+%Y-%m-%d'`.txt
```

## 演習3：AMeDAS地点テーブルの緯度経度をKMLで表示してみる

前回同様に、KMLを用いて可視化してみよう、という問題。

1. http://pd.wni.co.jp/cgi-bin/cvsweb.cgi/TABLES/AMEDAS.xml から最新（HEAD）のAMEDAS.xmlをダウンロードする。
2. XMLを読み込み、その中の緯度経度をKMLとしてプロットしよう。
3. KMLはGoogle Earthで開いて確認する。
