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
import phonenumbers
from awsscv.sf import Salesforce

logger = logging.getLogger()
logger.setLevel(logging.getLevelName(os.getenv('lambda_logging_level', 'DEBUG')))
connect_client = boto3.client('connect')

def vmx_to_sfother(writer_payload):

    logger.info('Beginning Voicemail to Salesforce Custom Object')
    logger.debug(writer_payload)

    # Format the URL to make it a user friendly link
    sf_formatted_url = '<a href="{0}" rel="noopener noreferrer" target="_blank">Play Voicemail</a>'.format(writer_payload['json_attributes']['presigned_url'])

    try:
        sf = Salesforce()

    except Exception as e:
        logger.error(e)
        logger.error('Failed to authenticate with Salesforce')
        return 'fail'

    # Create a voicemail in Salesforce
    try:
        if writer_payload['entity_type'] == 'agent':

            # Validate the agent's Salesforce ID, and correct, if necesary
            sf_agent_id = writer_payload['json_attributes']['entity_id']
            scv_agent_id_format = sf_agent_id.count('@')

            if scv_agent_id_format == 1:
                sf_agent_id = sf_agent_id.split('@')[0]
            if scv_agent_id_format == 2:
                sf_agent_id = sf_agent_id.split('@')[1]
            else:
                try:
                    get_agent_id = sf.query("SELECT Id FROM User WHERE Alias = '" + sf_agent_id + "' LIMIT 1")
                    sf_agent_id = get_agent_id[0]['Id']
                except Exception as e:
                    logger.error(e)
                    logger.error('Failed to validate Salesforce User ID')
                    return 'fail'

            data = {
                'Name': 'Direct voicemail for: ' + writer_payload['json_attributes']['entity_name'],
                os.environ['sf_vmx_transcript']: 'Voicemail transcript: ' + writer_payload['json_attributes']['transcript_contents'],
                'OwnerId': sf_agent_id,
                os.environ['sf_vmx_phone_field']: writer_payload['json_attributes']['vmx_from'],
                os.environ['sf_vmx_attributes']: json.dumps(writer_payload['json_attributes']),
                os.environ['sf_vmx_field']: sf_formatted_url
            }

        else:
            data = {
                'Name': 'Queue voicemail for: ' + writer_payload['json_attributes']['entity_name'],
                os.environ['sf_vmx_transcript']: 'Voicemail transcript: ' + writer_payload['json_attributes']['transcript_contents'],
                os.environ['sf_vmx_phone_field']: writer_payload['json_attributes']['vmx_from'],
                os.environ['sf_vmx_attributes']: json.dumps(writer_payload['json_attributes']),
                os.environ['sf_vmx_field']: sf_formatted_url
            }
        logger.debug(data)

        do_create = sf.create(sobject=os.environ['sf_vmx_custom_object'], data=data)

        logger.info('Salesforce custom voicemail created [{0}]'.format(do_create))
        return 'success'

    except Exception as e:
        logger.error(e)
        logger.error('Failed to create Salesforce custom voicemail')
        return 'fail'
