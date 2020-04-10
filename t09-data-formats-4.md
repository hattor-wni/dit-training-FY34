# 継続トレーニング #9：さまざまなデータフォーマットとファイル操作 (4)

## 概要

過去3回に続き、今回もさまざまなデータフォーマットとファイル操作のお話をします。
今回は前回の続きとしてその他のバイナリファイルについて説明します。

前回同様、どの言語でも共通で知っておくべき一般的な話を中心にしながら、
必要に応じて言語特有の方法に触れていきます。

### 本日お話すること

* RUフォロアップ
* BUFR / GRIB / GRIB2
  * 苦労する点
  * 苦労するかもしれないデータの例
  * 実際のプログラムでの処理
* よく使われる圧縮ファイルやアーカイブ
  * gzip / bzip2 / xzのファミリー
  * 解凍せずに処理する
  * プログラムにおいて解凍せずに処理する
  * パフォーマンスの違い
  * tar
  * zip
  * 実はzipなファイルたち
  * 可逆圧縮と非可逆圧縮：JPEGとフーリエ変換
* プログラムを用いたファイルシステムでの作業
  * 今いるのはどこ？
* ファイルシステムでのファイル処理
  * Pythonでのglobbingやファイル操作、ファイル名操作


## RUフォロアップ

前回、RUについて扱った。次のような内容であった。

* RUは、セパレータを挟んでヘッダ部とボディ部からなるデータフォーマットである
* ヘッダ部はテキストで行単位で記述されている
* セパレータは`^D^Z` (`0x041a`) である
* ボディ部は、ヘッダ内の`format`フィールドに記述された形式で、
  バイナリデータとして格納されている。

これについて、補足する。

これまで、JSONやCSV、XMLなどさまざまなフォーマットの話をした。
また、このあともGRIB2などの話をする。
**こういった他フォーマットのデータも、現在、社内では基本的にRUとして流通している。**
どういうことかというと、流したいデータの頭にRUのヘッダ部とセパレータをつけて、
ボディ部をそのデータそのものとして送信されている。

アメダス地点テーブル（[TagID:431020007](http://data-catalog.wni.co.jp/data_catalog/view.cgi?tagid=431020007)の最新版、t09/20191219_025315.000 を見るとすぐにわかるはず。

```
noritada[22:49]%  hexdump -C t09/20191219_025315.000 | head -15
00000000  57 4e 0a 68 65 61 64 65  72 5f 76 65 72 73 69 6f  |WN.header_versio|
00000010  6e 3d 31 2e 30 30 0a 64  61 74 61 5f 6e 61 6d 65  |n=1.00.data_name|
00000020  3d 41 4d 45 44 41 53 2e  78 6d 6c 0a 67 6c 6f 62  |=AMEDAS.xml.glob|
00000030  61 6c 5f 69 64 3d 30 30  32 35 0a 63 61 74 65 67  |al_id=0025.categ|
00000040  6f 72 79 3d 37 30 30 30  0a 64 61 74 61 5f 69 64  |ory=7000.data_id|
00000050  3d 33 31 30 32 30 30 30  37 0a 63 72 65 61 74 65  |=31020007.create|
00000060  64 3d 32 30 31 39 2f 31  32 2f 31 39 20 30 33 3a  |d=2019/12/19 03:|
00000070  30 30 3a 34 39 20 47 4d  54 0a 61 6e 6e 6f 75 6e  |00:49 GMT.announ|
00000080  63 65 64 3d 32 30 31 39  2f 31 32 2f 31 39 20 30  |ced=2019/12/19 0|
00000090  32 3a 35 33 3a 31 35 20  47 4d 54 0a 72 65 76 69  |2:53:15 GMT.revi|
000000a0  73 69 6f 6e 3d 31 0a 64  61 74 61 5f 73 69 7a 65  |sion=1.data_size|
000000b0  3d 33 32 32 32 31 30 35  0a 68 65 61 64 65 72 5f  |=3222105.header_|
000000c0  63 6f 6d 6d 65 6e 74 3d  41 4d 45 44 41 53 2e 78  |comment=AMEDAS.x|
000000d0  6d 6c 0a 66 6f 72 6d 61  74 3d 2b 49 4e 54 38 0a  |ml.format=+INT8.|
000000e0  04 1a 3c 3f 78 6d 6c 20  76 65 72 73 69 6f 6e 3d  |..<?xml version=|
```

このようなデータファイルについては、
当然ながら、ヘッダ部とセパレータを取り除いてしまえば、
ふつうにファイルとしてアクセスできる。
要は、ボディ部のデータサイズが正しいと仮定できれば、
`^D^Z` (`0x041a`) が登場するところまで取り除いてしまえばよい。
[cutruhead](http://pd.wni.co.jp/cgi-bin/cvsweb.cgi/fads/cuthead/)
という非常に小さなプログラムが社内にあるが、そんなものを使わなくても自分で処理できるはず。


## BUFR / GRIB / GRIB2

世界気象機関（WMO）の規定する気象データのフォーマットは色々あるが、
BUFR、GRIB、GRIB2はその中のバイナリデータフォーマットで、
社外の気象機関から入ってくるデータや社内のモデルデータはこのフォーマットになっていることが多い。

[前回](t07-data-formats-2.md)書いたように、
GRIBは、気象関連の分野に多い配列データを格納するためのフォーマットである。
GPVと略される格子点値 (grid point value) の格納に使われる。
BUFRは、非格子データ用のフォーマットである。

GRIB2はGRIBのバージョン2であり、次のようにsection構造が異なっている。

GRIB1:
* SECTION 0 Indicator section
* SECTION 1 Product definition section
* SECTION 2 (Grid description section)
* SECTION 3 (Bit-map section)
* SECTION 4 Binary data section
* SECTION 5 7777 (End section)

GRIB2:
* SECTION 0 Indicator Section
* SECTION 1 Identification Section
* SECTION 2 (Local Use Section)
* SECTION 3 Grid Definition Section
* SECTION 4 Product Definition Section
* SECTION 5 Data Representation Section
* SECTION 6 (Bit-map Section)
* SECTION 7 Binary Data Section
* SECTION 8 End Section

GRIB1は多次元データやアンサンブルデータに弱いなどの理由で、GRIB2が開発されたらしい。

フォーマットの詳細は、最近、気象庁予報部の豊田さんが個人的に色々記事を書いてくださっており、
あまりにもしっかりと書けているので、自分が説明するまでもない気がする。
[豊田さんの記事](https://qiita.com/e_toyoda)や、
[気象庁の技術情報](http://www.data.jma.go.jp/add/suishin/cgi-bin/jyouhou/jyouhou.cgi)を読むのが一番近道だろう。

* [気象通報式に関する記事まとめ](https://qiita.com/e_toyoda/items/b85d4995c5845cb27381)
* [BUFRとは](https://github.com/etoyoda/bufrconv/blob/master/BUFR.md)
* [WMO（世界気象機関）の格子データ形式GRIB2について](https://qiita.com/e_toyoda/items/ce7497e1a633b16f1ff1)

### 苦労する点

豊田さんの記事内でも触れられているが、実務で苦労する点を書いておく。
BUFRやGRIBで何が問題かというと、符号表というのがある点である。
たとえば格子点の位置に関わる図法1つとっても様々なものがあるし、
データの圧縮方法についても色々なものがある。
それらを1つ1つに仕様として番号が定義され、
処理プログラム内でその番号に相当する読み取り機能（1バイト目は○○を意味し……など）が実装されている。
データ内で、各sectionのテンプレート番号を読み、
その上でその番号に基づいてデータの詳細を読まないといけない。

要は、データ内の各sectionを次のようにして読む。

1. section前半に含まれるさまざまな共通パラメータを読む
2. 共通パラメータの1つとして定義されている、sectionのテンプレート番号も読み取れる
3. section後半は、符号表で定義されているテンプレート番号の意味にしたがって読む必要がある

テンプレート番号の種類が少なければたいして問題ではないが、
テンプレート番号の種類は多いし、WMOの符号表で定められているもの以外に、
「地域的使用のため予約」されている番号の範囲があって、
そこは、たとえば日本は日本ローカルの表を使ってよいようになっている。
そして、日本の気象庁はかなりその日本ローカルの表を使っており、
そのような機能は、GRIB処理ソフトウェアによってはサポートされていなかったりする。

簡単にまとめると：

* GRIB処理ソフトウェアは、さまざまな場合分けに対応しないといけない
  * 一般に、場合分けが多いと、ソフトウェアは非常に複雑であると見なされる
* 地域の番号定義に基づく挙動を必要とするデータが存在する
  * （日本気象庁の）GRIBデータと海外で作られたソフトウェアの組み合わせによっては、
    処理がエラーになる場合がある

ということを理解した上で、心してGRIBに挑むのがよいと思う。
うまくいかない場合に自分のプログラムを原因自分論で冷静に見つめ直すのは、
プログラミングにおいては重要だけど
（「使っているライブラリのバグか？」と思うときは、だいたい自分のミス）、
GRIBに関してはそうでないことも結構あるので、
たとえばほかのデータ（他国で作られたものなど）に変えてみる、
テンプレート番号が「地域的使用のため予約」されているものか確認する、
などが有効かと思う。

### 苦労するかもしれないデータの例

たとえば、以下の技術情報を見ればわかるが、
4.50008とか4.50011などといったテンプレート番号を使っており、
符号表としてJMAのものを参照するようになっている。

* [1km メッシュ全国合成レーダーGPVの技術情報](http://www.data.jma.go.jp/add/suishin/jyouhou/pdf/162.pdf)
* [高解像度香水ナウキャストの技術情報](http://www.data.jma.go.jp/add/suishin/jyouhou/pdf/398.pdf)

これらは、「もしかしたら地雷かも」と思ってかかるとよい（笑）。

### 実際のプログラムからでの処理

Pythonでは、[pygrib](https://jswhit.github.io/pygrib/docs/)を使うのがよい。
具体的には、[『pythonでgrib2フォーマットのファイルを触れる環境を用意する(Docker編)』](https://qiita.com/mhangyo/items/8494a8039973ba220ce5)、[『grib2をpython(matplotlib)で地図上で可視化』](https://qiita.com/mhangyo/items/f06debce3975a269a658) (by @mhangyo さん) などを参照するのがよいだろう。

ただ、たぶん日本の全国合成レーダーのGRIB2などだと、
前述の理由により上記の方法ではうまくいかないはず。
うまくいかない場合は、（ソフトウェアを直すのが一番正しいと思うのだけど、）
NCEPの公開している
[wgrib2](https://www.cpc.ncep.noaa.gov/products/wesley/wgrib2/)
でGRIB2をバイナリに落とす方法が、社内ではよくとられているようだ（あまり自分はやったことがない）。
具体的には、「wgrib2 bin」などで検索すれば[『pythonでGRIB2形式のバイナリファイルからレーダーエコー強度画像を作成する（画像作成編）』](https://qiita.com/kinosi/items/6f4f754f3f88f1fd74b4)などの記事が出てくるので、そういった記事を参照するとよい。
またwgrib2は一般的なパッケージ管理システム（DebianやUbuntuのapt、CentOSのyumなどのこと）ではあまり提供されていなかったりするので、ソースからインストールする必要があることが多い。その場合は[『wgrib2をDockerコンテナにインストールした話』](https://qiita.com/KentoDodo/items/c8f1dc7fb902c07e817e) (by @KentoDodo さん) などを参照するのがよい。


## よく使われる圧縮ファイルやアーカイブ

このあたりは使えば覚えられる話なのでサクッと。
一般ユーザの世界では圧縮ファイルとしてzipがよく使われるが、
プログラミングの世界で最も多いのはgzip, bzip2, xz。
複数のファイルをつなげるtarと一緒に使われる。

gzip, bzip2, xzは、1つのファイルを圧縮するためのツールの名前であり、フォーマットである。
一般ユーザの世界でよく使われるzipは、複数のファイルをまとめた上で圧縮してくれるので、
gzip, bzip2, xzとこの点で異なる。
「複数のファイルをまとめる」役割を果たすのはtar。

### gzip / bzip2 / xzのファミリー

以下のような感じで、ログファイルはよく圧縮されていたりする。

```
> ls /var/log/messages*
/var/log/messages
/var/log/messages.0.bz2
/var/log/messages.1.bz2
/var/log/messages.2.bz2
/var/log/messages.3.bz2
/var/log/messages.4.bz2
```

`.gz`なら`gzip`コマンドのファミリー、
`.bz2`なら`bzip2`コマンドのファミリー、
`.bz2`なら`xz`コマンドのファミリーで処理する。
「処理する」とは下記のようなこと：

* 圧縮ファイルを作るなら`gzip`
* 圧縮ファイルを展開するなら`gunzip`
* 圧縮ファイルの中身を`cat`のように表示するなら`zcat`
* 圧縮ファイルの中身を`less`のようにページャで眺めるなら`zless`
* 圧縮ファイルの中身を`grep`のように検索するなら`zgrep`

`gzip`の場合、下3つは頭が`z`なのが特殊だけど、
`bzip2`、`xz`はすべて頭を`bz`と`xz`にすればよい。

### 解凍せずに処理する

上にコマンドを示したことからわかるように、一般ユーザの圧縮のイメージとは異なり、
展開しなくても中身は見れるし調べられる。
より正確に言えば、**ファイルシステム上に展開しなくても中身は見れるし調べられる**。
これは重要。

なんとなく「圧縮されたものを使いたければ、展開する必要がある」というイメージがあると思うが、
1ファイルのみを圧縮している場合、展開しなくても作業できる。
というより、10倍程度のファイルサイズになってしまうので、
場合によってはコンピュータ内のディスク領域を占有してしまうし、
そのような巨大なファイルを書き込む時間も馬鹿にならないことがある。
それに、展開したファイルは、たいていの場合一時的にしか使わず、あとで削除する必要がある。
それを消し忘れると、無駄なスペースを占有する粗大ゴミができてしまう。
なので、圧縮されたファイルは、**なるべくファイルシステム上に展開せずに使う**ことが大切。

### プログラムにおいて解凍せずに処理する

「解凍せずに処理する」というのは、コマンドから使うときだけではない。
さまざまなプログラミング言語で、プログラムから「解凍せずに処理」できるようになっている。

たとえばPythonの場合は以下のモジュールを使う：

* [gzipモジュール](https://docs.python.org/ja/3/library/gzip.html)
* [bzip2モジュール](https://docs.python.org/ja/3/library/bz2.html)
* [lzmaモジュール](https://docs.python.org/ja/3/library/lzma.html)

通常のファイルを開くときに`open`するのとまったく同じ感覚で使えるので、活用しよう。

```
import gzip
with gzip.open('hoge.txt.gz', 'rb') as f:
    file_content = f.read()
```

### パフォーマンスの違い

検索すれば色々と出てくるが、一般的な感覚としては：

* gzip: 圧縮速度は速くはない、解凍速度は速い、圧縮サイズは中程度
* bzip2: 圧縮速度は速い、解凍速度は遅い、圧縮サイズはまぁ小さい
* xz: 圧縮速度は遅い、解凍速度は速い、圧縮サイズは小さい

なので、たとえばLinuxのソースコードような巨大なデータを配布する場合、
サイズが重要となるので通常はxzを使っている。
一方、ログなどは圧縮速度が求められたりするのでbzip2だったりする。

### tar

```
% tar zcvf hoge.tar.gz hoge   # hoge内のファイルをアーカイブをhoge.tar.gzに固める
% tar tf hoge.tar.gz          # hoge.tar.gz内のファイルの一覧を表示
% tar xvf hoge.tar.gz         # アーカイブを展開
```

`zcvf`などはオプション。
Unixの世界では通常、`-h`などのshort option、`--help`などのlong optionがあり、
short optionは`-la`などと複数繋げられる、などといった話は理解していると思う。
`tar`は特殊で、ハイフンなしで使うことが多い。ハイフンをつけてもよいけど。

`zcvf`などのオプションの順序は、教える人によって違うかもしれない。
自分は左手の指が動かしやすいのでこの順序で覚えている。
`z`はgzipでの圧縮を意味する。
ほかは`man tar`などでマニュアルページを見て調べてください。
展開時などに`z`を指定していないのは、展開時に圧縮フォーマットを勝手に判別してくれるから。
ほとんどの用途では上の3つのケースなので、
1つ1つのオプションを細かく考えたりはせず、指が自然に動くようになったほうがよい。

gzip圧縮をする`z`以外に、`j`を使うことでbzip2圧縮、`J`を使うことでxz圧縮ができる。
何も指定しないと圧縮はされない。

ちょっと特殊な使い方として、こんな使い方もする。

```
% tar -C /home/koba-n/work -cf - . | tar -C /mnt/hoge -xf -
```

これは、次のようなことをしている：

1. `/home/koba-n/work`に移動する
2. そのディレクトリ（`.`）内のファイルを固めて（圧縮せず）、`-`（標準出力の意味）に送る
3. `/mnt/hoge`に移動する
4. `-`（標準入力の意味）から送られてきたファイルを展開する

簡単に言うと、`/home/koba-n/work`の内容を`/mnt/hoge`にコピーしている。

さらに、こういう使い方もする：

```
% tar -C /home/koba-n/work -cf - . | ssh host-a tar -C /mnt/hoge -xf -
```

これは、やっていることは同じだが、
ローカルの`/home/koba-n/work`の内容をSSHで別ホストhost-aの`/mnt/hoge`にコピーしている。
まぁ、要は`scp`のようなことをしている。

`cp`や`scp`で何故いけないのか？
いけなくはないけど、指定したファイルを1つずつコピーするよりも、
複数のファイルをストリームで送ってコピーしてしまったほうが速いという考え方に基づく。
もしかしたら今では変わらないかもしれない（きちんと調べていない）。

### zip

WindowsやmacOSをふつうに使っているとたまに出会うzipは、
プログラムから使うことはそんなに多くない。
もし使う場合は、`zip`コマンドや`unzip`コマンドを使う。
Unixではそんなに必要とならないので、場合によってはデフォルトで入っていないこともある。
使い方は調べよう。

プログラムから使うためのインタフェースも、各言語で用意されている。
Pythonの場合は以下のモジュールとなる：

* [zipfileモジュール](https://docs.python.org/ja/3/library/zipfile.html)

### 実はzipなファイルたち

zipは、「複数のファイルを1ファイルに見せる」という意味では便利なフォーマットである。
`.zip`でない拡張子を使っているけど、実はzipなものたちがある。
たとえばMicrosoft Office 2007からデフォルトフォーマットとなった、`x`で終わるファイル群。

```
noritada[2:38]%  unzip -l t09/hoge.pptx
Archive:  t09/hoge.pptx
  Length      Date    Time    Name
---------  ---------- -----   ----
     7015  12-12-2019 03:27   ppt/theme/theme1.xml
     7000  12-12-2019 03:27   ppt/theme/theme2.xml
    10982  12-12-2019 03:27   ppt/notesMasters/notesMaster1.xml
      291  12-12-2019 03:27   ppt/notesMasters/_rels/notesMaster1.xml.rels
     6848  12-12-2019 03:27   ppt/notesSlides/notesSlide1.xml
      310  12-12-2019 03:27   ppt/notesSlides/_rels/notesSlide1.xml.rels
     2710  12-12-2019 03:27   ppt/slideLayouts/slideLayout1.xml
      445  12-12-2019 03:27   ppt/slideLayouts/_rels/slideLayout1.xml.rels
     5373  12-12-2019 03:27   ppt/slideLayouts/slideLayout2.xml
      310  12-12-2019 03:27   ppt/slideLayouts/_rels/slideLayout2.xml.rels
     2695  12-12-2019 03:27   ppt/slideLayouts/slideLayout3.xml
      445  12-12-2019 03:27   ppt/slideLayouts/_rels/slideLayout3.xml.rels
    22879  12-12-2019 03:27   ppt/slideMasters/slideMaster1.xml
     1023  12-12-2019 03:27   ppt/slideMasters/_rels/slideMaster1.xml.rels
    40244  12-12-2019 03:27   ppt/slides/slide1.xml
      461  12-12-2019 03:27   ppt/slides/_rels/slide1.xml.rels
      896  12-12-2019 03:27   ppt/presProps.xml
     6074  12-12-2019 03:27   ppt/presentation.xml
     1455  12-12-2019 03:27   ppt/_rels/presentation.xml.rels
      301  12-12-2019 03:27   _rels/.rels
    40577  12-12-2019 03:27   ppt/fonts/HelveticaNeue-italic.fntdata
    33737  12-12-2019 03:27   ppt/media/image2.jpg
    38465  12-12-2019 03:27   ppt/fonts/HelveticaNeue-bold.fntdata
     3372  12-12-2019 03:27   ppt/media/image1.jpg
    38607  12-12-2019 03:27   ppt/fonts/HelveticaNeue-regular.fntdata
    39758  12-12-2019 03:27   ppt/fonts/HelveticaNeue-boldItalic.fntdata
     1926  12-12-2019 03:27   [Content_Types].xml
---------                     -------
   314199                     27 files
```

たとえば電子書籍のフォーマットであるePubのファイル。

```
noritada[2:52]%  unzip -l t09/book.epub
Archive:  t09/book.epub
  Length      Date    Time    Name
---------  ---------- -----   ----
       20  12-19-2019 17:51   mimetype
      250  12-19-2019 17:51   META-INF/container.xml
      533  12-19-2019 17:51   OEBPS/book.xhtml
      778  12-19-2019 17:51   OEBPS/book-toc.xhtml
    45125  12-19-2019 17:51   OEBPS/images/ch01-imgsample.jpg
   114018  12-19-2019 17:51   OEBPS/images/cover.jpg
      778  12-19-2019 17:51   OEBPS/colophon.xhtml
      533  12-19-2019 17:51   OEBPS/titlepage.xhtml
      573  12-19-2019 17:51   OEBPS/ch01.xhtml
     8056  12-19-2019 17:51   OEBPS/style.css
     2473  12-19-2019 17:51   OEBPS/book.opf
---------                     -------
   173137                     11 files
```

### 可逆圧縮と非可逆圧縮：JPEGとフーリエ変換

このスライドを見てほしい。
というか、このスライドの例示がわかりやすかったので、JPEGの話ではなく、
わざわざ「JPEGとフーリエ変換」という話にしていたりする。

[フーリエ変換と画像圧縮の仕組み](https://www.slideshare.net/ginrou799/ss-46355460)

圧縮には可逆圧縮と非可逆圧縮がある。
たぶんそれは知っている……よね？

可逆圧縮はなんとなくイメージしやすい。
赤色が縦100マス、横100マス並んだ画像があるとして、
それをすべて「赤赤赤赤赤……」と書いてあげるよりも、
「赤10000個」と書いたほうが圧倒的に短くなるのは直感的だ。

非可逆圧縮は具体的に少しイメージしにくいと思うので、このフーリエ変換の話を入れておいた。
何らかの方法で、少ない情報から「ほぼ同じ」ものを作るのが非可逆圧縮である、
というイメージが持てれば幸いだ。
「面白い！」と思ってもらえればさらに嬉しい。


## プログラムを用いたファイルシステムでの作業

ファイルフォーマットではないが、折角なのでファイルつながりということで、
ファイルシステムの話をしておく。
ターミナルを立ち上げてシェル上でコマンドを色々打ってファイル操作するのを自動化したい、
というのはよくあるので、それに関する話を簡単にする。

### 今いるのはどこ？

気をつけなければいけないのは、
「どこを『今いる場所』としてプログラムが実行されているか」だ。
プログラムからファイルなどを相対パスで指定して読む場合、
「そのプログラムに対する相対パス」を指定してもプログラムは読んでくれない。

```
noritada[3:15]%  cat t09/sample.py
with open("README.md") as f:
    print(f.read())
noritada[3:15]%  ls README.md
README.md
noritada[3:14]%  python3 t09/sample.py
# DIT継続トレーニングカリキュラム
[snip]
noritada[3:14]%  cd t09
noritada[3:16]%  ls README.md
ls: README.md: No such file or directory
noritada[3:14]%  python3 sample.py
Traceback (most recent call last):
  File "sample.py", line 1, in <module>
    with open("README.md") as f:
FileNotFoundError: [Errno 2] No such file or directory: 'README.md'
```

なんとなく、いつも自分が手で作業する場所にいるつもりで、
不適切な相対パスを書いてしまうことは最初のうちは誰しもがやってしまうことなのでご注意を。

### Pythonでのglobbingやファイル操作、ファイル名操作

おそらく多くの人にとってシェルの便利な点の一つは、
`*.py`のようなワイルドカードでファイルを指定できることだろう。
ワイルドカードでファイルを選んだりするのをglobbingと言ったりする。

ただ、このワイルドカードはシェルの機能なので、
たとえばこんなPythonコードは書けない。

```
with open("*.txt") as f:
```

このようなワイルドカード含め、以下のようなことをするには、
[pathlibモジュール](https://docs.python.org/ja/3/library/pathlib.html)
を使うのがよい。

* ワイルドカードにマッチするファイルの一覧を得る
* ファイルパスからディレクトリ部分を取り除いてファイル名を得る
* 逆に、親ディレクトリとファイル名をつなげる
* `chmod`、`mv`、`rm`、`mkdir`など、基本的なファイル操作をする
