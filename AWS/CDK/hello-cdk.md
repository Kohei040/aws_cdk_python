# AWS CDK(Python)でHello World

#### チュートリアル手順

- 作業用の空ディレクトリ作成

```
$ mkdir hello-cdk
$ cd ./hello-cdk
```

- アプリの初期化

```
$ cdk init --language python
Applying project template app for python
Executing Creating virtualenv...

# Welcome to your CDK Python project!

This is a blank project for Python development with CDK.

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project.  The initialization
process also creates a virtualenv within this project, stored under the .env
directory.  To create the virtualenv it assumes that there is a `python3`
(or `python` for Windows) executable in your path with access to the `venv`
package. If for any reason the automatic creation of the virtualenv fails,
you can create the virtualenv manually.

~~~ Omitted ~~~

# Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!
```

- init後にvierualenvが実行されていない場合は以下を実行

```
(Mac/Linux)
$ python3 -m venv .env
$ source .env/bin/activate

(Windows)
$ .env\Scripts\activate.bat
```

- 必要な依存関係をインストール

```
$ pip install -r requirements.txt --user
```

- "app.py"を以下に変更

```
Before: HelloCdkStack(app, "hello-cdk-cdk-1")
After : HelloCdkStack(app, "HelloCdkStack")
```

- スタックの一覧を表示

```
$ cdk ls
HelloCdkStack
```

- S3バケットを追加する

```
$ pip install aws-cdk.aws-s3 --user
```

- "hello_cdk_stack.py"の内容を以下に変更
  - "MyFirstBucket"はS3の物理名ではなく、論理IDとなります
  - "aws_s3.Bucket"の使い方の詳細は[こちら](https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_s3/Bucket.html)を参照

```
from aws_cdk import core
from aws_cdk import (
    aws_s3 as s3,
    cdk
)

class HelloCdkStack(core.Stack):

    def __init__(self, app: core.App, id: str, **kwargs) -> None:
        super().__init__(app, id)

        # The code that defines your stack goes here
        bucket = s3.Bucket(self,
            "MyFirstBucket",
            versioned=True,)
```

- CloudFormation Templateに統合

```
$ cdk synth
Resources:
  MyFirstBucketB8884501:
    Type: AWS::S3::Bucket
    Properties:
      VersioningConfiguration:
        Status: Enabled
    DeletionPolicy: Retain
    Metadata:
      aws:cdk:path: HelloCdkStack/MyFirstBucket/Resource
  CDKMetadata:

    Type: AWS::CDK::Metadata
    Properties:
      Modules: aws-cdk=0.37.0,@aws-cdk/aws-events=0.37.0,@aws-cdk/aws-iam=0.37.0,@aws-cdk/aws-kms=0.37.0,@aws-cdk/aws-s3=0.37.0,@aws-cdk/core=0.37.0,@aws-cdk/cx-api=0.37.0,@aws-cdk/region-info=0.37.0,jsii-runtime=
Python/3.7.3
```

- スタックの配置

```
$ cdk deploy
HelloCdkStack: deploying...
HelloCdkStack: creating CloudFormation changeset...
 0/3 | 17:27:15 | CREATE_IN_PROGRESS   | AWS::CDK::Metadata | CDKMetadata
 0/3 | 17:27:15 | CREATE_IN_PROGRESS   | AWS::S3::Bucket    | MyFirstBucket (MyFirstBucketB8884501)
 0/3 | 17:27:16 | CREATE_IN_PROGRESS   | AWS::S3::Bucket    | MyFirstBucket (MyFirstBucketB8884501) Resource creation Initiated
 0/3 | 17:27:18 | CREATE_IN_PROGRESS   | AWS::CDK::Metadata | CDKMetadata Resource creation Initiated
 1/3 | 17:27:18 | CREATE_COMPLETE      | AWS::CDK::Metadata | CDKMetadata
 2/3 | 17:27:37 | CREATE_COMPLETE      | AWS::S3::Bucket    | MyFirstBucket (MyFirstBucketB8884501)
 3/3 | 17:27:38 | CREATE_COMPLETE      | AWS::CloudFormation::Stack | HelloCdkStack


 ✅  HelloCdkStack

Stack ARN:
arn:aws:cloudformation:us-east-1:<AccountID>:stack/HelloCdkStack/2afdb770-a15a-11e9-b3c3-12f2c8f206e2
```
