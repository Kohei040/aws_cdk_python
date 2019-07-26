# tblsとは
- DB情報をMarkdown形式等で出力することができるOSSツール
- [Source](https://github.com/k1LoW/tbls)
- [参考手順](https://qiita.com/k1LoW/items/2010413a8547b1e6645e)

## 環境構成
今回はDokcerで実行する方法となります　※tbls自体はgoで動きます
事前にDockerを[インストール](https://docs.docker.com/docker-for-windows/install/)してください

```
tbls/
└ conf/.tbls.yml     # ".tbls.yml"にDBの接続情報を記述します
├ Output/              # このフォルダにDB情報が出力されます
├ docker-compose.yml
└ Dockerfile
```

- .tbls.yml
```
# Usage : dsn: my://dbuser:dbpass@hostname:3306/dbname
dsn: my://dbuser:dbpass@hostname:3306/dbname
```

- docker-compose.yml
```
version: '3'
services:
  tbls:
    build: .
    volumes:
      - ./conf:/go/conf
      - ./output:/go/conf/dbdoc
```

- Dockerfile
```
FROM golang:1.12
RUN go get github.com/k1LoW/tbls && \
    apt-get update && \
    apt-get install -y graphviz && \
    mkdir /go/conf /go/conf/dbdoc
WORKDIR /go/conf
CMD ["tbls", "doc"]
```

## 実行手順

1. "./conf/.tbls.yml"に対象DBの接続情報を記述
2. 以下コマンドを実行し、tblsをDokcerで実行する

```
$ docker-compose up -d
```
