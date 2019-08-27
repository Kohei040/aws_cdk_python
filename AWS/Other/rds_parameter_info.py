# -*- coding: utf-8 -*-
import boto3


def aurora_parameter_group(cluster_parameter):
    """
    Aurora ClusterのParameter Groupでパラメータを変更した値のみを取得し、
    MarkdownのTable形式へ変換して"{対象グループ名}.md"に出力する。

    Parameter
    ------
    cluster_parameter: str
        Cluster Paramter Group名。
    """

    file = f'{cluster_parameter}.md'
    cluster_params = boto3.client('rds').describe_db_cluster_parameters(
        DBClusterParameterGroupName=cluster_parameter,
        Source='user'
    )['Parameters']

    with open(file, 'w', encoding='utf-8') as f:
        f.write('# Aurora Cluster Parameter Group'
                f'\n\n## {cluster_parameter}'
                '\n\n| Name | Value | Modifiable |  Source '
                '| ApplyType | Description | '
                '\n|:--|:--|:--|:--|:--|:--|')

    for cluster_param in cluster_params:
        param_name = cluster_param['ParameterName']
        try:
            param_value = cluster_param['ParameterValue']
        except KeyError:
            param_value = ' '
        modifiable = cluster_param['IsModifiable']
        apply_type = cluster_param['ApplyType']
        apply_method = cluster_param['ApplyMethod']
        description = cluster_param['Description']
        source = cluster_param['Source']

        with open(file, 'a', encoding='utf-8') as f:
            f.write(f'\n| {param_name} | {param_value} | {modifiable} | '
                    f'{source} | {apply_type}<br>({apply_method}) '
                    f'| {description} |')

    return 0


def db_parameter_group(db_parameter):
    """
    RDSのDB Parameter Groupでパラメータを変更した値のみを取得し、
    MarkdownのTable形式へ変換して"{対象グループ名}.md"に出力する。

    Parameter
    ------
    db_parameter: str
        RDSのDB Paramter Group名。
    """
    file = f'{db_parameter}.md'
    db_params = boto3.client('rds').describe_db_parameters(
        DBParameterGroupName=db_parameter,
        Source='user'
    )['Parameters']

    with open(file, 'w', encoding='utf-8') as f:
        f.write('# DB Parameter Group'
                f'\n\n## {db_parameter}'
                '\n\n| Name | Value | Modifiable |  Source '
                '| ApplyType | Description | '
                '\n|:--|:--|:--|:--|:--|:--|')

    for db_param in db_params:
        param_name = db_param['ParameterName']
        try:
            param_value = db_param['ParameterValue']
        except KeyError:
            param_value = ' '
        modifiable = db_param['IsModifiable']
        apply_type = db_param['ApplyType']
        apply_method = db_param['ApplyMethod']
        description = db_param['Description']
        source = db_param['Source']

        with open(file, 'a', encoding='utf-8') as f:
            f.write(f'\n| {param_name} | {param_value} | {modifiable} | '
                    f'{source} | {apply_type}<br>({apply_method}) '
                    f'| {description} |')

    return 0
