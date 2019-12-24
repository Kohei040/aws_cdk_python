# スクレイピング

- スクレイピングをする際は、著作権と利用規約を遵守する
- [サイトマップ](https://www.sitemaps.org/ja/)
    - サイト運営者がクローラーに対してクロールして欲しい情報をURLを列挙するXMLファイル
- robot.txt
    - どのURLを許可しているか、許可していないか等を記述してある
    - 基本的にはURL直下に配置されている
- Webサイトに高負荷をかけないように間隔をあける
    - timeモジュールで、`time.sleep(10)`等とする
- クローラーを開発する際は、連絡先を明示する

## Requestsライブラリ

- URLからHTMLを取得する
- pipでインストールできる
    - `pip install requests`
- 日本語などのマルチバイト文字を取得する場合、エンコーディングの扱いに注意する
    - 以下の１行を追加することで、文字化けは回避できる
    - `xxx.encoding = response.apparent_encoding`

```python
import requests
# 取得したいURL
url = "https://hoge.jp/hoge1"
# HTTPリクエストを送信してHTMLを取得
response = requests.get(url)
response.encoding = response.apparent_encoding
# 取得したHTMLを表示
print(response.text)
```

## [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)ライブラリ

- HTMLの構造を解析することができる
- pipでインストールできる
    - `pip install beautifulsoup4`
- 第一引数にHTMLを渡す
- 第二引数にHTMLパーサーを指定できる
    - `html.parser`等幾つか利用できる

```python
import requests
from bs4 import BeautifulSoup

url = "https://hoge.jp//hoge1.html"
response = requests.get(url)
response.encoding = response.apparent_encoding

bs = BeautifulSoup(response.text, 'html.parser')
# ulタグで囲まれた部分を抽出します
ul_tag = bs.find('ul')

# ulタグの中のaタグを抽出します
for a_tag in ul_tag.find_all('a'):
    # aタグのテキストを取得
    text = a_tag.text
    # aタグのhref属性を取得
    link_url = a_tag['href']
```
