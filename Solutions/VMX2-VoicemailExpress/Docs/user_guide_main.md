# Using Voicemail Express
The Voicemail Express solution is designed to operate with minimal configuration requirements, however there are a few key items that must be setup correctly for the solution to work. Depending on your delivery model, the requirements will vary but there are a core set of paramters required for all voicemail delivery models to work.

## How Voicemail Express Works
Voicemails are initialized in the Amazon Connect contact flows that provide the customer experience for voicemail. Most of the actual processing is done post-call via Contact Trace Record (CTR) analysis. As Amazon Connect emits contact trace records via a Kinesis Data Stream, a set of AWS Lambda functions scans those records and performs the processes required to deliver the voicemail. This is a four step process.

### 1. CTR processing with the vmx_kvs_to_s3 function
The vmx_kvs_to_s3 Lambda function processes the CTR events in the Kinesis data stream, checking to see if there is a voicemail indicator in the contact attributes for each record. It is specifically looking for an attribute with the key of **vm_flag** with a value of **1**. This tells the Lambda function to process the CTR as a voicemail. Once it identifies that the CTR is for a voicemail, it scans the CTR data to determine the Kinesis Video Stream information that was used to capture the customer audio along with some base data about the call, such as Contact ID, Queue ARN, voicemail language, etc. It uses the KVS information to extract the audio from the KVS stream and write it to S3. When writing the file to S3, it names the recording using the contact ID. Since this solution does not use any tracking database (to be in compliance with Service Cloud Voice's limited service stack) the function writes some key data as metadata on the recording in S3. This allows the solution to pass data along to the subsequent functions. When the voicemail recording is saved to S3, it generates an event that triggers the next step in the process.

### 2. Voicemail transcription with the vmx_transcriber function
When the voicemail recording is PUT into s3, it invokes the vmx_transcriber function. This function creates a new transcription job using the contact ID. It also pulls the language code for this transcription from the s3 object metadata that was written in the previous step. The generates a transcription that is written to s3. Once the transcription is written to s3, the next step in the process is triggered


## Core Contact Flow Parameters
x
