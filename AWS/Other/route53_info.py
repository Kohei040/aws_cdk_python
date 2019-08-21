# -*- coding: utf-8 -*-
import boto3

file = 'route53.md'
client = boto3.client('route53')


def main():
    """
    Route53で取得したDomainの設定を整理し、出力する。
    またHostedZone, Recordの設定を整理し、出力する。
    """

    with open(file, 'w', encoding='utf-8') as f:
        f.write('# Route53'
                '\n\n## Domain'
                '\n\n| Name | Auto Renew | Expiry Date |'
                '\n|:--|:--|:--|')

    # Route53で取得したDomain
    domains = [i for i in
               boto3.client('route53domains',
                            region_name='us-east-1').list_domains()['Domains']]
    for domain in domains:
        describe_domain(domain)

    # HostedZonesの設定を出力
    hosted_zones = [i for i in client.list_hosted_zones()['HostedZones']]
    with open(file, 'a', encoding='utf-8') as f:
        f.write('\n\n## Hosted Zone')
    for hosted_zone in hosted_zones:
        hosted_zone_id = hosted_zone['Id']
        domain_name = hosted_zone['Name']
        hosted_zone_type = hosted_zone['Config']['PrivateZone']

        with open(file, 'a', encoding='utf-8') as f:
            f.write('\n\n| DomainName | Type | Hosted Zone ID |'
                    f'\n|:--|:--|:--|'
                    f'\n|{domain_name}|{hosted_zone_type}|{hosted_zone_id}|'
                    '\n\n| Name | Type | Value | TTL |'
                    '\n|:--|:--|:--|:--|')
        # 各Recordの設定を出力
        describe_records(hosted_zone_id)


def describe_domain(domain):
    """
    Route53で取得したDomain設定をMarkdown形式へ変換して'route53.md'に出力する。

    Parameters
    ------
    domain: str
        Route53で取得したDomain名。
    """

    domain_name = domain['DomainName']
    auto_renew = domain['AutoRenew']
    expiry = domain['Expiry']

    with open(file, 'a', encoding='utf-8') as f:
        f.write(f'\n|{domain_name}|{auto_renew}|{expiry}|')

    return 0


def describe_records(hosted_zone_id):
    """
    HostedZoneのRecord設定を取得し、Markdown形式へ変換して'route53.md'に出力する。

    Parameters
    ------
    hosted_zone_id: int
        HostedZoneのID。
    """

    list_records = client.list_resource_record_sets(
        HostedZoneId=hosted_zone_id
    )['ResourceRecordSets']

    for record in list_records:
        name = record['Name']
        type = record['Type']
        try:
            values = [i['Value'] for i in record['ResourceRecords']]
        except KeyError:
            values = [i for i in record['AliasTarget']['DNSName']]
        value = '<br>'.join(map(str, values))
        try:
            ttl = record['TTL']
        except KeyError:
            ttl = ' '

        with open(file, 'a', encoding='utf-8') as f:
            f.write(f'\n|{name}|{type}|{value}|{ttl}|')

    return 0


if __name__ == '__main__':
    main()
