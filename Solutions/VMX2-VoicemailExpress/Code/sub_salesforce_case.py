# Version: 2022.03.23
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
import phonenumbers
from awsscv.sf import Salesforce

logger = logging.getLogger()
logger.setLevel(logging.getLevelName(os.getenv('lambda_logging_level', 'DEBUG')))
connect_client = boto3.client('connect')

def vm_to_sfcase(writer_payload):

    logger.info('Beginning Voicemail to Salesforce Case')
    logger.debug(writer_payload)

    try:
        sf = Salesforce()

    except Exception as e:
        logger.error(e)
        logger.error('Record {0} Result: Failed to authenticate with Salesforce'.format(writer_payload['loop_counter']))
        return 'fail'

    # Format the URL to make it a user friendly link
    sf_formatted_url = '<a href="{0}" rel="noopener noreferrer" target="_blank">Play Voicemail</a>'.format(writer_payload['json_attributes']['presigned_url'])

    # Create a case in Salesforce
    try:
        if writer_payload['entity_type'] == 'agent':
            # Validate the agent's Salesforce ID, and correct, if necesary
            sf_agent_id = writer_payload['json_attributes']['entity_id']

            if not sf_agent_id.startswith('005'):
                try:
                    get_agent_id = sf.query("SELECT Id FROM User WHERE Alias = '" + sf_agent_id + "' LIMIT 1")
                    sf_agent_id = get_agent_id[0]['Id']
                except Exception as e:
                    logger.error(e)
                    logger.error('Record {0} Result: Failed to validate Salesforce User ID'.format(writer_payload['loop_counter']))
                    return 'fail'
            if '@' in sf_agent_id:
                sf_agent_id = sf_agent_id.split('@')[0]

            data = {
                'Subject': 'Direct voicemail for: ' + writer_payload['json_attributes']['entity_name'] + ' from : ' + writer_payload['json_attributes']['vm_from'],
                'Description': 'Voicemail transcript: ' + writer_payload['json_attributes']['transcript_contents'],
                'Status': 'New',
                'Origin': 'Phone',
                'Priority': writer_payload['json_attributes']['vm_priority'],
                'OwnerId': sf_agent_id,
                os.environ['sf_vm_phone_field']: writer_payload['json_attributes']['vm_from'],
                os.environ['sf_vm_attributes']: json.dumps(writer_payload['json_attributes']),
                os.environ['sf_vm_field']: sf_formatted_url
            }

        else:
            data = {
                'Subject': 'Queue voicemail for: ' + writer_payload['json_attributes']['entity_name'] + ' from : ' + writer_payload['json_attributes']['vm_from'],
                'Description': 'Voicemail transcript: ' + writer_payload['json_attributes']['transcript_contents'],
                'Status': 'New',
                'Origin': 'Phone',
                'Priority': writer_payload['json_attributes']['vm_priority'],
                os.environ['sf_vm_phone_field']: writer_payload['json_attributes']['vm_from'],
                os.environ['sf_vm_attributes']: json.dumps(writer_payload['json_attributes']),
                os.environ['sf_vm_field']: sf_formatted_url
            }
        logger.debug(data)

        do_create = sf.create(sobject='Case', data=data)

        logger.info('Record {0} Result: Salesforce Case created [{1}]'.format(writer_payload['loop_counter'], do_create))
        return 'success'

    except Exception as e:
        logger.error(e)
        logger.error('Record {0} Result: Failed to create Salesforce Case'.format(writer_payload['loop_counter']))
        return 'fail'
