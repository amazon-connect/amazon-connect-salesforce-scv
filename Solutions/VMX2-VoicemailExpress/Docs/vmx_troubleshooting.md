# Troubleshooting Voicemail Express
Below are some common problems customers have encountered with the appropriate resolution.

## General troubleshooting tips
-  If you are experiencing issues, set the logging level of the Lambda functions to DEBUG. You can change this setting by going to the 4 core functions (VMXKVStoS3, VMXTranscriber, VMXPackager, VMXPresigner) and changing the Environment Variable for **lambda_logging_level** to `DEBUG`. This will provide the most detail.
-  The flow of events, at a high level, is:
    -  CTR is emitted
    -  VMXKVStoS3 function
    -  VMXTranscriber function
    -  VMXPackager function
    -  VMXPresigner function (VMXPacakger calls this function)
-  Begin troubleshooting at the VMXKVStoS3 function. Check the CloudWatch logs to see if the function succeeded and that the file was created and placed in S3
-  Once you validate that the file was created, look to see if there were any errors in the VMXTranscriber function. Depending on how closely you are monitoring progression, you can also look in the Transcribe console to see if the Transcription process is still running, completed, or returned an error.

## General Issues
### The voicemail audio is garbled when I play it back
Voicemail Express uses the Amazon Kinesis Video Stream to capture the recording. It is only expecting there to be one audio stream, from the customer, when it begins recording. If you have selected both **From the customer** and **To the customer** when initializing your KVS stream in your contact flow, the VMXKVStoS3 function will attempt to mix the two channels together, causing garbled audio. Make sure that you are only enabling the **From the customer** option when starting streaming.

### I am not getting any voicemails, regardless of delivery model
Make sure that you are setting the **vm_flag** value to `1` in your contact flows. This must be set in order for the VMXKVStoS3 function to know that it should process this record as a voicemail.

## Email Delivery Issues
### I see no errors, but email is not being delivered
1.  Validate that the email addresses or domain have been validated in SES
2.  For agent voicemails, validate that the agent ID is their email address
3.  For queue voicemails, validate that you have added the **QVMB::** prefix to the email address and included this in the queue description.
4.  If you are using a custom template, make sure all variables referenced in the template exist as contact attributes on the call

## Salesforce Case Issues
### I see a login error in the VMXPackager Lambda log
-  Validate that your Salesforce Config is setup correctly. You can do this by testing the AWSSCV_salesforce_validator function.

### I see no errors, but I do not see the case in the Cases view
-  Make sure that you are viewing **All cases** instead of **Recently viewed**
