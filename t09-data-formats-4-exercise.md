# 継続トレーニング #9：さまざまなデータフォーマットとファイル操作 (4) [演習]

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


## 演習1：GRIB2を処理してみる

GRIB2はデータによって難易度が大きく変わったりするので、
いきなり自分で一から触ろうとすると大変。
なので、今回は、下記記事の内容をそのままやってみる、でよいです！

* [『pythonでgrib2フォーマットのファイルを触れる環境を用意する(Docker編)』](https://qiita.com/mhangyo/items/8494a8039973ba220ce5)
* [『grib2をpython(matplotlib)で地図上で可視化』](https://qiita.com/mhangyo/items/f06debce3975a269a658)
* [『GRIB2をCartopyで地図上に可視化してみる』](https://qiita.com/noritada/items/1f808682b62efffaeced)
