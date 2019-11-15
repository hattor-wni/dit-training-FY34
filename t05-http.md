# 継続トレーニング #5：HTTPフォローアップ

## What's New

* 口頭で行った説明を各セクションに追加
* 口頭で行った以外に下記説明を追加：
  * curlコマンドを使ったHEADリクエストの例
  * 401 Unauthorizedの説明
  * 403などを返すと「存在する」ことがバレてしまうため、あえて404を返す場合があることの説明
* その他細かい表現の修正や改善をちらほら

詳細は [weathernews/dit-trainingのコミット履歴](https://github.com/weathernews/dit-training/commits/master) を参照。

## 概要

前回のフォローアップをいくつかします。

### 本日お話すること

* REST説明しなおし
* HTTPメソッド
* ヘッダのさまざまなフィールド
* ステータスコード
* URLとquery stringとpercent encoding
* Chrome上でHTTPを眺める
* PythonでURLを解析する
* PythonでURLを叩いてレスポンスを得る


## REST説明しなおし

前回、「RESTfulでない」という話の中で、こんな話をした：

「ログイン状態などの状態、セッション情報をサーバ側で管理する場合、
全ユーザの状態をサーバ側で管理しないといけないから大変なので、RESTのほうがよい。」

この話は、説明中に自分の頭の中で疑問が湧いてしまい、うまく説明できなかった。
おそらく10年前くらいの知識も入っているので、フォローする。

### ログイン（というより認証・認可）はRESTfulでないのか？

◆そもそも「全ユーザの状態をサーバ側で管理する」ことの何が大変か？

⇒それは、サーバが1台ではないため。
実際には、サーバ1台でサービスを提供することはなく、
大量のサーバ群がサービスを提供しているため、
頻繁に変わる「状態」を管理しようとすると、サーバ群の間でデータを同期する必要が出てくる。

◆でも世の中でログインが必要なWebサービスは大量にないか？

⇒そのとおり。実際、世の中ではこのあたりはあまり問題にならなくなった。

◆ログインやユーザ登録が必要なWeb APIはRESTfulではないのか？

⇒今は、ログインやユーザ登録が必要でもRESTfulと見なされている。
実際、たとえばGoogleなどの有名なAPIの多くが認証やユーザ登録を必要としている。
それは、前回も説明したとおり、
「使われたものの見返りがなく、サーバアクセス増加、インフラ増強によるコスト増加だけ」
になるのは避けたいという、サービス提供側の思惑があるはず。
誰がAPIのどの機能をどのくらい使ったか、というのをきちんと記録し、
利用度に応じて利用制限をかけたり、戦略などに生かしたりしたい（はず）。

なので、最近では、
「REST」の定義において「状態の管理がない」という側面はあまり気にされなくなってきている（ように思うのですが間違っていたら教えてください）。

### ではどんなAPIがRESTfulではないのか？

たとえば、次のように、実行したい関数名とデータをHTTP POSTで送るようなAPIも考えられるが、
これはRESTfulとは言い難い。

```
POST / HTTP/1.1
{"method": "get_list_item", arg: 10}
```

これをREST風に実現するなら、こうなる。

```
GET /list/10 HTTP/1.1
```

同じように、何でもPOSTを使うAPIもRESTfulとは言い難い。

```
POST /DeleteListItem HTTP/1.1
{"id": 10}
```

これをREST風に実現するなら、こうなる。

```
DELETE /list/10 HTTP/1.1
```

あるいは、エラー時にレスポンスとして次のようなものが返ってくるAPIもRESTfulでない。

```
HTTP/1.1 200 OK
（レスポンスヘッダは省略）

{"status": "999", "reason": "No such data"}
```

これをREST風にするとこうなる。

```
HTTP/1.1 404 Not found
```

### つまりRESTとは？

要は、RESTとは、
「HTTPで定義されているメソッドやパス、ステータスコードをうまく使って、シンプルに実現しよう」
という考え方。

HTTPは、URLにある「リソース」にアクセスするための手段。
したがって、RESTも「リソース」としてものを見る。

上のRESTfulでない例で、`/DeleteListItem`は、URLが「機能（アクション）」になっていた。
他方で、RESTfulな例では、URLは`/list/10`というリソースで、
それを削除するというアクションは、`DELETE`というメソッド名で表現されている。

（リソースなので、RESTfulな場合、URLを動詞でなく名詞とすることが多い。）

◆参考：

* [0からREST APIについて調べてみた](https://qiita.com/masato44gm/items/dffb8281536ad321fb08) …… 「RESTなAPIとそうではないAPIの例」がよい
* [HTTPメソッド(CRUD)についてまとめた](https://qiita.com/r_fukuma/items/a9e8d18467fe3e04068e) …… どの目的にどのHTTPメソッドを使うか、という話
* [RESTful API設計におけるHTTPステータスコードの指針](https://qiita.com/uenosy/items/ba9dbc70781bddc4a491) …… どの目的にどのステータスコードを使うか、という話


### RESTにこだわりすぎないことも重要

たとえば、

* カレンダーにイベントを追加する
* カレンダーのイベントを取得する
* カレンダーのイベントを更新する
* カレンダーのイベントを削除する

といった操作であれば、RESTと相性がいい。
ただ、サービスの機能次第なので、どんなAPIもRESTと相性がいいわけではない。

なるべくHTTPのメソッドやパス、ステータスコードをうまく使うという原則に沿いながらも、
最初に書いた「状態管理」のように、RESTと相性がよくないものでも必要に応じて使うのが大切。

## HTTPメソッド

[HTTP/1.1の仕様書](https://tools.ietf.org/html/rfc7231)の目次の4.3を眺めるのがよい。
先程の[『HTTPメソッド(CRUD)についてまとめた』](https://qiita.com/r_fukuma/items/a9e8d18467fe3e04068e)などに記載されているように、基本的にはGET、POST、PUT、DELETEの4種類を知っていればよい。

それ以外としては、HEADもたまに使う。これは、レスポンスのヘッダだけを取得するメソッド。
「データ本体はひとまず要らないけど、更新されたかどうかを知りたい（更新されていたら取得を考える）」というときに使う。
ヘッダだけなので転送データサイズが小さく、サーバへの負荷が少ない。

curlコマンドの`-I`オプションでHEADメソッドを送る例：

```
noritada[12:33]%  curl -I http://ioc.wni.com/img/logo.gif
HTTP/1.1 200 OK
Date: Fri, 15 Nov 2019 03:35:02 GMT
Server: Apache/2.2.24 (FreeBSD) mod_ssl/2.2.24 OpenSSL/0.9.8x PHP/5.3.25 with Suhosin-Patch
Last-Modified: Tue, 28 Jun 2005 10:45:20 GMT
ETag: "607022b-1228-3fa97f6ef1000"
Accept-Ranges: bytes
Content-Length: 4648
Content-Type: image/gif

noritada[12:35]%
```


## ヘッダのさまざまなフィールド

リクエストヘッダについては[HTTP/1.1の仕様書](https://tools.ietf.org/html/rfc7231)の5、レスポンスヘッダについては7を眺めるのがよい。
必要なものがあればもう少し深堀りする機会を作ります。


## ステータスコード

[HTTP/1.1の仕様書](https://tools.ietf.org/html/rfc7231)の目次の6を眺めるのがよい。

よく目にしそうなもの：

* 200 OK：基本的にこれ。
* 401 Unauthorized：そのURLに「何か」あるが、認証を通っていない場合。
* 403 Forbidden：そのURLに「何か」あるが、認証以外でアクセスを拒否された場合。
* 404 Not Found：
  そのURLにコンテンツが見つからない場合。
  アクセス権がない場合に403などを返すと「存在する」ことはバレてしまうので、
  あえて404を返す場合がある。
  たとえばGitHubでprivateなリポジトリを作り、権限がない人がアクセスしようとした場合、
  「404」になりますね。
* 500 Internal Server Error：
  HTTPを返そうとしたのにHTTP以外のレスポンスを返そうとした場合。
  HTTPレスポンスは、ヘッダ＋空行＋ボディです。
  たとえば、HTMLを返すCGIを書いたものの空行の出力を忘れたりすると、500になります。

ちなみに、コード自体は頭の3桁の数字で、Webブラウザなどはこれを見ます。
「OK」「Not Found」などは、そのコードの名称にすぎません。

◆参考：https://en.wikipedia.org/wiki/List_of_HTTP_status_codes


## URLとquery stringとpercent encoding

RESTを理解する上でHTTPとURLの理解が必要ですが、
URLのほうをあまりきちんと説明していなかったので、補足説明します。

たとえば、Googleで「hoge」と検索すると、このようなURLになります。

https://www.google.com/search?q=hoge&oq=hoge&aqs=chrome..69i57j69i65.307j0j1&sourceid=chrome&ie=UTF-8

`?`以降は、query stringと呼ばれます。
これらはURLの引数として与えられたパラメータで、
`key1=value1&key2=value2`のように、
キーと値が連なった形式（Pythonでいうと「辞書」のようなもの）となっています。

◆参考：https://en.wikipedia.org/wiki/Query_string

同じように、Googleで「Webを支える技術」と検索すると、このようなURLになります。

https://www.google.com/search?sxsrf=ACYBGNSo-zoyu4vMSWG1RGVdsmSzWWfD-w%3A1573778237467&source=hp&ei=PfPNXeemGrCzmAX88regDw&q=Web%E3%82%92%E6%94%AF%E3%81%88%E3%82%8B%E6%8A%80%E8%A1%93&oq=Web%E3%82%92%E6%94%AF%E3%81%88%E3%82%8B%E6%8A%80%E8%A1%93&gs_l=psy-ab.3..35i39j0i4i37i32l7.1307.1307..1524...0.0..0.86.160.2......0....2j1..gws-wiz.....10..35i362i39.0OBLYMf8-bg&ved=0ahUKEwinubDm_OrlAhWwGaYKHXz5DfQQ4dUDCAY&uact=5

これは、「URLエンコーディング」「パーセントエンコーディング」などと呼ばれます。
URLに入れられる文字は決まっているので、そこに入らない文字はすべてこのように別の文字に置き換えられます。

上のquery stringの話を考えればわかるでしょう。
`?`は、URLの本体とquery stringの区切りとして使われると決まっている文字です。
同じように、query stringのキーと値を区切るという役割が`=`や`&`にもあります。
こういった文字が他の部分にも入っていたら、機械的に処理できませんよね。


## Chrome上でHTTPを眺める

前回はcurlコマンドでHTTPのヘッダやステータスなどを眺めましたが、
ChromeのDevToolsでも見られます。

![](images/t05-chrome-devtools.png)

（JavaScriptのプログラミングで使ったことがある人もいると思います。）

## PythonでURLを解析する

上で説明したようなURLの解析（URLからquery stringを切り出し、パラメータごとの値にし、percent encodingをデコードする）は、[urllib.parse](https://docs.python.org/ja/3/library/urllib.parse.html)を使うのがよいでしょう。
query stringの切り出し、辞書への変換、percent encodingのデコードなど、個々の操作をやることもできますし、一括して操作することも可能です。
また、逆に辞書などをquery stringにしてURLにくっつけることも可能です。

◆参考：[小ネタ: urllibでURLをパースする・生成する](https://ohke.hateblo.jp/entry/2019/01/19/230000) …… そんなに難しいライブラリでもありませんが、上の公式ドキュメントを読むのが辛ければこういうのをさっと眺めてもよいかもしれません。

同じようなライブラリは他の言語にもあります。


## PythonでURLを叩いてレスポンスを得る

PythonでURLを叩いてレスポンスを得るには、通常はRequestsパッケージを使えば問題ないでしょう。
広く使われていますが、Python同包の標準ライブラリというわけではないので、別途インストールする必要があります。色々な場面でよく使うので、入れておくのがいいと思います。

使い方は、[Requests公式ドキュメントのクイックスタート](https://requests-docs-ja.readthedocs.io/en/latest/user/quickstart/)を見ればすぐわかるはずです。
ステータスコードを得る例など、おそらく使うであろう例はほとんどが載っているはずです。
また、PythonでURLを解析する例を紹介したばかりですが、
「URLにパラメーターを渡す」という例にあるとおり、
パラメータをURLに組み込むにはRequestsだけでいけてしまうこともわかります。

同じようなライブラリは他の言語にもあります。
