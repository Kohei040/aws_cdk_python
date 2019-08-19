# -*- coding: utf-8 -*-
import boto3

file = 'vpc.md'
client = boto3.client('ec2')

vpc_ids, vpc_cider_blocks, vpc_names = [], [], []


def main():
    """
    """
    with open(file, 'w', encoding='utf-8') as f:
        f.write('## VPC')

    vpc_ids, vpc_names = get_vpc()
    subnet_output(vpc_ids, vpc_names)
    route_table_output(vpc_ids, vpc_names)
    natgateway_output()


def get_vpc():
    """
    VPCの設定情報を取得し、MarkdownのTable形式へ変換して"vpc.md"に出力する。

    Returns
    ------
    vpc_ids: list
        VPC IDのリスト。
    vpc_names: list
        VPC名のリスト。
    """

    vpc_list = client.describe_vpcs()['Vpcs']
    for i, vpc in enumerate(vpc_list):
        vpc_ids.append(vpc['VpcId'])
        vpc_cider_blocks.append(vpc['CidrBlock'])
        vpc_names.append(vpc_check_tag_name(vpc, vpc_ids[i]))

    for name, id, cider_blocks in zip(vpc_names, vpc_ids, vpc_cider_blocks):
        with open(file, 'a', encoding='utf-8') as f:
            f.write('\n\n| Name | VPC ID | IPv4 CIDR |'
                    '\n|:--|:--|:--|'
                    f'\n|{name}|{id}|{cider_blocks}|')

    return vpc_ids, vpc_names


def vpc_check_tag_name(vpc, id):
    """
    VPCのTagにNameが付与されているかを峻別。

    Paramters
    ------
    vpc: str
        VPCの名前。
    id: str
        VPCのID。

    Returns
    ------
    tag_name: str
        TagのNameに付与されている値。
    """

    try:
        tag_name = [i['Value'] for i in vpc['Tags'] if i['Key'] == 'Name'][0]
    except KeyError:
        vpc_default = vpc['IsDefault']
        tag_name = '(DefaultVPC)' if vpc_default else ' '

    return tag_name


def subnet_output(vpc_ids, vpc_names):
    """
    VPC毎にSubnetの設定情報を取得し、MarkdownのTable形式へ変換して"vpc.md"に出力する。

    Paramters
    ------
    vpc_ids: list
        VPC IDのリスト。
    vpc_names: list
        VPC名のリスト。
    """

    with open(file, 'a', encoding='utf-8') as f:
        f.write('\n\n## Subnet')
    # Subnetの一覧を取得
    for i, vpc_id in enumerate(vpc_ids):
        with open(file, 'a', encoding='utf-8') as f:
            f.write(f'\n\n#### {vpc_names[i]} ({vpc_id})'
                    '\n\n| Name | Subnet ID | IPv4 CIDR | AZ |'
                    '\n|:--|:--|:--|:--|'
                    )
            vpc_subnet_list = client.describe_subnets(
                Filters=[
                    {
                        'Name': 'vpc-id',
                        'Values': [
                            vpc_id,
                        ]
                    },
                ],
            )['Subnets']
            # Subnet毎に情報を抜き出す
            for i, subnet in enumerate(vpc_subnet_list):
                subnet_id = subnet['SubnetId']
                subnet_az = subnet['AvailabilityZone']
                subnet_cider = subnet['CidrBlock']
                try:
                    subnet_name = [i['Value'] for i in subnet['Tags']
                                   if i['Key'] == 'Name'][0]
                except KeyError:
                    subnet_name = ' '
                # Subnet情報をファイルに記述
                f.write(f'\n| {subnet_name} | {subnet_id} | '
                        f'{subnet_cider} | {subnet_az} |')

    return 0


def route_table_output(vpc_ids, vpc_names):
    """
    VPC毎にRoute Tableの設定情報を取得し、MarkdownのTable形式へ変換して"vpc.md"に出力する。

    Paramters
    ------
    vpc_ids: list
        VPC IDのリスト。
    vpc_names: list
        VPC名のリスト。
    """
    with open(file, 'a', encoding='utf-8') as f:
        f.write('\n\n## Route Table')
    # RouteTableの一覧を取得
    for i, vpc_id in enumerate(vpc_ids):
        with open(file, 'a', encoding='utf-8') as f:
            f.write(f'\n\n#### {vpc_names[i]} ({vpc_id})'
                    '\n\n| Name | RouteTable ID | Subnet Associations | '
                    'Destination | Target |'
                    '\n|:--|:--|:--|:--|:--|')
            route_table_list = client.describe_route_tables(
                Filters=[
                    {
                        'Name': 'vpc-id',
                        'Values': [
                            vpc_id,
                        ]
                    },
                ],
            )['RouteTables']
            # 各RouteTableの情報を抜き出す
            for i, route_table in enumerate(route_table_list):
                route_table_id = route_table['RouteTableId']
                subnet_associations = route_table['Associations']
                subnet_ids = [d.get('SubnetId') for d in subnet_associations]
                subnet_id = '<br>'.join(map(str, subnet_ids))
                route_table_routes = route_table['Routes']
                destinations, targets = [], []
                for i, routes in enumerate(route_table_routes):
                    destinations.append(list(routes.values())[0])
                    targets.append(list(routes.values())[1])
                destination = '<br>'.join(map(str, destinations))
                target = '<br>'.join(map(str, targets))
                try:
                    route_table_name = [i['Value'] for i in route_table['Tags']
                                        if i['Key'] == 'Name'][0]
                except Exception as e:
                    route_table_name = ' '
                # RouteTable情報をファイルに記述
                f.write(f'\n| {route_table_name} | {route_table_id} | '
                        f'{subnet_id} | {destination} | {target} |')

    return 0


def natgateway_output():
    """
    NAT Gatewayの設定情報を取得し、MarkdownのTable形式へ変換して"vpc.md"に出力する。
    """

    with open(file, 'a', encoding='utf-8') as f:
        f.write('\n\n## NAT Gateway'
                '\n\n| Name | NatGatewayId | PublicIp | VPC | Subnet |'
                '\n|:--|:--|:--|:--|:--|'
                )
        nat_gateways = client.describe_nat_gateways()['NatGateways']
        for i, ngw in enumerate(nat_gateways):
            ngw_id = ngw['NatGatewayId']
            ngw_pub_ip = ngw['NatGatewayAddresses'][0]['PublicIp']
            ngw_vpc = ngw['VpcId']
            ngw_subnet = ngw['SubnetId']
            try:
                ngw_name = [i['Value'] for i in ngw['Tags']
                            if i['Key'] == 'Name'][0]
            except Exception as e:
                ngw_name = ' '
            f.write(f'\n| {ngw_name} | {ngw_id} | {ngw_pub_ip} | '
                    '{ngw_vpc} | {ngw_subnet} |')

    return 0


if __name__ == '__main__':
    main()
