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

if __name__ == '__main__':
    main()
