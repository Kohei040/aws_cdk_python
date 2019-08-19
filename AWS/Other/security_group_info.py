# -*- coding: utf-8 -*-
import boto3
import vpc_info as vpc

file = 'security_group.md'
client = boto3.client('ec2')

vpc_ids, vpc_names = vpc.get_vpc()


def main():
    with open(file, 'w', encoding='utf-8') as f:
        f.write('# Security Group')
    for vpc_id, vpc_name in zip(vpc_ids, vpc_names):
        with open(file, 'a', encoding='utf-8') as f:
            f.write(f'\n\n## {vpc_name} ({vpc_id})')
        security_groups = client.describe_security_groups(
            Filters=[
                {
                    'Name': 'vpc-id',
                    'Values': [
                        vpc_id,
                    ]
                },
            ],
        )['SecurityGroups']
        for security_group in security_groups:
            describe_security_group(security_group)
    return 0


def describe_security_group(security_group):
    name = security_group['GroupName']
    id = security_group['GroupId']

    with open(file, 'a', encoding='utf-8') as f:
        f.write(f'\n\n##### {name} ({id})')

    inbound_rules = security_group['IpPermissions']
    with open(file, 'a', encoding='utf-8') as f:
        f.write('\n\n- Inbound Rule'
                '\n\n| Protocol | Port | Source | Description |'
                '\n|:--|:--|:--|:--|')
    for rule in inbound_rules:
        detailed_rule(rule)

    outbound_rules = security_group['IpPermissionsEgress']
    with open(file, 'a', encoding='utf-8') as f:
        f.write('\n\n- Outbound Rule'
                '\n\n| Protocol | Port | Destination | Description |'
                '\n|:--|:--|:--|:--|')
    for rule in outbound_rules:
        detailed_rule(rule)

    return 0


def detailed_rule(rule):
    if rule['IpProtocol'] == '-1':
        protocol = 'All'
        port = 'All'
    else:
        protocol = rule['IpProtocol']
        from_port = rule['FromPort']
        to_port = rule['ToPort']
        port = from_port if from_port == to_port else f'{from_port}-{to_port}'

    for ip_range in rule['IpRanges']:
        cidr_ip = ip_range['CidrIp']
        try:
            description = ip_range['Description']
        except KeyError:
            description = ' '
        with open(file, 'a', encoding='utf-8') as f:
            f.write(f'\n| {protocol} | {port} | {cidr_ip} | {description} |')

    for user_id in rule['UserIdGroupPairs']:
        id = user_id['GroupId']
        try:
            description = user_id['Description']
        except KeyError:
            description = ' '
        with open(file, 'a', encoding='utf-8') as f:
            f.write(f'\n| {protocol} | {port} | {id} | {description} |')

    return 0


if __name__ == '__main__':
    main()
