# -*- coding: utf-8 -*-
import boto3

file = 'network.md'
client = boto3.client('ec2')

vpc_list = client.describe_vpcs()['Vpcs']
vpc_ids, vpc_cider_blocks, vpc_names= [], [], []

def main():
    get_vpc()
    vpc_output()
    subnet_output()
    route_table_output()
    with open(file, 'r') as f:
        print(f.read())

def get_vpc():
    for i, vpc in enumerate(vpc_list):
        vpc_ids.append(vpc['VpcId'])
        vpc_cider_blocks.append(vpc['CidrBlock'])
        vpc_names.append(vpc_check_tag_name(vpc, vpc_ids[i]))
    return 0

def vpc_output():
    with open(file, 'w', encoding='utf-8') as f:
        f.write('## VPC\n\n| Name | VPC ID | IPv4 CIDR |\n|:--|:--|:--|')
        for i, vpc_id in enumerate(vpc_ids):
            f.write('\n|' + vpc_names[i] + '|' + vpc_id + '|' + vpc_cider_blocks[i] + '|')
    return 0

def vpc_check_tag_name(vpc, id):
    try:
        tag_name = vpc['Tags'][0]['Value']
        return tag_name
    except KeyError:
        vpc_default = vpc['IsDefault']
        if vpc_default:
            tag_name = '(DefaultVPC)'
            return tag_name
        else:
            tag_name = ' '
            return tag_name

def subnet_output():
    with open(file, 'a') as f:
        f.write('\n\n## Subnet')
    for i, vpc_id in enumerate(vpc_ids):
        with open(file, 'a') as f:
            f.write('\n\n#### ' + vpc_names[i] + '(' + vpc_id + ')')
            f.write('\n\n| Name | Subnet ID | IPv4 CIDR | AZ |\n|:--|:--|:--|:--|')
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
            for i, subnet in enumerate(vpc_subnet_list):
                subnet_id = subnet['SubnetId']
                subnet_az = subnet['AvailabilityZone']
                subnet_cider = subnet['CidrBlock']
                try:
                    subnet_name = subnet['Tags'][0]['Value']
                except KeyError:
                    subnet_name = ' '
                f.write('\n|' + subnet_name + '|' + subnet_id + '|' + subnet_cider + '|' + subnet_az + '|')
    return 0

def route_table_output():
    with open(file, 'a') as f:\
        f.write('\n\n## Route Table')
    for i, vpc_id in enumerate(vpc_ids):
        with open(file, 'a') as f:
            f.write('\n\n#### ' + vpc_names[i] + '(' + vpc_id + ')')
            f.write('\n\n| Name | RouteTable ID | Subnet Associations | Destination | Target |\n|:--|:--|:--|:--|:--|')
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
            for i, route_table in enumerate(route_table_list):
                route_table_id = route_table['RouteTableId']
                print(route_table_id)
                subnet_associations = []
                subnet_associations.append(route_table['Associations'])
                print(subnet_associations)
                try:
                    route_table_name = route_table['Tags'][0]['Value']
                except KeyError:
                    route_table_name = ' '
                print(route_table_name)

if __name__ == '__main__':
    main()
