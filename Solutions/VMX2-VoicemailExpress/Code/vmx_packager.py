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

# Import the VMX Model Types
import sub_connect_task
import sub_ses_email
import sub_salesforce_case
import sub_salesforce_other
import sub_other

logger = logging.getLogger()
logger.setLevel(logging.getLevelName(os.getenv('lambda_logging_level', 'DEBUG')))
connect_client = boto3.client('connect')

def lambda_handler(event, context):
    logger.debug(event)
    loop_counter = 0

    # Process the records in the event
    for record in event['Records']:
        # Establish writer data
        writer_payload = {}

        # Increment loop counter
        loop_counter = loop_counter+1

        # Establish data for transcript and recording
        try:
            transcript_key = record['s3']['object']['key']
            contact_id = transcript_key.replace('.json','')
            recording_key = transcript_key.replace('.json','.wav')
            transcript_bucket = os.environ['s3_transcripts_bucket']
            recording_bucket = os.environ['s3_recordings_bucket']

        except Exception as e:
            logger.error(e)
            logger.error('Record {0} Result: Failed to extract keys'.format(loop_counter))
            continue

        # Invoke presigner Lambda to generate presigned URL for recording
        try:
            client = boto3.client('lambda')

            input_params = {
                'recording_bucket': recording_bucket,
                'recording_key': recording_key
            }

            lambda_response = client.invoke(
                FunctionName = os.environ['presigner_function_arn'],
                InvocationType = 'RequestResponse',
                Payload = json.dumps(input_params)
            )
            response_from_presigner = json.load(lambda_response['Payload'])
            raw_url = response_from_presigner['presigned_url']

        except Exception as e:
            logger.error(e)
            logger.error('Record {0} Result: Failed to generate presigned URL'.format(loop_counter))
            continue

        # Extract the tags from the recording object
        try:
            s3_client = boto3.client('s3')
            object_data = s3_client.get_object_tagging(
                Bucket = recording_bucket,
                Key = recording_key
            )

            object_tags = object_data['TagSet']
            loaded_tags = {}

            for i in object_tags:
                loaded_tags.update({i['Key']:i['Value']})

        except Exception as e:
            logger.error(e)
            logger.error('Record {0} Result: Failed to extract tags'.format(loop_counter))
            continue

        # Grab the transcript from S3
        try:
            s3_resource = boto3.resource('s3')

            transcript_object = s3_resource.Object(transcript_bucket, transcript_key)
            file_content = transcript_object.get()['Body'].read().decode('utf-8')
            json_content = json.loads(file_content)

            transcript_contents = json_content['results']['transcripts'][0]['transcript']

        except Exception as e:
            logger.error(e)
            logger.error('Record 0 Result: Failed to retrieve transcript'.format(loop_counter))
            continue

        # Set some key vars
        queue_arn = loaded_tags['vm_queue_arn']
        arn_substring = queue_arn.split('instance/')[1]
        instance_id = arn_substring.split('/queue')[0]
        queue_id = arn_substring.split('queue/')[1]
        writer_payload.update({'instance_id':instance_id,'contact_id':contact_id,'queue_id':queue_id,'loop_counter':loop_counter})

        # Determine queue type and set additional vars
        if queue_id.startswith('agent'):
            try:
                writer_payload.update({'entity_type':'agent'})
                # Set the Agent ID
                agent_id = arn_substring.split('agent/')[1]
                # Grab agent info
                get_agent = connect_client.describe_user(
                    UserId = agent_id,
                    InstanceId = instance_id
                )
                logger.debug(get_agent['User']['IdentityInfo'])
                entity_name = get_agent['User']['IdentityInfo']['FirstName']+' '+get_agent['User']['IdentityInfo']['LastName']
                entity_id = get_agent['User']['Username']
                entity_description = 'Amazon Connect Agent'

            except Exception as e:
                logger.error(e)
                logger.error('Record {0} Result: Failed to find agent'.format(loop_counter))
                entity_name = 'UNKNOWN'

        else:
            writer_payload.update({'entity_type':'queue'})
            # Grab Queue info
            get_queue_details = connect_client.describe_queue(
                InstanceId=instance_id,
                QueueId=queue_id
            )

            try:
                entity_name = get_queue_details['Queue']['Name']
                entity_id = get_queue_details['Queue']['QueueArn']
                entity_description = get_queue_details['Queue']['Description']
            except Exception as e:
                logger.error(e)
                logger.error('Record {0} Result: Failed to extract queue name'.format(loop_counter))
                entity_name = 'UNKNOWN'

        # Get the existing contact attributes from the call and append the standard vars for voicemail to the attributes
        try:
            contact_attributes = connect_client.get_contact_attributes(
                InstanceId = instance_id,
                InitialContactId = contact_id
            )
            json_attributes = contact_attributes['Attributes']
            json_attributes.update({'entity_name':entity_name,'entity_id':entity_id,'entity_description':entity_description,'transcript_contents':transcript_contents,'callback_number':json_attributes['vm_from'],'presigned_url':raw_url})
            writer_payload.update({'json_attributes':json_attributes})
            contact_attributes = json.dumps(contact_attributes['Attributes'])

        except Exception as e:
            logger.error(e)
            logger.error('Record {0} Result: Failed to extract attributes'.format(loop_counter))
            contact_attributes = 'UNKNOWN'

        logger.debug(writer_payload)

        # Determing VMX mode
        if 'vm_mode' in writer_payload['json_attributes']:
            if writer_payload['json_attributes']['vm_mode']:
                vm_mode = writer_payload['json_attributes']['vm_mode']
        else:
            vm_mode = os.environ['default_vm_mode']

        logger.debug('VM Mode set to {0}.'.format(vm_mode))

        # Execute the correct VMX mode
        if vm_mode == 'task':

            try:
                write_vm = sub_connect_task.vm_to_connect_task(writer_payload)

            except Exception as e:
                logger.error(e)
                logger.error('Failed to activate task function')
                continue

        elif vm_mode == 'email':

            try:
                write_vm = sub_ses_email.vm_to_ses_email(writer_payload)

            except Exception as e:
                logger.error(e)
                logger.error('Failed to activate email function')
                continue

        elif vm_mode == 'sfcase':
            # Set case Here
            try:
                write_vm = sub_salesforce_case.vm_to_sfcase(writer_payload)

            except Exception as e:
                logger.error(e)
                logger.error('Failed to activate email function')
                continue

        elif vm_mode == 'sfother':
            # Set Task Here
            try:
                write_vm = sub_salesforce_other.vm_to_sfother(writer_payload)

            except Exception as e:
                logger.error(e)
                logger.error('Failed to activate email function')
                continue

        elif vm_mode == 'other':
            # Set other Here
            try:
                write_vm = sub_other.vm_to_other(writer_payload)

            except Exception as e:
                logger.error(e)
                logger.error('Failed to activate email function')
                continue

        else:
            logger.error('Invalid mode selection')
            continue

        if write_vm == 'success':
            logger.info('Record {0} VM successfully written'.format(loop_counter))

        else:
            logger.info('Record {0} VM failed to write'.format(loop_counter))
            continue

        # End Voicemail Writer

        # Do some cleanup
        # Delete the transcription job
        try:
            transcribe_client = boto3.client('transcribe')
            transcribe_client.delete_transcription_job(
                TranscriptionJobName=contact_id
            )

        except Exception as e:
            logger.error(e)
            logger.error('Record {0} Failed to delete transcription job'.format(loop_counter))

        # Clear the vm_flag for this contact
        try:

            update_flag = connect_client.update_contact_attributes(
                InitialContactId=contact_id,
                InstanceId=instance_id,
                Attributes={
                    'vm_flag': '0'
                }
            )

        except Exception as e:
            logger.error(e)
            logger.error('Record {0} Failed to change vm_flag'.format(loop_counter))

    return {
        'status': 'complete',
        'result': '{0} records processed'.format(loop_counter)
    }
