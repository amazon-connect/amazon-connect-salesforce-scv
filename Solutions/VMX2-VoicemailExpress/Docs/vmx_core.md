# High-level overview of the Voicemail Express solution
Voicemail Express provides basic voicemail functionality for Amazon Connect Customers. It is a solution that has been designed to be easy to deploy and maintain. As such, there is a limited feature stack, and few administrative options, however all of the code is open and customizable to fit different customer needs. This page will provide a foundational understanding of how the solution works.

## High-Level Flow
Voicemails are captured in the Amazon Connect contact flow, processed post-call, and delivered using the selected delivery mode. Here is a quick overview of the basic steps required:
1.  Customer calls in, is provided the option to leave a voicemail (for whatever reason), and decides to do so.
2.  Specific contact attributes are set to mark the contact as having a voicemail
3.  An Amazon Kinesis Video Stream (KVS) is initialized to record the audio from the customer
4.  Customer completes the message and ends the call
5.  A contact trace record (CTR) is emitted for the contact via Amazon Kinesis Data Stream
6.  That CTR triggers the VMXKVStoS3 AWS Lambda function. This function:
   -  Identifies that the contact is a voicemail
   -  Retrieves some key data about the contact
   -  Extracts the voicemail recording from the KVS stream
   -  Writes the voicemail recording to an Amazon Simple Storage Service (S3) bucket, using the extracted data as metadata
7. The creation of the recording object in S3 triggers the next Lambda function, VMXTranscriber. This function:
    -  Retrieves the recording file from S3
    -  Uses the metadata to create a new transcription job
    -  The transcription job writes the completed transcription to a different S3 bucket
8.  The creation of the transcription object in S3 triggers the next Lambda function, VMXPackager. This function:
    -  Retrieves the transcript file from S3
    -  Uses the data in the transcript file identify the contact and find the recording
    -  Retrieves the metadata from the recording file
    -  Invokes the VMXPresigner function to generate a presigned URL for the recording
    -  Determines queue/agent information, deliver mode, destination, etc
    -  Invokes the appropriate function for the delivery mode
    -  Once delivery is successful, it deletes the existing transcription job
    - Finally, the contact attributes are updated to remove the voicemail flag so future instances of this CTR do not generate new voicemails.

## Required Contact Attributes (All Modes)
In order for the voicemail system to work, contacts must have certain contact attributes set. Regardless of mode, the following attributes are used:
- **vm_flag (Required)**: (0,1) this attribute flags the call as requiring processing by the voicemail solution. All new voicemails should have this value set to `1`. When the packager function completes, it will update the value to `0`. If this value is set to anything other than `1` or is missing altogether, the voicemail system will ignore the CTR and voicemail processing WILL NOT HAPPEN. Example: 'vm_flag':'1'
- **vm_from (Reqiured)**: (customer phone in E.164 format) this attribute indicates the phone number of the customer. You can set this using the System attribute of `Customer number` ($.CustomerEndpoint.Address) or set this to a phone number provided by the customer. It should always be in E.164 format. Example: 'vm_from':'+15555551212'
- **vm_queue_arn (Required)**: (ARN) the Amazon Resource Number of the queue that this voicemail should belong to. In most cases, it makes most practical sense to first set the appropriate queue as the working queue, then to set this attribute using the System attribute of `Queue ARN` ($.Queue.ARN). This is critical as the Lambda functions use the queue ARN to determine the target queue, instance ID, queue mode (agent vs queue), etc. Example: 'vm_queue_arn':'arn:aws:connect:us-east-1:YOURACCOUNTNUMBER:instance/YOURINSTANCEID/queue/YOURQUEUEID'
- **vm_lang (Required)**: (Language code) the language code that Transcribe should use when transcribing the call. The list of supported languages and their language codes can be found in the [Amazon Transcribe Developer Guide](https://docs.aws.amazon.com/transcribe/latest/dg/supported-languages.html).
- **vm_mode (Optional)**: (email|task|sfcase|sfother|other) which delivery mode should be used for this voicemail. If nothing is provided, the voicemail will be delivered via the default mode selected during implementation. Example: 'vm_mode':'task'

There are additional contact attributes for each delivery mode. For details, please refer to the documentation page for the appropriate delivery mode.

### When to set the voicemail contact attributes
The voicemail system was designed to allow customers to interact with it as they would most other voicemail systems, allowing them to simply hang up when they have left their message instead of waiting for a tone or message. As such, it is best to set these attributes just before you begin recording the customer voice. You should not, however, set them too early as the customer could change their mind and just hang up before leaving a message, leading to errors in code execution. Technically speaking, the only attribute that should not be set until the customer is getting ready to record is the `vm_flag` attribute, since it is the ket that triggers the entire voicemail process. The example contact flow provided with the installation, VMXCoreFlow-InstanceName, shows the `vm_flag` attribute being set just after media streaming begins, with the other attributes being set in a prior flow.

## Recording the customer audio
The voicemail system uses the Kinesis Vide Streams integration of Amazon Connect to capture the customer audio. Since we are trying to capture the customer audio for a voicemail, when no other parties should be on the phone, we are only expecting audio from the customer in the stream. When configuring your contact flow, please follow the example provided in VMXCoreFlow-InstanceName and **only initialize** the audio `From the customer`. If you select only `To the customer`, you will not get the customer's voicemail at all. If you select both options, the audio will be garbled.

## Setting the max voicemail time
By default, the max voicemail length is 1 minute. If you want to increase or decrease this, you will need to change the timeout on the **Get customer input** block in the VMXCoreFlow-InstanceName contact flow (or whichever custom flow you are using to capture voicemails). If you are INCREASING this number, you may also want to edit the Kinesis trigger on your VMXKVStoS3 function, reducing the batch size. This is important because the audio capture from KVS does take a little bit of time and since all Lambda functions have a 15 minute timeout, you could run into an issue.

## Additional Notes
1.  **Calls in Queue**; If you are providing the voicemail option after you have already queued the call, be aware that the voicemail process can be completely interrupted if an agent in the assigned queue becomes available. While connecting a caller to an agent is not a bad thing, there are a few things to consider:
  1.  The caller will suddenly switch from leaving a voicemail to hearing a whisper flow (if configured), then connect to an agent. They may not understand what is happening and hang up.
  2.  If the call connects while the customer was leaving the voicemail, the CTR still likely contains the vm_flag setting to 1. This means that the voicemail system will still do the voicemail process and, most likely, will transcribe the entire conversation from the customer's perspective. To correct this,  part of the customer or agent whisper should be to check for the presence of the flag and, if it exists, set it to 0.
  3.  If you are going to use KVS for realtime transcription in service cloud voice, and you initialize this during the agent whisper flow, you would need to also stop streaming and restart so that you have both sides of the conversation.
