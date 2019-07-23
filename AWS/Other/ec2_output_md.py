# -*- coding: utf-8 -*-
import boto3
import network_output_md as vpc

file = 'ec2.md'
client = boto3.client('ec2')

vpc_ids, vpc_names = vpc.get_vpc()

def main():
    ec2_output()
    # with open(file, 'r') as f:
    #     print(f.read())


def ec2_output():
    with open(file, 'w', encoding='utf-8') as f:
        f.write('')

if __name__ == '__main__':
    main()
