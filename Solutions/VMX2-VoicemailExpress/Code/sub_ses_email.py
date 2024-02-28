# Version: 2024.02.28
"""
**********************************************************************************************************************
 *  Copyright 2020 Amazon.com, Inc. or its affiliates. All Rights Reserved                                            *
 *                                                                                                                    *
 *  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated      *
 *  documentation files (the "Software"), to deal in the Software without restriction, including without limitation   *
 *  the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and  *
 *  to permit persons to whom the Software is furnished to do so.                                                     *
 *                                                                                                                    *
 *  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO  *
 *  THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE    *
 *  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF         *
 *  CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS *
 *  IN THE SOFTWARE.                                                                                                  *
 **********************************************************************************************************************
"""

# Import the necessary modules for this flow to work
import json
import os
import logging
import boto3

logger = logging.getLogger()
logger.setLevel(logging.getLevelName(os.getenv('lambda_logging_level', 'DEBUG')))
connect_client = boto3.client('connect')
ses_client = boto3.client('sesv2')

def vmx_to_ses_email(writer_payload):

    logger.info('Beginning Voicemail to email')
    logger.debug(writer_payload)

    # Identify the proper address to send the email FROM
    if 'email_from' in writer_payload['json_attributes']:
        if writer_payload['json_attributes']['email_from']:
            vmx_email_from_address = writer_payload['json_attributes']['email_from']
    else:
        vmx_email_from_address = os.environ['default_email_from']

    # Set destination address
    if writer_payload['entity_type'] == 'agent':
        vmx_email_target_address = writer_payload['json_attributes']['entity_id']

    elif writer_payload['entity_type'] == 'queue':
        vmx_email_target_address = writer_payload['json_attributes']['entity_description'].split('QVMB::')[1]

    else:
        vmx_email_target_address = os.environ['default_email_target']

    if '@' in vmx_email_target_address:
        logger.info('Valid email address format')

    else:
        vmx_email_target_address = os.environ['default_email_target']


    if 'email_template' in writer_payload['json_attributes']:
        if writer_payload['json_attributes']['email_template']:
            vmx_email_template = writer_payload['json_attributes']['email_template']

    else:
        if writer_payload['entity_type'] == 'agent':
            vmx_email_template = os.environ['default_agent_email_template']

        else:
            vmx_email_template = os.environ['default_queue_email_template']

    vmx_email_data = json.dumps(writer_payload['json_attributes'])

    # Send the email
    try:

        send_email = ses_client.send_email(
            FromEmailAddress=vmx_email_from_address,
            Destination={
                'ToAddresses': [
                    vmx_email_target_address,
                ],
            },
            Content={
                'Template': {
                    'TemplateName': vmx_email_template,
                    'TemplateData': vmx_email_data
                }
            }
        )

        return 'success'

    except Exception as e:
        logger.error(e)
        logger.error('Failed to send email.')

        return 'fail'
