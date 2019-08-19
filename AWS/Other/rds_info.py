# -*- coding: utf-8 -*-
import boto3
import json

file = 'rds.md'
client = boto3.client('rds')


def main():
    """
    RDSインスタンスの設定情報をからAuroraかどうかを判別し、
    AuroraもしくはRDSごとに設定を取得する為の関数を呼び出す。
    """

    all_instances = client.describe_db_instances()['DBInstances']
    # AuroraもしくはRDSかを峻別
    clusters, rds_instances = [], []
    for instance in all_instances:
        try:
            clusters.append(instance['DBClusterIdentifier'])
        except KeyError:
            rds_instances.append(instance['DBInstanceIdentifier'])

    # Aurora Cluster
    with open(file, 'w', encoding='utf-8') as f:
        f.write('# Aurora Cluster')
    for cluster in list(set(clusters)):
        cluster_instances = describe_aurora_cluster(cluster)
        for instance in cluster_instances:
            describe_auroara_instance(instance)

    # RDS for MySQL
    with open(file, 'a', encoding='utf-8') as f:
        f.write('\n\n# RDS for MySQL')
    for instance in rds_instances:
        describe_db_instance(instance)

    return 0


def describe_aurora_cluster(cluster):
    """
    Auroraの設定をMarkdownのTable形式へ変換して"rds.md"に出力する。

    Parameters
    ------
    cluster: str
        Aurora Cluster名前。

    Returns
    ------
    cluster_instances: list
        Aurora Clusterに属するDBインスタンスのリスト。
    """

    describe_clusters = client.describe_db_clusters(
        DBClusterIdentifier=cluster,
    )['DBClusters']
    for i in describe_clusters:
        cluster_parameter_group = i['DBClusterParameterGroup']
        subnet_group = i['DBSubnetGroup']
        cluster_status = i['Status']
        endpoint = i['Endpoint']
        read_endpoint = i['ReaderEndpoint']
        multi_az = i['MultiAZ']
        engine = i['Engine']
        engine_version = i['EngineVersion']
        port = i['Port']
        master_user = i['MasterUsername']
        backup_window = i['PreferredBackupWindow']
        backup_period = i['BackupRetentionPeriod']
        maintenance_window = i['PreferredMaintenanceWindow']
        security_groups = [x['VpcSecurityGroupId']
                           for x in i['VpcSecurityGroups']]
        security_group = '<br>'.join(map(str, security_groups))
        cluster_instances = [x['DBInstanceIdentifier']
                             for x in i['DBClusterMembers']]
        cluster_instance = '<br>'.join(map(str, cluster_instances))
        iam_roles = [x['RoleArn'] for x in i['AssociatedRoles']]
        iam_role = '<br>'.join(map(str, iam_roles))
    with open(file, 'a', encoding='utf-8') as f:
        f.write(f'\n\n## {cluster}'
                '\n\n| Key | Value |'
                '\n|:--|:--|'
                f'\n| Engine | {engine} {engine_version} |'
                f'\n| Satus | {cluster_status} |'
                f'\n| Endpoint | {endpoint} |'
                f'\n| Read Endpoint | {read_endpoint} |'
                f'\n| Master User | {master_user} |'
                f'\n| Port | {port} |'
                f'\n| Cluster Member | {cluster_instance} |'
                f'\n| Security Group | {security_group} |'
                f'\n| MultiAZ| {multi_az} |'
                f'\n| Subnet Group | {subnet_group} |'
                f'\n| Cluster Paramter Group | {cluster_parameter_group} |'
                f'\n| Backup (Period) | {backup_window}({backup_period})|'
                f'\n| Maintenance Window | {maintenance_window} |'
                f'\n| IAM Role | {iam_role} |')

    return cluster_instances


def describe_auroara_instance(instance):
    """
    Aurora配下のDBインスタンス情報をMarkdownのTable形式へ変換して"rds.md"に出力する。

    Paramters
    ------
    instance: str
        DBインスタンスの名前。
    """

    describe_instances = client.describe_db_instances(
        DBInstanceIdentifier=instance,
    )['DBInstances']
    for i in describe_instances:
        instance_type = i['DBInstanceClass']
        az = i['AvailabilityZone']
        db_parameter_groups = [x['DBParameterGroupName']
                               for x in i['DBParameterGroups']]
        db_parameter_group = '<br>'.join(map(str, db_parameter_groups))
        try:
            cloudwatch_logs = [x for x in i['EnabledCloudwatchLogsExports']]
            cw_log = '<br>'.join(map(str, cloudwatch_logs))
        except KeyError:
            cw_log = ' '
        option_groups = [x['OptionGroupName']
                         for x in i['OptionGroupMemberships']]
        option_group = '<br>'.join(map(str, option_groups))
        public_access = i['PubliclyAccessible']
    with open(file, 'a', encoding='utf-8') as f:
        f.write(f'\n\n#### {instance}'
                '\n\n| Key | Value |'
                '\n|:--|:--|'
                f'\n| Instance Type | {instance_type} |'
                f'\n| AvailabilityZone | {az} |'
                f'\n| Public Access | {public_access} |'
                f'\n| DB Parameter Group | {db_parameter_group} |'
                f'\n| Option Group | {option_group} |'
                f'\n| Enabled CloudWatchLogs | {cw_log} |'
                )

    return 0


def describe_db_instance(instance):
    """
    Auroa以外のインスタンス設定をMarkdownのTable形式へ変換して"rds.md"に出力する。

    Parameters
    ------
    instance: str
        DBインスタンスの名前。
    """

    describe_instances = client.describe_db_instances(
        DBInstanceIdentifier=instance,
    )['DBInstances']
    for i in describe_instances:
        instance_name = i['DBInstanceIdentifier']
        instance_type = i['DBInstanceClass']
        engine = i['Engine']
        engine_version = i['EngineVersion']
        status = i['DBInstanceStatus']
        endpoint = i['Endpoint']['Address']
        port = i['Endpoint']['Port']
        storage = i['AllocatedStorage']
        backup_window = i['PreferredBackupWindow']
        backup_period = i['BackupRetentionPeriod']
        security_group_ids = [x['VpcSecurityGroupId']
                              for x in i['VpcSecurityGroups']]
        security_group_id = '<br>'.join(map(str, security_group_ids))
        db_parameter_groups = [x['DBParameterGroupName']
                               for x in i['DBParameterGroups']]
        db_parameter_group = '<br>'.join(map(str, db_parameter_groups))
        vpc = i['DBSubnetGroup']['VpcId']
        db_subnet_group = i['DBSubnetGroup']['DBSubnetGroupName']
        maintenance_window = i['PreferredMaintenanceWindow']
        multi_az = i['MultiAZ']
        auto_minor_upgrade = i['AutoMinorVersionUpgrade']
        read_replicas = [x for x in i['ReadReplicaDBInstanceIdentifiers']]
        read_replica = '<br>'.join(map(str, read_replicas))
        option_groups = [x['OptionGroupName']
                         for x in i['OptionGroupMemberships']]
        option_group = '<br>'.join(map(str, option_groups))
        public_access = i['PubliclyAccessible']
        storage_type = i['StorageType']
        try:
            cloudwatch_logs = [x for x in i['EnabledCloudwatchLogsExports']]
            cw_log = '<br>'.join(map(str, cloudwatch_logs))
        except KeyError:
            cw_log = ' '
        iam_roles = [x['RoleArn'] for x in i['AssociatedRoles']]
        iam_role = '<br>'.join(map(str, iam_roles))
    with open(file, 'a', encoding='utf-8') as f:
        f.write(f'\n\n## {instance_name}'
                '\n\n| Key | Value |'
                '\n|:--|:--|'
                f'\n| Engine | {engine} {engine_version} |'
                f'\n| Instance Type | {instance_type} |'
                f'\n| Status | {status} |'
                f'\n| Endpoint | {endpoint} |'
                f'\n| Port | {port} |'
                f'\n| Storage Type | {storage_type} |'
                f'\n| Storage | {storage} GiB|'
                f'\n| VPC | {vpc} |'
                f'\n| Security Group | {security_group_id} |'
                f'\n| Public Access | {public_access} |'
                f'\n| MultiAZ | {multi_az} |'
                f'\n| Subnet Group | {db_subnet_group} |'
                f'\n| DB Parameter Group | {db_parameter_group} |'
                f'\n| Option Group | {option_group} |'
                f'\n| Enabled CloudWatchLogs | {cw_log} |'
                f'\n| Read Replica | {read_replica} |'
                f'\n| Backup (Period) | {backup_window} ({backup_period})|'
                f'\n| Maintenance Window | {maintenance_window} |'
                f'\n| Auto Minior Upgrade | {auto_minor_upgrade} |'
                f'\n| IAM Role | {iam_role} |')

    return 0


if __name__ == '__main__':
    main()
