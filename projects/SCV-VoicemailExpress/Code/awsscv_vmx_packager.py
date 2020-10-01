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

# Import the necessary moduels for this flow to work
import json
import os
import boto3
from awsscv.sf import Salesforce
import phonenumbers

def lambda_handler(event, context):
    # Uncomment the following line for debugging
    # print(event)
    loop_counter = 0

    # Process the records in the CTR
    for record in event['Records']:

        # Increment Loop
        loop_counter = loop_counter+1

        # Establish data for transcript and recording
        try:
            transcript_key = record['s3']['object']['key']
            contact_id = transcript_key.replace('.json','')
            recording_key = transcript_key.replace('.json','.wav')
            transcript_bucket = os.environ['s3_transcripts_bucket']
            recording_bucket = os.environ['s3_recordings_bucket']

        except:
            print('Record ' + str(loop_counter) + ' Result: Failed to extract keys')
            continue

        # Invoke presigner Lambda to generate presigned URL for recording and format for Salesforce
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
            formatted_url = '<a href="' + response_from_presigner['presigned_url'] + '" rel="noopener noreferrer" target="_blank">Play Voicemail</a>'

        except:
            print('Record ' + str(loop_counter) + ' Result: Failed to generate presigned URL')
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

        except:
            print('Record ' + str(loop_counter) + ' Result: Failed to extract tags')
            continue

        # Grab the transcript
        try:
            s3_resource = boto3.resource('s3')

            transcript_object = s3_resource.Object(transcript_bucket, transcript_key)
            file_content = transcript_object.get()['Body'].read().decode('utf-8')
            json_content = json.loads(file_content)

            transcript_contents = json_content['results']['transcripts'][0]['transcript']

        except:
            print('Record ' + str(loop_counter) + ' Result: Failed to retrieve transcript')
            continue

        # Determine the queue/agent name
        if loaded_tags['vm_queue_type'] == 'agent':
            vm_prefix = 'Direct'
            try:
                queue_arn = loaded_tags['vm_queue_arn']
                split_1 = queue_arn.split('instance/')[1]
                instance_id = split_1.split('/queue')[0]
                agent_id = split_1.split('agent/')[1]

                connect_client = boto3.client('connect')
                get_agent = connect_client.describe_user(
                    UserId=agent_id,
                    InstanceId=instance_id
                )
                print(get_agent['User']['IdentityInfo'])
                entity_name = get_agent['User']['IdentityInfo']['FirstName']+' '+get_agent['User']['IdentityInfo']['LastName']
            except:
                print('Record ' + str(loop_counter) + ' Result: Failed to find agent')
                entity_name = 'UNKNOWN'

        else:
            vm_prefix = 'Queue'
            try:
                entity_name = loaded_tags['vm_queue_name']
            except:
                print('Record ' + str(loop_counter) + ' Result: Failed to extract queue name')
                entity_name = 'UNKNOWN'

        # Build the human readable phone number for the subject
        try:
            incoming_phone = '+' + loaded_tags['vm_from']
            parsed_phone = phonenumbers.parse(incoming_phone, None)
            international_phone = phonenumbers.format_number(parsed_phone, phonenumbers.PhoneNumberFormat.INTERNATIONAL)

        except:
            international_phone = '+' + loaded_tags['vm_from']

        # Perform the salesforce login
        try:
            sf = Salesforce()

        except:
            print('Record ' + str(loop_counter) + ' Result: Failed to authenticate with Salesforce')
            continue

        # Create a case in Salesforce
        try:
            data = {
                'Subject': vm_prefix + ' voicemail for: ' + entity_name + ', from : ' + international_phone,
                'Description': 'Voicemail transcript: ' + transcript_contents,
                'Status': 'New',
                'Priority': loaded_tags['vm_priority'],
                'Origin': 'Phone',
                os.environ['sf_case_vm_phone_field']: international_phone,
                os.environ['sf_case_vm_field']: formatted_url
            }
            print(data)

            response = sf.create(sobject='Case', data=data)
            sf_case = response

        except:
            print('Record ' + str(loop_counter) + ' Result: Failed to create case')
            continue

        # Delete the transcription
        try:
            transcript_delete = transcript_object.delete()

        except:
            print('Record ' + str(loop_counter) + ' Failed to delete transcript')

        print('Record ' + str(loop_counter) + ' Result: Success!')

        # Clear the vm_flag for this contact
        try:
            # Grab instance ID
            queue_arn = loaded_tags['vm_queue_arn']
            split_1 = queue_arn.split('instance/')[1]
            instance_id = split_1.split('/queue')[0]

            # Do the update
            update_flag = connect_client.update_contact_attributes(
                InitialContactId=contact_id,
                InstanceId=instance_id,
                Attributes={
                    'vm_flag': '0'
                }
            )

        except:
            print('Record ' + str(loop_counter) + ' Failed to change vm_flag')

    return {
        'status': 'complete',
        'result': str(loop_counter) + ' records processed'
    }
