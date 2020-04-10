# 継続トレーニング #4：HTTPとWeb API -- HTTPの構成要素、Web API、RESTful [演習]

## 準備：今回の教材を手に入れる

第1回と同じリポジトリ（ https://github.com/weathernews/dit-training-FY34 から最新の変更を取り込む。

1. 変更を一時的に退避し、masterブランチに移動
2. masterブランチにupstreamから変更を取り込む
3. masterから適当なブランチ（t03-workなど）を作り、移動
4. t03ディレクトリに移動
5. `./setup.sh <アカウント名>` で、自分用のディレクトリを作成（前回行っていただいたようなファイルのコピーを自動化するためのスクリプト）
6. `t03-hosts` にて、最初に説明した`docker-compose up --build -d`で起動

（Gitに関して、
コマンドからでなくVSCodeなど自分の環境からのほうが楽にバージョン管理の操作ができる場合は、
それでもOKです（フォローはできませんが……）。）

参考：

* [第1回の演習](t01-version-control-exercise.md)
* [第2回](t02-program-lifecycle.md) のdocker-composeの説明
* [第2回の演習](t02-program-lifecycle-exercise.md)


## 演習：EXPO LegacyのAPIを用いてデータを取ってきてみる

[EXPO Legacy Swagger API](https://test-legacy.wni.com/doc/)から、
2019年9月9日（台風15号が上陸した日）のAMEDAS千葉の風速をとってきてみよう。

プログラミング言語はPythonでもPerlでもJavaScriptでも何でもかまわない。
curlコマンドで対話的にやっても、（まずは）OK。


