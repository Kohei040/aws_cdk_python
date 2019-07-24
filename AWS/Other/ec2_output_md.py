# -*- coding: utf-8 -*-
import boto3
import network_output_md as vpc

file = 'ec2.md'
client = boto3.client('ec2')

vpc_ids, vpc_names = vpc.get_vpc()

def main():
    ec2_output()
    with open(file, 'r') as f:
        print(f.read())

def ec2_output():
    with open(file, 'w', encoding='utf-8') as f:
        f.write('## EC2')
    for i, vpc_id in enumerate(vpc_ids):
        with open(file, 'a', encoding='utf-8') as f:
            f.write(f'\n\n#### {vpc_names[i]} ({vpc_id})')
        ec2_describe(vpc_id)
    return 0

def ec2_describe(vpc_id):
    get_instances = client.describe_instances(
        Filters=[
            {
                'Name': 'network-interface.vpc-id',
                'Values': [
                    vpc_id,
                ]
            },
        ],
    )['Reservations']
    for instances in get_instances:
        instance = instances['Instances'][0]
        try:
            name = [i['Value'] for i in instance['Tags'] if i['Key'] == 'Name'][0]
        except:
            name = ' '
        id = instance['InstanceId']
        type = instance['InstanceType']
        try:
            pub_ip = instance['PublicIpAddress']
        except:
            pub_ip = '-'
        pri_ip = instance['PrivateIpAddress']
        status = instance['State']['Name']
        ami_id = instance['ImageId']
        subnet = instance['SubnetId']
        az = instance['Placement']['AvailabilityZone']
        sg_names, sg_ids = [], []
        for i, sg in enumerate(instance['NetworkInterfaces'][0]['Groups']):
            sg_names.append(sg['GroupName'])
            sg_ids.append(sg['GroupId'])
        sg_name = '<br>'.join(map(str, sg_names))
        sg_id = '<br>'.join(map(str, sg_ids))
        try:
            key_name = instance['KeyName']
        except:
            key_name = '-'
        try:
            role = instance['IamInstanceProfile']['Arn']
        except:
            role = '-'
        with open(file, 'a', encoding='utf-8') as f:
            f.write('\n\n| Name | ID | Type | PublicIP | PrivateIP | Status |' \
                    '\n|:--|:--|:--|:--|:--|:--|' \
                    f'\n| {name} | {id} | {type} | {pub_ip} | {pri_ip} | {status} |' \
                    f'\n| **AMI ID** | {ami_id} | **SubnetID** | {subnet} | **AZ** | {az} |' \
                    f'\n| **KeyPair** | {key_name} | **IAM Role** | {role} |||' \
                    f'\n| **SecurityGroup** | {sg_name} | {sg_id} ||||')
    return 0


if __name__ == '__main__':
    main()
