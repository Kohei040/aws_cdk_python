# -*- coding: utf-8 -*-
import boto3
import network_output_md as vpc

file = 'elb.md'
client = boto3.client('elbv2')

def main():
    with open(file, 'w', encoding='utf-8') as f:
        f.write('# ELB')
    get_elbs = client.describe_load_balancers()['LoadBalancers']
    for elb in get_elbs:
        elb_arn = elb_describe(elb)
        describe_attribute(elb_arn)
        describe_listener(elb_arn)
        describe_target_group(elb_arn)

    # 生成結果を出力
    with open(file, 'r', encoding='utf-8') as f:
        print(f.read())

def elb_describe(elb):
    elb_arn = elb['LoadBalancerArn']
    elb_name = elb['LoadBalancerName']
    dns = elb['DNSName']
    scheme = elb['Scheme']
    elb_type = elb['Type']
    vpc = elb['VpcId']
    zones = [i['SubnetId'] + ' (' + i['ZoneName'] + ')' \
             for i in elb['AvailabilityZones']]
    zone = '<br>'.join(map(str, zones))
    elb_sg_ids = [i for i in elb['SecurityGroups']]
    elb_sg = '<br>'.join(map(str, elb_sg_ids))
    address_type = elb['IpAddressType']
    with open(file, 'a', encoding='utf-8') as f:
        f.write(f'\n\n## {elb_name}' \
                '\n\n- Description' \
                '\n\n| Name | Value |' \
                '\n|:--|:--|' \
                f'\n| DNS | {dns} |' \
                f'\n| Scheme | {scheme} |' \
                f'\n| Type | {elb_type} |' \
                f'\n| VPC | {vpc} |' \
                f'\n| AvailabilityZone | {zone} |' \
                f'\n| SecurityGroup | {elb_sg} |' \
                f'\n| IP Address Type | {address_type} |'
                )
    return elb_arn

def describe_attribute(elb_arn):
    elb_attribute = client.describe_load_balancer_attributes(
        LoadBalancerArn=elb_arn
    )['Attributes']
    access_log = [i['Value'] for i in elb_attribute \
                  if i['Key'] == 'access_logs.s3.enabled'][0]
    access_log_bucket = [i['Value'] for i in elb_attribute \
                         if i['Key'] == 'access_logs.s3.bucket'][0]
    access_log_prefix = [i['Value'] for i in elb_attribute \
                         if i['Key'] == 'access_logs.s3.prefix'][0]
    if access_log == 'true':
        access_log_location = f'{access_log_bucket}/{access_log_prefix}'
    else:
        access_log_location = '-'
    idle_timeout = [i['Value'] for i in elb_attribute \
                    if i['Key'] == 'idle_timeout.timeout_seconds'][0]
    http2 = [i['Value'] for i in elb_attribute \
             if i['Key'] == 'routing.http2.enabled'][0]
    protection = [i['Value'] for i in elb_attribute \
                  if i['Key'] == 'deletion_protection.enabled'][0]
    with open(file, 'a', encoding='utf-8') as f:
        f.write('\n\n- Attributes' \
                '\n\n| Name | Value |' \
                '\n|:--|:--|' \
                f'\n| Deletion Protection | {protection} |'
                f'\n| Access Logs | {access_log} |' \
                f'\n| Access Logs Location | {access_log_location} |' \
                f'\n| Idle Timeout | {idle_timeout} |' \
                f'\n| HTTP2/ | {http2} |'
                )
    return 0

def describe_listener(elb_arn):
    elb_listeners = client.describe_listeners(
        LoadBalancerArn=elb_arn,
    )['Listeners']
    listen_port = [i['Port'] for i in elb_listeners]
    protocol = [i['Protocol'] for i in elb_listeners]
    action_type = [i['DefaultActions'][0]['Type'] for i in elb_listeners]
    target_group = [i['DefaultActions'][0]['TargetGroupArn'] for i in elb_listeners]
    with open(file, 'a', encoding='utf-8') as f:
        f.write('\n\n- Listeners')
    for i, elb in enumerate(elb_listeners):
        with open(file, 'a', encoding='utf-8') as f:
            f.write('\n\n| Name | Value |' \
                    '\n|:--|:--|' \
                    f'\n| Port | {listen_port[i]} |' \
                    f'\n| Protocol | {protocol[i]} |' \
                    f'\n| Type | {action_type[i]} |' \
                    f'\n| Target Group | {target_group[i]} |'
                    )
    return 0

def describe_target_group(elb_arn, target_group_arn):
    target_groups = client.describe_target_groups(
        LoadBalancerArn=elb_arn,
        TargetGroupArns=[
            target_group_arn,
        ]
    )['TargetGroups']
    print(target_groups)

if __name__ == '__main__':
    main()
