import boto3, json, logging, os, datetime

from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

# Lamdbaで定義する変数
SLACK_CHANNEL = os.environ['SLACK_CHANNEL']
SLACK_URL     = os.environ['SLACK_URL']

# ロギング設定
logger = logging.getLogger()
logger.setLevel(logging.INFO)

client = boto3.client('logs')

# ログの最大表示数
output_limit = 5

# Lambda実行関数
def lambda_handler(event, context):
    logger.info('Event: ' + str(event))
    sns_message = json.loads(event['Records'][0]['Sns']['Message'])
    logger.info("SNS Message: " + str(sns_message))
    metric = metric_filter(sns_message['Trigger']['MetricName'], sns_message['Trigger']['Namespace'])
    logger.info('Filter: ' + str(metric))
    slack_notification(sns_message, cwlogs_filter(metric, sns_message))

# CloudWatchLogsのFilter取得
def metric_filter(metric_name, namespace):
    cw_metrics = client.describe_metric_filters(
        metricName = metric_name,
        metricNamespace = namespace
    )['metricFilters']

    return cw_metrics

# CloudWatchLogsから対象のログを取得
# アラームは5分間隔で検知する為、検知した際の5分前まで遡りログを取得
def cwlogs_filter(cw_filter, sns_message):
    group_name = cw_filter[0]['logGroupName']
    alarm_time = datetime.datetime.strptime(sns_message['StateChangeTime'][:19] ,'%Y-%m-%dT%H:%M:%S')
    unix_alarm_time = datetime.datetime.timestamp(alarm_time)
    unix_start_time = (unix_alarm_time - 300) * 1000
    unix_end_time   = unix_alarm_time * 1000
    filter = cw_filter[0]['filterPattern']

    log_messages = client.filter_log_events(
        logGroupName=group_name,
        startTime=int(unix_start_time),
        endTime=int(unix_end_time),
        filterPattern=filter,
        interleaved=True,
        limit=output_limit
    )['events']

    filter_messages = []
    for i, x in enumerate(log_messages):
       filter_messages.append(x['message'])

    return filter_messages

# Slackに通知
def slack_notification(sns_message, reason):
    alarm_name  = sns_message['AlarmName']
    new_state   = sns_message['NewStateValue']
    output_logs = '\n'.join(reason)
    slack_message = {
        'channel': SLACK_CHANNEL,
        'link_names': 1,
        'attachments':[
            {
                'as_user': True,
                'icon_emoji': ':scream:',
                'color': 'danger',
                'title': "CloudWatchAlarm",
                'text': "@channel " + "%s state is now %s: \n %s" % (alarm_name, new_state, output_logs)
            }
        ]
    }

    req = Request(SLACK_URL, json.dumps(slack_message).encode('utf-8'))
    try:
        response = urlopen(req)
        response.read()
        logger.info("Message posted to %s", slack_message['channel'])
    except HTTPError as e:
        logger.error("Request failed: %d %s", e.code, e.reason)
    except URLError as e:
        logger.error("Server connection failed: %s", e.reason)
