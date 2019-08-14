# -*- coding: utf-8 -*-
import boto3
import network_output_md as vpc

file = 'ec2.md'
client = boto3.client('ec2')

vpc_ids, vpc_names = vpc.get_vpc()

def main():
    ec2_output()
    with open(file, 'r', encoding='utf-8') as f:
        print(f.read())

def ec2_output():
    with open(file, 'w', encoding='utf-8') as f:
        f.write('# EC2')
    for i, vpc_id in enumerate(vpc_ids):
        with open(file, 'a', encoding='utf-8') as f:
            f.write(f'\n\n## {vpc_names[i]} ({vpc_id})')
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
        status = instance['State']['Name']
        try:
            name = [i['Value'] for i in instance['Tags'] if i['Key'] == 'Name'][0]
        except:
            name = ' '
        instance_id = instance['InstanceId']
        instance_type = instance['InstanceType']
        try:
            pub_ip = instance['PublicIpAddress']
        except:
            pub_ip = '\-'
        pri_ip = instance['PrivateIpAddress']
        ami_id = instance['ImageId']
        subnet = instance['SubnetId']
        az = instance['Placement']['AvailabilityZone']
        sg_names, sg_ids = [], []
        for sg in instance['NetworkInterfaces'][0]['Groups']:
            sg_names.append(sg['GroupName'])
            sg_ids.append(sg['GroupId'])
        sg_list = []
        for i, sg_name in enumerate(sg_names):
            sg_list.append(sg_name + ' (' + sg_ids[i] + ')')
        sg = '<br>'.join(map(str, sg_list))
        ebs_ids = []
        for ebs in instance['BlockDeviceMappings']:
            ebs_ids.append(ebs['Ebs']['VolumeId'])
        ebs_list = []
        for ebs_id in ebs_ids:
            describe_ebs = client.describe_volumes(
                VolumeIds = [
                    ebs_id,
                ],
            )['Volumes'][0]
            ebs_type = describe_ebs['VolumeType']
            ebs_size = describe_ebs['Size']
            ebs_list.append(ebs_id + ' (Type: ' + ebs_type + ', Size: ' + str(ebs_size) + 'GiB)')
        ebs = '<br>'.join(map(str, ebs_list))
        try:
            key_name = instance['KeyName']
        except:
            key_name = '\-'
        try:
            role = instance['IamInstanceProfile']['Arn']
        except:
            role = '\-'
        with open(file, 'a', encoding='utf-8') as f:
            f.write(f'\n\n- {name} ({instance_id})' \
                    '\n\n| Name | Value |' \
                    '\n|:--|:--|' \
                    f'\n| Status | {status} |' \
                    f'\n| Type | {instance_type} |' \
                    f'\n| PublicIP | {pub_ip} |' \
                    f'\n| PrivateIP | {pri_ip} |' \
                    f'\n| AMI ID | {ami_id} |' \
                    f'\n| Subnet | {subnet} |' \
                    f'\n| AvailabilityZone | {az} |' \
                    f'\n| SecurityGroup| {sg} |' \
                    f'\n| KeyPair | {key_name} |' \
                    f'\n| IAM Role | {role} |' \
                    f'\n| Volume | {ebs} |')
    return 0


if __name__ == '__main__':
    main()
