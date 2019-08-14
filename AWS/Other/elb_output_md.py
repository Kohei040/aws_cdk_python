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
    zones = [i['SubnetId'] + ' (' + i['ZoneName'] + ')'
             for i in elb['AvailabilityZones']]
    zone = '<br>'.join(map(str, zones))
    elb_sg_ids = [i for i in elb['SecurityGroups']]
    elb_sg = '<br>'.join(map(str, elb_sg_ids))
    address_type = elb['IpAddressType']
    with open(file, 'a', encoding='utf-8') as f:
        f.write(f'\n\n## {elb_name}'
                '\n\n#### Description'
                '\n\n| Key | Value |'
                '\n|:--|:--|'
                f'\n| DNS | {dns} |'
                f'\n| Scheme | {scheme} |'
                f'\n| Type | {elb_type} |'
                f'\n| VPC | {vpc} |'
                f'\n| AvailabilityZone | {zone} |'
                f'\n| SecurityGroup | {elb_sg} |'
                f'\n| IP Address Type | {address_type} |'
                )
    return elb_arn


def describe_attribute(elb_arn):
    elb_attribute = client.describe_load_balancer_attributes(
        LoadBalancerArn=elb_arn
    )['Attributes']
    access_log = [i['Value'] for i in elb_attribute
                  if i['Key'] == 'access_logs.s3.enabled'][0]
    access_log_bucket = [i['Value'] for i in elb_attribute
                         if i['Key'] == 'access_logs.s3.bucket'][0]
    access_log_prefix = [i['Value'] for i in elb_attribute
                         if i['Key'] == 'access_logs.s3.prefix'][0]
    if access_log == 'true':
        access_log_location = f'{access_log_bucket}/{access_log_prefix}'
    else:
        access_log_location = ' '
    idle_timeout = [i['Value'] for i in elb_attribute
                    if i['Key'] == 'idle_timeout.timeout_seconds'][0]
    http2 = [i['Value'] for i in elb_attribute
             if i['Key'] == 'routing.http2.enabled'][0]
    protection = [i['Value'] for i in elb_attribute
                  if i['Key'] == 'deletion_protection.enabled'][0]
    with open(file, 'a', encoding='utf-8') as f:
        f.write(f'\n| Deletion Protection | {protection} |'
                f'\n| Access Logs | {access_log} |'
                f'\n| Access Logs Location | {access_log_location} |'
                f'\n| Idle Timeout | {idle_timeout} |'
                f'\n| HTTP2/ | {http2} |'
                )
    return 0


def describe_listener(elb_arn):
    elb_listeners = client.describe_listeners(
        LoadBalancerArn=elb_arn,
    )['Listeners']
    protocol = [i['Protocol'] for i in elb_listeners]
    listen_port = [i['Port'] for i in elb_listeners]
    action_type = [i['DefaultActions'][0]['Type'] for i in elb_listeners]
    target_group_arn = [i['DefaultActions'][0]['TargetGroupArn']
                        for i in elb_listeners]
    with open(file, 'a', encoding='utf-8') as f:
        f.write('\n\n##### Listeners')
    for i, elb in enumerate(elb_listeners):
        with open(file, 'a', encoding='utf-8') as f:
            f.write('\n\n| Key | Value |'
                    '\n|:--|:--|'
                    f'\n| Protocol | {protocol[i]} |'
                    f'\n| Port | {listen_port[i]} |'
                    f'\n| Type | {action_type[i]} |'
                    f'\n| Target Group | {target_group_arn[i]} |'
                    )
    return 0


def describe_target_group(elb_arn):
    target_groups = client.describe_target_groups(
        LoadBalancerArn=elb_arn,
    )['TargetGroups']
    with open(file, 'a', encoding='utf-8') as f:
        f.write('\n\n#### Target Group')
    for target_group in target_groups:
        target_group_name = target_group['TargetGroupName']
        target_group_arn = target_group['TargetGroupArn']
        target_group_protocol = target_group['Protocol']
        target_group_port = target_group['Port']
        target_group_type = target_group['TargetType']
        target_group_target = describe_health_check(target_group_arn)
        health_check_protocol = target_group['HealthCheckProtocol']
        health_check_port = target_group['HealthCheckPort']
        health_check_path = target_group['HealthCheckPath']
        health_check_interval = target_group['HealthCheckIntervalSeconds']
        health_check_timeout = target_group['HealthCheckTimeoutSeconds']
        with open(file, 'a', encoding='utf-8') as f:
            f.write('\n\n| Key | Value |'
                    '\n|:--|:--|'
                    f'\n| Name | {target_group_name} |'
                    f'\n| ARN | {target_group_arn} |'
                    f'\n| Protocol | {target_group_protocol} |'
                    f'\n| Port | {target_group_port} |'
                    f'\n| Target Type | {target_group_type} |'
                    f'\n| Target | {target_group_target} |'
                    f'\n| HealthCheck Protocol | {health_check_protocol} |'
                    f'\n| HealthCheck Port | {health_check_port} |'
                    f'\n| HealthCheck Path | {health_check_path} |'
                    f'\n| HealthCheck Interval | {health_check_interval} |'
                    f'\n| HealthCheck Timeout | {health_check_timeout}|'
                    )
    return 0


def describe_health_check(target_group_arn):
    target_health_checks = client.describe_target_health(
        TargetGroupArn=target_group_arn,
    )['TargetHealthDescriptions']
    target_ids = [i['Target']['Id'] for i in target_health_checks]
    target_states = [i['TargetHealth']['State'] for i in target_health_checks]
    targets = [f'{target_id} ({target_states[i]})'
               for i, target_id in enumerate(target_ids)]
    target_group_target = '<br>'.join(map(str, targets))
    return target_group_target


if __name__ == '__main__':
    main()
