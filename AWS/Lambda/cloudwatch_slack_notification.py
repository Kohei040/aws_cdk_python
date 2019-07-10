import boto3, json, logging, os

from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

SLACK_CHANNEL = os.environ['CHANNEL_NAME']
HOOK_URL = os.environ['SLACK_URL']

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info("Event: " + str(event))
    message = json.loads(event['Records'][0]['Sns']['Message'])
    logger.info("Message: " + str(message))

    alarm_name = message['AlarmName']
    new_state = message['NewStateValue']
    reason = message['NewStateReason']

    slack_message = {
        'channel': SLACK_CHANNEL,
        'link_names': 1,
        'attachments':[
            {
                'as_user': True,
                'icon_emoji': ':scream:',
                'color': 'danger',
                'title': "CloudWatchAlarm",
                'text': "@channel " + "%s state is now %s: %s" % (alarm_name, new_state, reason)
            }
        ]
    }

    req = Request(HOOK_URL, json.dumps(slack_message).encode('utf-8'))
    try:
        response = urlopen(req)
        response.read()
        logger.info("Message posted to %s", slack_message['channel'])
    except HTTPError as e:
        logger.error("Request failed: %d %s", e.code, e.reason)
    except URLError as e:
logger.error("Server connection failed: %s", e.reason)
