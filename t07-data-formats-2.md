# 継続トレーニング #7：さまざまなデータフォーマットとファイル操作 (2)

## 概要

前回に続き、今回もさまざまなデータフォーマットとファイル操作のお話をします。
前回は基本的なファイル操作、プレーンテキスト、JSON、CSVを説明しましたが、
今回はXML、文字列のフォーマット、フラットバイナリを（時間があればRUも）説明します。

前回同様、どの言語でも共通で知っておくべき一般的な話を中心にしながら、
必要に応じて言語特有の方法に触れていきます。

### 本日お話すること

* XML
  * SGML、HTML、XML
  * XMLのメリット、デメリット
  * DOM
  * XPath
  * さまざまなXML
    * KML
    * SVG
    * macOSのplist
* 文字列のフォーマット
  * 日時
  * タイムゾーン（フォーマットとは少し違うが……）
  * 経緯度
  * 色
* フラットバイナリ
  * エンディアン
  * pack
* RU


## XML

前回チラッと見せたKMLは、XMLという言語の一つの例である。
XMLは、JSONの普及前は最もよく使われるテキストベースのデータフォーマットだった（と思う）。

### SGML、HTML、XML

XMLは、HTMLの兄弟（という言葉は少し微妙だが）であり、
SGMLというマークアップ言語を祖先にもつ。

もともとさまざまな文書を表現できるSGMLというマークアップ言語が1986年に作られた。
「さまざまな文書を表現できる言語」というより、
「文書を表現する言語を作るための言語」というのが正確だ。

* タグを自由に定義できた。
* HTMLには`&amp;`や`&lt;`のような記法（文字実体参照）があるが、
  SGMLではこのようなものを自由に定義して、変数のように使うことができた。
  （`&username;`と書いておいて、処理時に`"Taro Yamada"`に置換する、など。）
* HTMLでは、`<img>`などは終了タグが存在しないし、`<p>`などは省略可能だが、
  同じようにSGMLでも終了タグが省略可能なタグを作れた。

この「文書を表現する言語を作るための言語」で作られたWeb用の言語がHTMLである。
つまりHTMLはSGMLの実装の一つだ。
使えるタグや文字実体参照は決められており、使えるタグの中には、
終了タグが存在しない`<img>`、終了タグが省略可能な`<p>`などが含まれている。

他方で、SGMLはかなり拡張性が高く、様々な表記ができたので、
機能が多すぎて、それらすべてをサポートする処理系を実装するのが大変という問題もあった。
たとえば省略可能な終了タグだ。
終了タグが省略可能ということは、テキストを処理していくときに、
「前のタグが閉じないまま別のタグが現れた」という場合に、
「前のタグの終了タグが省略されたと見なす」
「前のタグは終了せず、新たに登場したタグを子要素と見なす」
のどちらなのかをきちんと場合分けしなければいけない。
タグを自由に定義できる以上、この場合分けもユーザが自由に定義できる。
というより、ユーザが定義してあげないとパーサはどちらなのか判別できない。
つまり、「タグAはタグBのみを子要素として持つことができ、終了タグを省略できる」
といったことが書かれているユーザの定義文書（要は言語仕様）を読み込んで、
その上で目的の文書を読み込む、という2ステップが必要となる。
パーサを作るのが大変なのは想像がつくだろう。

ということで、
こういったSGMLの複雑さを排除した上で「タグを自由に定義できる」機能はそのままとした言語が、
XMLだ。
「データを表現する言語を作れる言語」、すなわち「データを自由に表現できる」言語である。
前述のような経緯から、XMLでは終了タグは省略できない。

たとえば以下は、Pythonのリポジトリに含まれていた簡単なXMLファイルである。

cpython:Lib/test/xmltestdata/simple.xml

```.
<!-- comment -->
<root>
   <element key='value'>text</element>
   <element>text</element>tail
   <empty-element/>
</root>
```

このファイルを作ったユーザの定義文書は存在しないが、
それでもどういう親子関係かは簡単にわかるだろう。

XMLとはつまりこういうものだ：

* タグや属性は自由に定義できる。
* 定義は、書いてもいいし書かなくてもいい。
  * 定義を書けば、
    たとえば「このタグには日付を含めないといけない」など、制約を厳密に検証できる。
  * でも、ちょっと内輪で使うだけだからわざわざ書きたくないというのであれば、それはそれでOK。
* 終了タグは必須。

### XMLのメリット、デメリット

**構造化データ** （情報が構造化されているデータ）という点で、XMLとJSONの市場は似ている。
JSONと比べたときのXMLのメリットやデメリットは、たとえばこんなところだろうか。

メリット：
* 複雑な表現ができる
  * 子要素と属性を使い分けることで、複雑なデータをうまく表現できることがある。JSONだと子要素と属性は平等。
* 多様なデータを表現ができる
  * 日付の型などもXML Schemaには一応定義されている。
* タグの定義（schema）を書けば、文法以上のチェック（妥当性の検証）ができる
  * もっとも、JSON Schemaも開発中の模様。

デメリット：
* 複雑
  * たとえば「付属する情報」を表現したいときに、子要素と属性の2つの選択肢がある。
* schemaを定義しなければ基本的には文字列しか表現できない
  * schemaの定義を書けば、たとえば`"2019-01-01"`は日付とわかり、プログラムが勝手に処理してくれるように仕向けることは可能。ただschemaがなければ、これは単なる文字列にすぎず、自前で変換しないといけない。
* 冗長
  * 開始タグと1文字しか変わらない終了タグを一々書かないといけない。
  * ファイルサイズの肥大にもつながる。

### DOM

Document Object Modelのこと。
[第4回](t04-http-webapi-rest.md)で少し説明したが、APIの1つ。
XMLの木構造のどこかにアクセスしたり、子供を追加したり削除したり、
といったことをするための統一的なインタフェース。

JavaScriptでHTMLをいじるときに理解したかどうかはわからないが、
HTMLは木構造になっている。
XMLも同様。
そこに新たに枝を作ったり切り取ったりするのを、言語によらず統一的な方法でできる。

[MDNのDOMの説明](https://developer.mozilla.org/ja/docs/Web/API/Document_Object_Model)がしっかりしているので、こちらを参照されたい。
たとえば、おおもとの要素（いわゆるルート）には[Document](https://developer.mozilla.org/ja/docs/Web/API/Document)としてアクセスできる。

とはいえ、DOMをそのまま使って書くのはかなり大変なので、
最近は色々なライブラリがもう少し高度なインタフェースを提供してくれている。
JavaScriptでもDOMで書けるが、おそらくそんなことをしている人はあまりいないだろう。
ただ、理解しておくと何をしているかのイメージはつかみやすいはず。

#### Pythonの場合

[xml.etree.ElementTree]https://docs.python.org/ja/3/library/xml.etree.elementtree.html]モジュールを使うのがわかりやすいはず。

### XPath

XML内の場所を文字列で一意に指定できるのがXPathである。

これも、[MDNの説明](https://developer.mozilla.org/ja/docs/Web/XPath)がわかりやすい。


### さまざまなXML

SGMLにHTMLという実装が存在するように、
XMLも「言語を作る言語」なので、実装が色々とある。

#### KML

1つの実装は、前回登場した[KML](https://developers.google.com/kml/documentation/kmlreference?hl=ja)だ。
これは、Google EarthやGoogle Mapsの機能を用いて特定の場所にピンを立てたりするのによく用いられている。


#### SVG

別の実装として、ベクター画像を表現するSVGというフォーマットがある。
たとえば以下は、Jupyterに含まれるホーム用のアイコンのSVG画像である。

jupyterlab:packages/theme-dark-extension/style/icons/md/ic_home_24px.svg

```
<svg xmlns="http://www.w3.org/2000/svg" fill="#E0E0E0" width="24" height="24" viewBox="0 0 24 24"><path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z"/></svg>
```

画像にはラスター画像とベクター画像がある。
前者はビットマップ、要はペイントソフトで描く、塗りつぶしによって構成される絵だ。
圧縮フォーマットを含めれば、PNGをはじめ、さまざまなフォーマットがある。
後者はドロー系ソフトで描く、線で構成される絵だ。
商用のAdobe Illustrator以外に、オープンソースにもいくつかのソフトウェアはあったが、
それぞれ独自のフォーマットを使っており、共通のフォーマットが長らく存在しなかった。
SVGはその共通のフォーマットをXMLベースで定義したものだ。

なお、ベクター画像の特長は、線で構成されるため、拡大しても綺麗に見られる点にある。

### macOSのplist

XMLは、設定の管理に使われていることが結構多い。
macOSではplistというXMLベースのフォーマットが、さまざまな設定情報の管理に使われている。
もっとも、基本的にはバイナリになっているので、中身を見るときは変換してあげる必要がある。

```
noritada[3:29]% plutil -convert xml1 -o - Library/Application\ Support/App\ Store/updatejournal.plist | head -11
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>autoInstalledUpdates</key>
	<array>
		<dict>
			<key>__seenByUser</key>
			<true/>
			<key>artist-name</key>
			<string>Collabora Productivity</string>
```

Chromium（Chromeのunbrandedなオープンソースソフトウェア）のソースコードでも、
macOS用のコンポーネントの一部でplistは見られる。

src:chrome/updater/mac/Info.plist

```
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict/>
</plist>
```


## 文字列のフォーマット

ファイルフォーマットではないが、ここで文字列のフォーマットも説明しておく。
これらは、テキストファイルの中でよく用いられるので、
テキストファイルフォーマットと一緒に説明しておいたほうがよいと考えたためである。

### 日時

気象において日時は重要である。
いつの情報だかわからない気象データに何の価値もないだろう。

「01/08/02」のような日付の表記は、地域によって意味合いが異なる。

* 日本：2001年8月2日
* 英国：2002年8月1日
* 米国：2002年1月8日

ということで、日付（および日時）の表記は重要である。

テキストファイルの中でよく用いられる日時のフォーマットは2種類存在する。

◆参考：[日付の表記に関するノート - The Web KANZAKI](https://www.kanzaki.com/docs/html/dtf.html) …… 昔小林がお世話になったサイト

#### RFC 5322

まず歴史的に長いのが、
[RFC 5322の日付フォーマット](https://tools.ietf.org/html/rfc5322#section-3.3)
である。
RFC 5322は、電子メール（要はメール）の規格を定義したもので、
その日付はたとえば次のような表記となっている。

例：`Thu, 5 Dec 2019 19:20:26 +0900`

おそらくどこかで見たことがあるのではないだろうか。
メールソフトによっては、この表記のままユーザ向けに表示しているものもあるかもしれない。
「何でこんな英語っぽい日付の表記なんだろう？」と思ったかもしれないが、
機械が処理するための規格として表示するために決まっているので仕方がない
（とはいえ、それを人間に見せるかはまた別の問題）。

ちなみに、HTMLの文法はウェブアプリケーションを開発していれば学ばなければならないが、
メールの文法は、今日では知る必要はあまりなく、目にすることもほとんどないだろう。
あまり実用性がなさそうなので、このトレーニングでも特に扱わないが、折角なので見てみよう。
GmailのWeb UIで各メールを表示する画面において、右上に「︙」というボタンがあり、
そこを押すとメニューが出てくる。
その中に「メッセージのソースを表示」という項目があるのでそれを選ぶと、
そのメールのソースが見られる。
これがメールの生の姿である。
たとえば、ヘッダにはこんな行が並んでおり、ほかにも様々な行がある。

```
Subject: <AA3 954> 継続トレーニング #7：さまざまなデータフォーマットとファイル操作 (2)
From: Noritada KOBAYASHI <koba-n@wni.com>
To: DIT WNI <dit@wni.com>, AA3 WNI <aa3@wni.com>
Date: Thu, 5 Dec 2019 19:20:26 +0900
Reply-To: aa3@wni.com
Sender: aa3-request@wni.com
Content-Transfer-Encoding: 8bit
Content-Type: text/plain; charset="UTF-8"
```

なお、[第4回](t04-http-webapi-rest.md)や[第5回](t05-http.md)にて、
こんなHTTPヘッダの例を見た。
実は、HTTPの規格はメールの規格をベースの一つとして作られたので、このように似ている。

```
HTTP/1.1 200 OK
Date: Fri, 08 Nov 2019 00:00:28 GMT
Server: Apache/2.2.24 (FreeBSD) mod_ssl/2.2.24 OpenSSL/0.9.8x PHP/5.3.25 with Suhosin-Patch
Accept-Ranges: bytes
Content-Length: 24617
Content-Type: text/html; charset=none
```

◆参考
* [RFC 822における日時のフォーマット](https://tools.ietf.org/html/rfc822#section-5) …… RFC 822は1982年のメールの規格。年が2桁になっていたり、タイムゾーンとして`GMT`のような文字列を許容していたりするが、HTTPの規格にも取り入れられた。
* [RFC 2822における日時のフォーマット](https://tools.ietf.org/html/rfc2822#section-3.3) …… RFC 2822はRFC 822を置き換えるものとして2001年に作られたメールの規格。

#### ISO 8601

RFC 5322（やおおもとのRFC 822）はいかにも欧米っぽい表記だが、
グローバルな時代にふさわしく定義された表記が、ISO 8601である。
こちらのほうが日本人にも馴染みやすいだろう。

例：
* `2019-12-05T19:20:26+0900`
* `2019-12-05T09:20:26Z`（タイムゾーンがUTCの場合）
* `2019-12-05`（日付だけの場合）

シンプルな基本形式として、
ハイフンとコロンを省いた`20191205T192026+0900`のようなものも定義されていたり、
年間の通算日の表記など、色々なパターンが定義されているが、あまり使わない。

例の日時の記法（`YYYY-MM-DDThh:mm:ssTZD`などと表記）はXML SchemaでdateTime型として取り入れられており、
`YYYY-MM-DD`もdate型として取り入れられているので、XMLを扱う場合はこれらの記法はよく目にするはず。

亜種として、`2019-12-05 19:20:26+0900`のように`T`でなく` `で日付と日時を区切った記法もたまに目にする（これはISO 8601ではない）。

◆参考
* [RFC 3339](http://tools.ietf.org/html/rfc3339) …… 2002年。省略可/不可などわずかな違いはあるが、普段使う分にはISO 8601との違いは気にしなくてよいはず。
* [W3CのDate and Time Formatsの定義](https://www.w3.org/TR/NOTE-datetime)

#### 日時フォーマットのプログラムでの読み書き

RFC 5322の書式をもし扱うことになったらライブラリに任せてしまうのがよいが、
ISO 8601は（タイムゾーンのない`YYYY-MM-DDThh:mm:ss`であれば）シンプルで、
パースしやすいので、自前で読み書きできたほうがよい。

たいていのプログラミング言語には`strftime()`のような名前のメソッドが用意されており、
日時を任意のフォーマットで出力することができる。
たとえば名前に日時を含めたファイルにデータを保存したり、
ユーザ向けに任意のフォーマットで日時を表示したり、といったことはよくあるので、
ある程度のフォーマットは何も見ずに出力できるようになっておくとよい。

また、同様にシェル上で`date`コマンドでも同じことができるので、
これも使えるようになっておくとよい。

ハンズオン：
* 演習1：strftimeで任意のフォーマットで出力してみる
* 演習2：dateコマンドで日時のファイルを作ってみる


### タイムゾーン（フォーマットとは少し違うが……）

グローバルな日時を扱っていると、特定の日時データに関して、
タイムゾーンを別のタイムゾーンに変えたい、ということがよくある。
気象データのタイムゾーンは基本的にUTC（のはず）だが、
ユーザはそれぞれの地域のタイムゾーンで生活しているので、
ユーザ向けに気象データを出そうとしたら、日時はタイムゾーンを変えて表示しなければならない。
また、
たとえば日本企業のビジネスデータの時刻は多くが日本標準時（JST）になっているはずなので、
ビジネスデータと気象データを紐付ける場合、どちらかのタイムゾーンを変えなければならない。

タイムゾーン自体をデータとして扱うことはかなり稀なので、公に定義された書式も存在しない。
ただ、プログラムでタイムゾーンを指定する場合は文字列を使うことが多く、
少し特殊なので、ここで説明しておくことにした。

タイムゾーンの指定に最もよく使われるのは、
`"Asia/Tokyo"`のようなフォーマットの文字列である。
これはtz databaseというデータベースに登録されており、
このデータベースは閏秒などが決まるたびに更新されている。
ほかにどんなタイムゾーンが指定できるかは、Wikipediaのリストを見るのが早いだろう。

https://en.wikipedia.org/wiki/List_of_tz_database_time_zones

macOSであれば、`/usr/share/zoneinfo.default`の下に入っており、
ディレクトリを`ls`すればどんなものがあるか見られる。
なお、中身はバイナリなので、テキストファイルで開いても読めないし、
どんなタイムゾーンがあるか知りたいだけであれば、読んでもあまり意味がない。

```
noritada[0:45]% ls /usr/share/zoneinfo.default
+VERSION	Atlantic	Chile		Eire		GMT		Hongkong	Japan		Mexico		Pacific		Turkey		WET
Africa		Australia	Cuba		Etc		GMT+0		Iceland		Kwajalein	NZ		Poland		UCT		Zulu
America		Brazil		EET		Europe		GMT-0		Indian		Libya		NZ-CHAT		Portugal	US		iso3166.tab
Antarctica	CET		EST		Factory		GMT0		Iran		MET		Navajo		ROC		UTC		posixrules
Arctic		CST6CDT		EST5EDT		GB		Greenwich	Israel		MST		PRC		ROK		Universal	zone.tab
Asia		Canada		Egypt		GB-Eire		HST		Jamaica		MST7MDT		PST8PDT		Singapore	W-SU
noritada[0:45]% ls /usr/share/zoneinfo.default/Asia
Aden		Baghdad		Chita		Dubai		Irkutsk		Kathmandu	Macau		Oral		Sakhalin	Tehran		Urumqi
Almaty		Bahrain		Choibalsan	Dushanbe	Istanbul	Katmandu	Magadan		Phnom_Penh	Samarkand	Tel_Aviv	Ust-Nera
Amman		Baku		Chongqing	Famagusta	Jakarta		Khandyga	Makassar	Pontianak	Seoul		Thimbu		Vientiane
Anadyr		Bangkok		Chungking	Gaza		Jayapura	Kolkata		Manila		Pyongyang	Shanghai	Thimphu		Vladivostok
Aqtau		Barnaul		Colombo		Harbin		Jerusalem	Krasnoyarsk	Muscat		Qatar		Singapore	Tokyo		Yakutsk
Aqtobe		Beirut		Dacca		Hebron		Kabul		Kuala_Lumpur	Nicosia		Qyzylorda	Srednekolymsk	Tomsk		Yangon
Ashgabat	Bishkek		Damascus	Ho_Chi_Minh	Kamchatka	Kuching		Novokuznetsk	Rangoon		Taipei		Ujung_Pandang	Yekaterinburg
Ashkhabad	Brunei		Dhaka		Hong_Kong	Karachi		Kuwait		Novosibirsk	Riyadh		Tashkent	Ulaanbaatar	Yerevan
Atyrau		Calcutta	Dili		Hovd		Kashgar		Macao		Omsk		Saigon		Tbilisi		Ulan_Bator
```

環境変数`TZ`を指定すると、`date`コマンドでの表示を特定のタイムゾーンに変えられる。

```
noritada[0:27]%  TZ="Asia/Tokyo" date
2019年 12月 6日 金曜日 00時27分45秒 JST
noritada[0:27]%  TZ="UTC" date
2019年 12月 5日 木曜日 15時28分18秒 UTC
noritada[0:28]%  TZ="Japan" date      # deprecated (廃止予定) のようだが、一応使える
2019年 12月 6日 金曜日 00時28分24秒 JST
noritada[0:28]%  TZ="JST" date        # JSTという指定は無効なので、UTCで表示される
2019年 12月 5日 木曜日 15時29分31秒 UTC
noritada[0:58]%  TZ="JST-9" date      # POSIXのTZ環境変数の表記
2019年 12月 6日 金曜日 00時58分16秒 JST
noritada[0:57]%  TZ="JST+9" date      # でも符号を間違えるとこうなる
2019年 12月 5日 木曜日 06時58分41秒 JST
```

上記のように、`"JST"`という表記は使えないし、`"JST+9"`と符号を誤ると変なことになるので、
一番安全なのは`"Asia/Tokyo"`のような表記にするのが最も安全だ。


### 経緯度

https://qiita.com/tag1216/items/0b38ee5aedea0ef4a058


### 色

色は、わざわざ書くまでもないだろう。
RGBで

rgb()表記もある。
