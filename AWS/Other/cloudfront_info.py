# -*- coding: utf-8 -*-
import boto3

file = 'cloudfront.md'
client = boto3.client('cloudfront')


def main():
    """
    CloudFrontのDistribution IDを取得し、
    Distribution毎に設定情報を取得する為の関数を呼び出す。
    """

    with open(file, 'w', encoding='utf-8') as f:
        f.write('# CloudFront')

    distributions = client.list_distributions()['DistributionList']['Items']

    for distribution in distributions:
        id = distribution['Id']
        details_distribution(id)

    return 0


def details_distribution(id):
    """
    各Distributionの設定を整理し、Markdown形式へ変換して"cloudfront.md"に出力する。

    Parameters
    ------
    id: int
        DistributionのID。
    """

    distribution = client.get_distribution(
        Id=id
    )['Distribution']

    # General Settings
    status = distribution['Status']
    arn = distribution['ARN']
    domain_name = distribution['DomainName']
    try:
        alias_cnames = [i['CNAME'] for i in distribution['AliasICPRecordals']]
        cnames = '<br>'.join(map(str, alias_cnames))
    except KeyError:
        cnames = ' '
    dist_config = distribution['DistributionConfig']
    comment = dist_config['Comment']
    web_acl = dist_config['WebACLId']
    http_version = dist_config['HttpVersion']
    ipv6 = dist_config['IsIPV6Enabled']
    price_class = dist_config['PriceClass']
    state = "Enabled" if dist_config['Enabled'] else "Disabled"
    certificate_resource = dist_config['ViewerCertificate']['CertificateSource']
    if certificate_resource == 'cloudfront':
        ssl = 'Default (*.cloudfront.net)'
    else:
        acm_arn = dist_config['ViewerCertificate']['ACMCertificateArn']
        ssl = f'ACM: {acm_arn}'
    logging_enabled = dist_config['Logging']['Enabled']
    logging_cookie = dist_config['Logging']['IncludeCookies']
    logging_bucket = dist_config['Logging']['Bucket']
    logging_prefix = dist_config['Logging']['Prefix']

    with open(file, 'a', encoding='utf-8') as f:
        f.write(f'\n\n## {id}'
                '\n\n#### General Settings'
                '\n\n| Key | Value |'
                '\n|:--|:--|'
                f'\n| Status | {status} |'
                f'\n| Distribution State | {state} |'
                f'\n| ARN | {arn} |'
                f'\n| Domain Name | {domain_name} |'
                f'\n| Alternate Domain Names (CNAMEs) | {cnames} |'
                f'\n| Comment | {comment} |'
                f'\n| HTTP Version | {http_version} |'
                f'\n| Web ACL | {web_acl} |'
                f'\n| Price Class | {price_class} |'
                f'\n| SSL | {ssl} |'
                f'\n| Logging | {logging_enabled}  |'
                f'\n| Logging Include Cookies | {logging_cookie} |'
                f'\n| Logging Bucket | {logging_bucket}/{logging_prefix} |'
                f'\n| IPv6 | {ipv6} |')

    # Origin Settings
    for origin in dist_config['Origins']['Items']:
        origin_id = origin['Id']
        origin_domain = origin['DomainName']
        origin_path = origin['OriginPath']

        with open(file, 'a', encoding='utf-8') as f:
            f.write('\n\n#### Origin Settings'
                    '\n\n| Key | Value |'
                    '\n|:--|:--|'
                    f'\n| Origin Id | {origin_id} |'
                    f'\n| Origin Name | {origin_domain} |'
                    f'\n| Origin Path | {origin_path} |')

    # Default Behavior
    default_behavior = dist_config['DefaultCacheBehavior']
    target_orgin = default_behavior['TargetOriginId']
    if default_behavior['ViewerProtocolPolicy'] == 'allow-all':
        protocol = 'HTTP or HTTPS'
    else:
        protocol = default_behavior['ViewerProtocolPolicy']
    allow_methods = [i for i in default_behavior['AllowedMethods']['Items']]
    allow_method = ', '.join(map(str, allow_methods))
    default_ttl = default_behavior['DefaultTTL']
    min_ttl = default_behavior['MinTTL']
    max_ttl = default_behavior['MaxTTL']
    restrict_access = default_behavior['TrustedSigners']['Enabled']

    with open(file, 'a', encoding='utf-8') as f:
        f.write('\n\n#### Default Behavior'
                '\n\n| Key | Value |'
                '\n|:--|:--|'
                f'\n| Target Otigin | {target_orgin} |'
                f'\n| Protocol Policy | {protocol} |'
                f'\n| Allow Methods | {allow_method} |'
                f'\n| Default TTL | {default_ttl} |'
                f'\n| MinTTL | {min_ttl} |'
                f'\n| MaxTTL | {max_ttl} |'
                f'\n| Use Signed URLs orSigned Cookies | {restrict_access} |')


if __name__ == '__main__':
    main()
