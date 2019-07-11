# -*- coding: utf-8 -*-
import boto3

file = 'network.md'

client = boto3.client('ec2')

vpc_list = client.describe_vpcs()['Vpcs']
vpc_ids, vpc_cider_blocks, vpc_names= [], [], []

def main():
    vpc_contents()
    vpc_main()
    subnet_main()
    with open(file, 'r') as f:
        print(f.read())

def vpc_contents():
    for i, vpc in enumerate(vpc_list):
        vpc_ids.append(vpc['VpcId'])
        vpc_cider_blocks.append(vpc['CidrBlock'])
        vpc_names.append(vpc_check_tag_name(vpc, vpc_ids[i]))
    return 0

def vpc_main():
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

def subnet_main():
    with open(file, 'a') as f:
        f.write('\n\n## Subnet\n\n')
    for i, vpc_id in enumerate(vpc_ids):
        with open(file, 'a') as f:
            f.write('\n\n#### ' + vpc_names[i] + '(' + vpc_id + ')')
            vpc_subnet_list = client.describe_subnets(
                Filters=[
                    {
                        'Name': 'vpc-id',
                        'Values': [
                            vpc_id,
                        ]
                    },
                ],
            )['Subnets'][i]['SubnetId']
            print(vpc_subnet_list)
    return 0

if __name__ == '__main__':
    main()
