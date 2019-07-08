# AWS Cloud Development Kit(CDK)

## 事前準備

- node.js(>=8.11.x)
```
$ node --version
v12.4.0
```

- Python(>=3.6)
```
$ python --version
Python 3.7.3
```

- Install the AWS CDK
```
$ npm install -g aws-cdk
$ cdk --version
0.37.0 (build c4bdb54)
$ pip install --upgrade aws-cdk.cdk --user
```

- [Credential及びRegionの設定](https://docs.aws.amazon.com/ja_jp/cdk/latest/guide/getting_started.html#getting_started_credentials)
  - 今回はAWS CLIのCredential情報(~/.aws/config)を利用

## 参考
- [AWS CDK Developer Guide](https://docs.aws.amazon.com/ja_jp/cdk/latest/guide/home.html)
- [AWS CDK Python Reference](https://docs.aws.amazon.com/cdk/api/latest/python/index.html)
