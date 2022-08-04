# Version: 2022.04.15
"""
**********************************************************************************************************************
 *  Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved                                            *
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
import json
import boto3
import os
import logging

logger = logging.getLogger()
logger.setLevel(logging.getLevelName(os.getenv('lambda_logging_level', 'INFO')))

def lambda_handler(event, context):
    logger.debug(event)

    # Establish a loop counter
    loop_counter = 0

    # Process the incoming S3 event
    for recording in event['Records']:

        # Increment loop
        loop_counter = loop_counter+1

        # Grab incoming data elements from the S3 event
        try:
            recording_key = recording['s3']['object']['key']
            recording_name = recording_key.replace('voicemail_recordings/','')
            contact_id = recording_name.replace('.wav','')
            recording_bucket = recording['s3']['bucket']['name']

        except Exception as e:
            logger.error(e)
            logger.debug('Record {0} Result: Failed to extract data from event'.format(loop_counter))
            continue

        # Establish the S3 client and get the object tags
        try:
            s3_client = boto3.client('s3')
            object_data = s3_client.get_object_tagging(
                Bucket=recording_bucket,
                Key=recording_key
            )

            object_tags = object_data['TagSet']
            loaded_tags = {}

            for i in object_tags:
                loaded_tags.update({i['Key']:i['Value']})

        except Exception as e:
            logger.error(e)
            logger.debug('Record {0} Result: Failed to extract tags from object'.format(loop_counter))
            continue

        # Build the Recording URL
        try:
            recording_url = 'https://{0}.s3-{1}.amazonaws.com/{2}'.format(recording_bucket, recording['awsRegion'], recording_key)

        except Exception as e:
            logger.error(e)
            logger.debug('Record {0} Result: Failed to generate recording URL'.format(loop_counter))
            continue

        # Do the transcription
        try:
            # Esteablish the client
            transcribe_client = boto3.client('transcribe')

            # Submit the transcription job
            transcribe_response = transcribe_client.start_transcription_job(
                TranscriptionJobName=contact_id,
                LanguageCode=loaded_tags['vm_lang'],
                MediaFormat='wav',
                Media={
                    'MediaFileUri': recording_url
                },
                OutputBucketName=os.environ['s3_transcripts_bucket']
            )

        except Exception as e:
            logger.error(e)
            logger.debug('Record {0} Result: Transcription job failed'.format(loop_counter))
            continue

        logger.debug('Record {0} Result: Success!'.format(loop_counter))

    return {
        'status': 'complete',
        'result': '{0} records processed'.format(loop_counter)
    }
