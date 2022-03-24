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
# Version: 2021.12.14

import json
import boto3
import logging
from botocore.client import Config
import base64
import os

logger = logging.getLogger()
logger.setLevel(logging.getLevelName(os.getenv('lambda_logging_level', 'INFO')))

def lambda_handler(event, context):
    logger.debug(event)

    # Establsih an empty response
    response = {}
    # Set the default result to success
    response.update({'result':'success'})

    # Retrieve credentials from AWS Secrets Manager
    try:
        use_keys = get_secret()

    except Exception as e:
        logger.error(e)
        response.update({'result':'fail'})
        response.update({'detail':'key retrieval failed'})
        return response

    # Configure the environment for the URL generation and initialize s3 client
    try:
        my_config = Config(
            region_name = os.environ['aws_region'],
            signature_version = 's3v4',
            retries = {
                'max_attempts': 10,
                'mode': 'standard'
            }
        )

        client = boto3.client(
            's3',
            aws_access_key_id = use_keys['AWSSCV_vmx_iam_key_id'],
            aws_secret_access_key = use_keys['AWSSCV_vmx_iam_key_secret'],
            config=my_config
        )

    except Exception as e:
        logger.error(e)
        response.update({'result':'fail'})
        response.update({'detail':'s3 client init failed'})
        return response

    # Generate the presigned URL and return
    try:
        presigned_url = client.generate_presigned_url('get_object',
            Params = {'Bucket': event['recording_bucket'],
                    'Key': event['recording_key']},
            ExpiresIn = int(os.environ['s3_obj_lifecycle'])*86400
        )
        response.update({'presigned_url': presigned_url})

        return response

    except Exception as e:
        logger.error(e)
        response.update({'result':'fail'})
        response.update({'detail':'presigned url generation failed'})
        logger.debug(response)
        return response

# Sub to retrieve the secrets from Secrets Manager
def get_secret():
    # Set vars
    secret_response = {}
    try:
        secret_name = os.environ['secrets_key_id']
        region_name = os.environ['aws_region']

    except Exception as e:
        logger.error(e)
        secret_response.update({'result':'fail'})
        secret_response.update({'detail':'environment vars failed'})
        return secret_response

    # Create a Secrets Manager session
    try:
        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name=region_name
        )

    except Exception as e:
        logger.error(e)
        secret_response.update({'result':'fail'})
        secret_response.update({'detail':'AWS Secrets Manager session failed'})
        return secret_response

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )

    except Exception as e:
        logger.error(e)
        secret_response.update({'result':'fail'})
        secret_response.update({'detail':'failed to get secrets'})
        return secret_response

    else:
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
        else:
            decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])

    secret_response.update(json.loads(secret))

    return secret_response
