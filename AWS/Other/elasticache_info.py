# -*- coding: utf-8 -*-
import boto3

file = 'elasticache.md'
client = boto3.client('elasticache')


def main():
    """
    ElastiCache(Redis)の情報を取得する関数を呼び出す。
    ※Cluster Modeは非対応
    """

    with open(file, 'w', encoding='utf-8') as f:
        f.write('# ElastiCache(Redis)')

    # Replica Group
    get_replica_groups = client.describe_replication_groups(
    )['ReplicationGroups']
    for replica_group in get_replica_groups:
        describe_cluster(replica_group)

    # Single Node
    single_nodes = client.describe_cache_clusters(
        ShowCacheNodeInfo=True,
        ShowCacheClustersNotInReplicationGroups=True
    )['CacheClusters']
    for node in single_nodes:
        describe_node(node)

    return 0


def describe_cluster(replica_group):
    """
    RedisのRepalica Groupの設定情報を取得し、
    MarkdownのTable形式へ変換して"elasticache.md"に出力する。

    Parameter
    ------
    replica_group: str
        Replica Groupの名称。
    """

    cluster_name = replica_group['ReplicationGroupId']
    description = replica_group['Description']
    status = replica_group['Status']
    node_type = replica_group['CacheNodeType']
    member_clusters = [i for i in replica_group['MemberClusters']]
    cluster = '<br>'.join(map(str, member_clusters))
    encryption_transit = replica_group['TransitEncryptionEnabled']
    encryption_at_rest = replica_group['AtRestEncryptionEnabled']
    backup = replica_group['SnapshotWindow']
    backup_period = replica_group['SnapshotRetentionLimit']

    for node in replica_group['NodeGroups']:
        node_id = node['NodeGroupId']
        node_status = node['Status']
        primary_endpoint = node['PrimaryEndpoint']['Address']
        primary_port = node['PrimaryEndpoint']['Port']
        reader_endpoint = node['ReaderEndpoint']['Address']
        reader_port = node['ReaderEndpoint']['Port']
        availability_zones = [i['PreferredAvailabilityZone']
                              for i in node['NodeGroupMembers']]
        az = '<br>'.join(map(str, availability_zones))

    describe_node = client.describe_cache_clusters(
        CacheClusterId=member_clusters[0]
    )['CacheClusters'][0]

    engine = describe_node['Engine']
    engine_version = describe_node['EngineVersion']
    security_groups = [i['SecurityGroupId']
                       for i in describe_node['SecurityGroups']]
    security_group = '<br>'.join(map(str, security_groups))
    subnet_group = describe_node['CacheSubnetGroupName']
    parameter_group = (describe_node['CacheParameterGroup']
                       ['CacheParameterGroupName'])
    maintenance = describe_node['PreferredMaintenanceWindow']

    with open(file, 'a', encoding='utf-8') as f:
        f.write(f'\n\n## {cluster_name}'
                '\n\n| Key | Value |'
                '\n|:--|:--|'
                f'\n| Engine | {engine} {engine_version} |'
                f'\n| Description | {description} |'
                f'\n| Status | {status} |'
                f'\n| Cluster Member | {cluster} |'
                f'\n| Node Type | {node_type} |'
                f'\n| Primary Endpoint | {primary_endpoint}:{primary_port} |'
                f'\n| Reader Endpoint | {reader_endpoint}:{reader_port} |'
                f'\n| Security Group | {security_group} |'
                f'\n| Availability Zones | {az} |'
                f'\n| Subent Group | {subnet_group} |'
                f'\n| Parameter Group | {parameter_group} |'
                f'\n| Maintenance Window | {maintenance} |'
                f'\n| Backup Window (Period) | {backup} ({backup_period}) |'
                f'\n| Encryption in-transit | {encryption_transit} |'
                f'\n| Encryption at-rest | {encryption_at_rest} |')

    return 0


def describe_node(node):
    """
    RedisのSingle Nodeの設定情報をMarkdownのTable形式へ変換して"elasticache.md"に出力する。

    Parameter
    ------
    node: dict
        Nodeの設定情報。
    """

    node_name = node['CacheClusterId']
    engine = node['Engine']
    engine_version = node['EngineVersion']
    status = node['CacheClusterStatus']
    node_type = node['CacheNodeType']
    endpoint = node['CacheNodes'][0]['Endpoint']['Address']
    port = node['CacheNodes'][0]['Endpoint']['Port']
    security_groups = [i['SecurityGroupId'] for i in node['SecurityGroups']]
    security_group = '<br>'.join(map(str, security_groups))
    az = node['PreferredAvailabilityZone']
    subnet_group = node['CacheSubnetGroupName']
    parameter_group = node['CacheParameterGroup']['CacheParameterGroupName']
    maintenance = node['PreferredMaintenanceWindow']
    backup = node['SnapshotWindow']
    backup_period = node['SnapshotRetentionLimit']
    encryption_transit = node['TransitEncryptionEnabled']
    encryption_at_rest = node['AtRestEncryptionEnabled']

    with open(file, 'a', encoding='utf-8') as f:
        f.write(f'\n\n## {node_name}'
                '\n\n| Key | Value |'
                '\n|:--|:--|'
                f'\n| Engine | {engine} {engine_version} |'
                f'\n| Status | {status} |'
                f'\n| Node Type | {node_type} |'
                f'\n| Endpoint | {endpoint}:{port} |'
                f'\n| Security Group | {security_group} |'
                f'\n| Availability Zones | {az} |'
                f'\n| Subent Group | {subnet_group} |'
                f'\n| Parameter Group | {parameter_group} |'
                f'\n| Maintenance Window | {maintenance} |'
                f'\n| Backup Window (Period) | {backup} ({backup_period}) |'
                f'\n| Encryption in-transit | {encryption_transit} |'
                f'\n| Encryption at-rest | {encryption_at_rest} |')

    return 0


if __name__ == '__main__':
    main()
