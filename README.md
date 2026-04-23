# textdancer
textdancerはテキスト操作を扱いやすくするためのモジュールです。

# インストール方法
pipを利用してインストールします。

```
pip install textdancer
```

# クラス
2種類のカテゴリに属するクラスを用意しています。

## Cursor
カーソル機能を提供します。

元々はテキスト行を扱いしやすくするために開発されましたが、
抽象化してあるので、一般的なデータ構造として扱えます。

### RangeCursor
min～maxの値を指すカーソルを定義します。

### SubscriptCursor
配列の添字を扱うためのカーソルです。RangeCursorをラップしたものです。
0～len(variable)-1

## TextChunk
テキストファイルをチャンクとして扱うtextdancerのメインクラスです。

カーソルを保持しているため、fetchしながら操作を行なうことができます。
また、リストの派生クラスであるため、イテレーターを利用する書き方もできます。
イテレーターを利用した場合はカーソルポジションは影響を受けません。

次のコードはfetchとイテレーターをそれぞれ利用した記述方法です。
いずれも同じ結果を返します。

```
chunk = TextChunk(["10", "20", "30", "40", "50", "60"])

while chunk.cursor.hasNext():
    print(chunk.fetchNext())

for line in chunk:
    print(line)
```

また、簡易的なパーサーを書きやすくなるような機能を実装しています。

正規表現リストを用いた行検索機能、行検索機能を用いたpick機能です。
行検索機能はカーソルの影響を受けずに正規表現にマッチする行のポジションを取得できます。
pick機能は内部的に行検索を実行し、見つかった行から最終行、
あるいはカーソルのカレント行から見つかった行までをサブセットとし、
新しいTextChunkとして切り出します。

行検索機能はカーソルの影響を受けませんでしたが、pick機能はカーソル位置が変更されます。
これはテキストのサブセットを取得しながら全行を走査できるようにするためです。

たとえば、次のように書くとテキストを走査し、
ヘッダに紐づくディテールをサブセットとして得られます。

```
chunk = TextChunk([
    "brief 1",
    "  detail 1-1",
    "  detail 1-2",
    "brief 2",
    "  detail 2-1",
    "  detail 2-2",
])

while chunk.cursor.hasNext():
    picked = chunk.pickTo(["^brief.*$"], skipCurrentLineSearch=True)
    if picked:
        print(f"picked: {picked}")
```

実行結果
```
picked: ['brief 1', '  detail 1-1', '  detail 1-2']
picked: ['brief 2', '  detail 2-1', '  detail 2-2']
```

テキストの構成として、いくつかの明細の後に合計を示すものがあります。
このようなデータ構造の場合は、次のように書けば全行を走査しながら必要なサブセットを得られます。
skipCurrentLineSearchパラメーターの代わりにpickToSearchLineパラメーターが利用されている点に注意してください。

```
chunk = TextChunk([
    "detail 1-1",
    "detail 1-2",
    "total 1",
    "detail 2-1",
    "detail 2-2",
    "total 2",
])

while chunk.cursor.hasNext():
    picked = chunk.pickTo(["^total.*$"], pickToSearchLine=True)
    if picked:
        print(f"picked: {picked}")
```

実行結果
```
picked: ['detail 1-1', 'detail 1-2', 'total 1']
picked: ['detail 2-1', 'detail 2-2', 'total 2']
```


