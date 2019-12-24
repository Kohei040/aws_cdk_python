# Flask

- PythonのWebアプリケーションフレームワーク
- ルーティング(Routing)
    - `@app.route("/")`と指定された場合、`http://ドメイン/`のURLにアクセス
    - 以下の例では、hello関数が実行される

```python
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"
```

## [Jinja2](https://palletsprojects.com/p/jinja/)

- Flaskで利用するテンプレートエンジン
- テンプレートとなるHTMLを用意し、任意のデータを渡す
    1. サーバ側から任意のデータをテンプレートに渡す
    2. そのデータを展開する
    3. HTMLを生成する
    4. レスポンスを返す
- HTMLで受け取るときは`{{ 変数名 }}`で記述する

```python
# hello.py
from flask import Flask, render_template
app = Flask(__name__)


@app.route("/")
def index():
    return render_template('hello.html', hello="こんにちは")
```

```html
# templates/hello.html
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Flask Application</title>
</head>
<body>
<h1>{{ hello }}, Flask</h1>
</body>
</html>
```

- テンプレートのループ処理
    - テンプレートにリスト、辞書を渡すことができ、以下の様に変数の中身を列挙できる
    - `{% for x in list %}{{ x }}{% endfor %}`

```python
# view.py
from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def index():
    week = ['月', '火', '水', '木', '金']
    return render_template('index.html')
```

```html
# templates/index.html
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Flask Application</title>
</head>
<body>
{% for a_day in week %}
    <h3>{{ a_day }}</h3>
{% endfor %}
</body>
</html>
```

## クエリストリング

- Webサーバに追加で情報を与える為にURLに付与する情報
- コンテキストパスの続けて`?`を記述し、`key=value`形式で記述
    - `http://ホスト名/コンテキストパス?key=value`

```python
from flask import Flask, render_template, request
app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/result")
def result():
    fruits = {'1': 'もも', '2': 'りんご', '3': 'みかん'}
    # 値を受け取る
    fruit_no = request.args.get('fruit_no', '')
    return render_template('result.html', fruit=fruits[fruit_no])
```

```html
~~~
<ul>
    <li><a href="/result?fruit_no=1">1番</a></li>
    <li><a href="/result?fruit_no=2">2番</a></li>
    <li><a href="/result?fruit_no=3">3番</a></li>
</ul>
~~~
```

## フォーム(form)

- 画面にデータを入力し、画面から動的にデータを受け取る
- `<form>`タグで囲む
    - `method`はデータの送信方法
    - `action`にはデータの送信先

```python
~~~
@app.route("/output")
def output():
    your_name = request.args.get('name', '')
    return render_template('output.html', name=your_name)
~~~
```

```html
~~~
<form method="get" action="/output">
    <p>名前：<input type="text" name="name"></p>
    <button type="submit">送信</button>
</form>
~~~
```

## `url_for`関数

- Flaskの関数
- 引数に関数名を入れると、`route`メソッドで指定されたアドレスが戻り値になる
- 第二引数に関数の引数に代入する値を指定できる

```python
~~~
@app.route("/output/<fruit_no>/")
def output(fruit_no):
    your_name = request.args.get('name', '')
    return render_template('output.html',
                           name=your_name,
                           fruit=fruits[fruit_no])
~~~
```

```html
~~~
<form method="get" action="{{ url_for('output', fruit_no=fruit_no) }}">
    <p>名前：<input type="text" name="name"></p>
    <button type="submit">送信</button>
</form>
~~~
```

- データの受け取り(POST)

```python
~~~
@app.route("/output", methods=['POST'])
def output():
    # inputタグのname属性を指定する
    your_name = request.form['name']
    return render_template('output.html', name=your_name)
~~~
```

```html
~~~
<form method="post" action="{{ url_for('output')}}">
    <p>名前：<input type="text" name="name" size="40"></p>
    <button type="submit">送信</button>
</form>
~~~
```

- リダイレクト

```python
from flask import Flask, redirect, render_template, request, url_for
app = Flask(__name__)


@app.route("/")
def index():
    return render_template('input.html')


@app.route("/output", methods=['POST'])
def output():
    # inputタグのname属性を指定する
    your_name = request.form['name']
    return redirect(url_for('redirect_test', name=your_name))


@app.route("/redirect_test", methods=['GET'])
def redirect_test():
    your_name = request.args.get('name', '')
    return render_template('output.html', name=your_name)
```

```html
# templates/input.html
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>お名前を入力して下さい</title>
</head>
<body>
<form method="post" action="{{ url_for('output')}}">
    <p>名前：<input type="text" name="name" size="40"></p>
    <button type="submit">送信</button>
</form>
</body>
</html>


# templates/output.html
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>お名前の表示</title>
</head>
<body>
    <h1>入力された名前は「{{ name }}」です</h1>
    <input type="button" onclick="location.href='{{ url_for('index')}}'"value="戻る">
</body>
</html>
```

- テンプレートでif文

```python
# validate.py
from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)


@app.route("/")
def index():
    return render_template('name_input.html')


@app.route("/validate", methods=['POST'])
def validate():
    name = request.form['name']
    name2 = request.form['name2']
    if name != name2:
        error = '入力内容が一致しません'
        return render_template('name_input.html', error=error)

    return redirect(url_for('success'))


@app.route("/success")
def success():
    return render_template('success.html')
```

```html
# templates/name_input.html
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>入力チェック</title>
</head>
<body>
    <h2>同じ内容を入力して、送信ボタンを押す。</h2>
    {% if error %}
    <p><strong> {{ error }}</strong></p>
     {% endif %}
    <form method="POST" action="{{ url_for('validate')}}">
        <p>名前：<input type="text" name="name" size="40" value="{{ request.form.name}}"></p>
        <p>名前(確認用)：<input type="text" name="name2" size="40" value="{{ request.form.name2}}"></p>
        <button type="submit">送信</button>
    </form>
</body>
</html>
```