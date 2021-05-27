import os, json, logging
from awsscv.sf import Salesforce

logger = logging.getLogger()
logger.setLevel(logging.getLevelName(os.getenv('lambda_logging_level', 'INFO')))

def lambda_handler(event, context):
    logger.debug(event)

    try:
        sf_chatter_feed_id = os.getenv('sf_chatter_feed_id', None)

        ids = []

        if sf_chatter_feed_id is not None:
            sf = Salesforce()

            for record in event['Records']:
                results = sf.create_formatted_chatter_post(sf_chatter_feed_id, format_record(record), 'AllUsers');
                logger.debug(results)
                ids.append({ "id": results['id'] })

        return { "success": True, "ids": ids }

    except Exception as e:
        logger.error(e)
        return { "success": False, "error": str(e) }

def format_record(record):
    messageSegments = []

    messageSegments.extend([
        { 'markupType': 'Paragraph', 'type': 'MarkupBegin' },
        { 'markupType': 'Bold', 'type': 'MarkupBegin' },
        { 'text': record['Sns']['Subject'], 'type': 'Text'},
        { 'markupType': 'Bold', 'type': 'MarkupEnd' },
        { 'markupType': 'Paragraph', 'type': 'MarkupEnd' }
    ])

    try:
        message = json.loads(record['Sns']['Message'])

        trigger = message['Trigger']

        del message['Trigger']

        for key in message:
            value = message[key]

            messageSegments.extend([
                { 'markupType': 'Paragraph', 'type': 'MarkupBegin' },
                { 'text': '{} - {}'.format(key, value), 'type': 'Text' },
                { 'markupType': 'Paragraph', 'type': 'MarkupEnd' }
            ])

        messageSegments.extend([
            { 'text': 'Trigger', 'type': 'Text'},
            { 'markupType': 'UnorderedList', 'type': 'MarkupBegin' }
        ])

        for key in trigger:
            value = trigger[key]

            messageSegments.extend([
                { 'markupType': 'ListItem', 'type': 'MarkupBegin' },
                { 'text': '{} - {}'.format(key, value), 'type': 'Text' },
                { 'markupType': 'ListItem', 'type': 'MarkupEnd' }
            ])


        messageSegments.extend([
            { 'markupType': 'UnorderedList', 'type': 'MarkupEnd' }
        ])

    except Exception as e:
        message = record['Sns']['Message']

        messageSegments.extend([
            { 'markupType': 'Paragraph', 'type': 'MarkupBegin' },
            { 'text': 'Message - {}'.format(message), 'type': 'Text' },
            { 'markupType': 'Paragraph', 'type': 'MarkupEnd' }
        ])

    logger.debug(messageSegments)

    return messageSegments
