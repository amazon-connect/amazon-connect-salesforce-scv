# Voicemail Express Lambda Functions
The Voicemail Express solution is effectively built on four core Lambda functions. These functions also depend on modules from the [SCV Common Layers](/Common/AWSSCV-CommonLayers). 
Function | Runtime | Description
------------ | ------------- | -------------
scv_vmx_kvs_to_s3 | NodeJS 12.0 | Processes the Contact Trace Record. Uses data from the record to locate the KVS stream fragments from the recorded voicemail. It then writes the to a single WAV file and writes that file to S3. Additionally, it uses S3 object tagging to store data about the voicemail for further processing.
scv_vmx_transcriber | Python 3.8 | Sends the generated WAV file to Amazon Trasccribe for processing. Once the transcription is complete, the JSON transcript is written to S3
scv_vmx_presigner | Python 3.8 | Generates a presigned URL that allows the recording to be accessed externally without the need to login. URL expires based on the threshold set during deployment
scv_vmx_packager | Python 3.8 | Creates a case in Salesforce which includes: 1. A customized subject indicating the type of voicemail, where it belongs, and who it was from, 2. includes the caller phone number, 3. Includes a transcript of the voicemail, 4. Includes the presigned URL to the audio file. Once complete, it deletes the transcript from S3 and overwrites the contact trace record for the call to remove the voicemail flag.
