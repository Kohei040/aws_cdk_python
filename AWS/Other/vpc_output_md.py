# -*- coding: utf-8 -*-
import boto3

client = boto3.client('ec2')
vpc_list = client.describe_vpcs()['Vpcs']

def output_vpc():
    with open('vpc.md', 'w', encoding='utf-8') as f:
        f.write('| Name | VPC ID | IPv4 CIDR |\n|:--|:--|:--|')

        for vpc in vpc_list:
            vpc_id = vpc['VpcId']
            cider_block = vpc['CidrBlock']
            vpc_name = check_tag_name(vpc, vpc_id)
            f.write('\n|' + vpc_name + '|' + vpc_id + '|' + cider_block + '|')

    with open('vpc.md', 'r') as f:
        vpc_md = f.read()

    return  print(vpc_md)

def check_tag_name(vpc, vpc_id):
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

if __name__ == '__main__':
    output_vpc()
