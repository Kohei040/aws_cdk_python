# HTML&CSS

## HTML

- HTMLは、"Hyper Text Markup Language"の略
- タグ`<>`を使用し、マークアップをする
- ブラウザーがHTMLを解釈/処理して表示することを、レンダリングと呼ぶ

```html
<!DOCTYPE html>
<html lang="ja">
  <head>
    <title>ページタイトル</title>
  </head>
  <body>
    <h1>見出し1</h1>
    <p>本文1</p>
    <h2>見出し2</h2>
    <p>本文2</p>
  </body>
</html>
```

## CSS

- CSSは、"Cascading Style Sheet"の略
- 文書に色付け、文字のサイズ変更、背景の変更等、視覚的な情報をHTMLとは別に記述できる
- タグの中に記述するときは、`style`属性を指定する
- CSSは以下の３箇所に記述できる
    - タグの中
    - style要素の中
    - CSS専用ファイル

```html
<!DOCTYPE html>
<html lang="ja">
  <head>
    <title>ページタイトル</title>

    <! -- CSSの記述 -->
    <style type="text/css">
      body {background-color: #eee;}
      h1#header1 {color: red;}
      h2#header2 {color: blue;}
      p.content  {border:1px solid #000;}
    </style>

  </head>
  <body>
    <h1 id="header1">見出し1</h1>
    <p class="content">本文1</p>
    <h2 id="header2">見出し2</h2>
    <p class="content">本文2</p>
  </body>
</html>
```

### CSSセレクター

- CSSを適用したいタグを指定する記述方法
- HTMLタグの属性を利用し、特定のタグだけを装飾可能
    - class属性
        - HTMLの中で特定のタグを指定するときに利用
        - 重複可能
    - id属性
        - HTMLの中で唯一のタグの指定するときに利用
        - 重複不可

```css
# id属性「header1」を持つh1タグのみにCSSを適用
h1#header1 {color: red; font-size: 140%}

# class属性「contents」を持つpタグのみにCSSを適用
p.content  {border:1px solid #000;}
```

## フォーム`<form>`関連のタグ

- テキストフィールド
    - `<input>`タグの`type`属性に`text`を指定
    - `<input type="text" name="name" size="40">`
- チェックボックス
    - `<input>`タグの`type`属性に`checkbox`を指定
    - `<input  type="checkbox" name="over18">`
- ラジオボタン
    - `<input>`タグの`type`属性に`radion`を指定
    - 複数のタグを用意し、`name`属性に共通の値を指定し、`value`属性に値を指定
    - `<input type="radio" name="sex" value="男"> 男`
    - `<input type="radio" name="sex" value="女"> 女`
- テキストエリア
    - `<textarea>`タグを使用し、`rows`属性に行数を指定
    - `<textarea name="other" rows="5"></textarea>`
- コンボボックス
    - 複数の要素から1つを選択する
    - `<select>`タグで囲み、各要素を`<option>`タグで追加する

```html
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>お名前を入力して下さい</title>
</head>
<body>
<h1>入力フォーム</h1>
<form method="post" action="/output">
    <p>名前：<input type="text" name="name" size="40"></p>
    <p>18歳以上：<input type="checkbox" name="over18"></p>
    <p>性別：
        <input type="radio" name="sex" value="男">男
        <input type="radio" name="sex" value="女">女
    </p>
    <p>所属：
        <select name="belong">
            <option></option>
            <option>東京支店</option>
            <option>千葉支店</option>
            <option>神奈川支店</option>
            <option>埼玉支店</option>
        </select>
    </p>
    <p>その他：</p>
    <button type="submit">送信</button>
</form>
</body>
</html>
```
