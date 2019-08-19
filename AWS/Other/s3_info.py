# -*- coding: utf-8 -*-
import boto3
import json

file = 's3.md'
client = boto3.client('s3')


def main():
    """
    S3 Bucketの一覧を取得し、各情報を取得する為の関数を呼び出す。
    """

    with open(file, 'w', encoding='utf-8') as f:
        f.write('# S3')

    buckets = client.list_buckets()['Buckets']
    for bucket in buckets:
        bucket_name = bucket['Name']
        with open(file, 'a', encoding='utf-8') as f:
            f.write(f'\n\n## {bucket_name}')
        bucket_properties(bucket_name)
        bucket_policy(bucket_name)
        bucket_lifecycle(bucket_name)

    return 0


def bucket_properties(bucket_name):
    """
    Bucketのプロパティ情報を取得し、's3.md'に出力する。

    Parameters
    ------
    bucket_name: str
        S3 Bucketの名前。
    """

    # BucketのRegion取得
    region = client.get_bucket_location(
        Bucket=bucket_name
    )['LocationConstraint']

    # Versioning設定取得
    try:
        versioning = client.get_bucket_versioning(
            Bucket=bucket_name
        )['Status']
    except KeyError:
        versioning = 'Disabled'

    # Server Access Log設定取得
    try:
        logging_enabled = client.get_bucket_logging(
            Bucket=bucket_name
        )['LoggingEnabled']
        target_bucket = logging_enabled['TargetBucket']
        target_prefix = logging_enabled['TargetPrefix']
        logging = f'{target_bucket}/{target_prefix}'
    except KeyError:
        logging = 'Disabled'

    # Static WebSite hosing設定取得
    try:
        website_rule = client.get_bucket_website(
            Bucket=bucket_name
        )
        website = 'Enabled'
    except Exception:
        website = 'Disabled'

    # Default Envryption設定取得
    try:
        encryption = client.get_bucket_encryption(
            Bucket=bucket_name
        )['ServerSideEncryptionConfiguration']['Rules'][0] \
        ['ApplyServerSideEncryptionByDefault']['SSEAlgorithm']
    except Exception:
        encryption = 'Disabled'

    with open(file, 'a', encoding='utf-8') as f:
        f.write('\n\n#### Properties'
                '\n\n| Key | Value |'
                '\n|:--|:--|'
                f'\n| Region | {region} |'
                f'\n| Versioning | {versioning} |'
                f'\n| Server Access Log | {logging} |'
                f'\n| Static WebSite hosting | {website} |'
                f'\n| Default Encryption | {encryption} |')

    return 0


def bucket_policy(bucket_name):
    """
    Bucket Policyを取得・整形し、's3.md'に出力する。

    Parameters
    ------
    bucket_name: str
        S3 Bucketの名前。
    """

    try:
        policy_json = client.get_bucket_policy(
            Bucket=bucket_name
        )['Policy']
        policy_load = json.loads(policy_json)
        policy = json.dumps(policy_load, indent=4)
    except Exception:
        policy = 'None'

    with open(file, 'a', encoding='utf-8') as f:
        f.write('\n\n#### Bucket Policy'
                f'\n\n```\n{policy}\n```')

    return 0


def bucket_lifecycle(bucket_name):
    """
    LofeCycleの設定を取得し、's3.md'に出力する。

    Parameters
    ------
    bucket_name: str
        S3 Bucketの名前。
    """

    with open(file, 'a', encoding='utf-8') as f:
        f.write('\n\n#### Lifecycle')

    try:
        lifecycles = client.get_bucket_lifecycle_configuration(
            Bucket=bucket_name
        )['Rules']
        for lifecycle in lifecycles:
            rule_id = lifecycle['ID']
            status = lifecycle['Status']
            prefix = lifecycle['Filter']['Prefix']
            try:
                expired = lifecycle['Expiration']['Days']
                action = f'\n| Delete Expiration | {expired} |'
            except KeyError:
                transitions = lifecycle['Transitions']
                days = [i['Days'] for i in transitions]
                day = '<br>'.join(map(str, days))
                storages = [i['StorageClass'] for i in transitions]
                storage = '<br>'.join(map(str, storages))
                action = f'\n| Transition Day | {day} |' \
                         + f'\n| Storage Class | {storage} |'

            with open(file, 'a', encoding='utf-8') as f:
                f.write('\n\n| Key | Value |'
                        '\n|:--|:--|'
                        f'\n| Rule | {rule_id} |'
                        f'\n| Status | {status} |'
                        f'\n| Prefix | {prefix} |'
                        f'{action}')

    except Exception:
        with open(file, 'a', encoding='utf-8') as f:
            f.write('\n\nNone')

    return 0


if __name__ == '__main__':
    main()
