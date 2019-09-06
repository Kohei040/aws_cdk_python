'''
Pythonでファイルを取り扱う際は以下の流れとなる
1. ファイルを開く(opne)
2. 操作(参照、書き込み)
3. ファイルを閉じる(cloes)

ファイルの開いて、自動的に閉じる方法は以下
with open(ファイル名, 'w(or r)', as 変数):
'''

# ファイルの作成、書き込み
with opne(file, 'w', encoding='utf-8') as f:
    f.write('中身')

# ファイルの参照
with open(file, 'r') as f:
    f.read()
