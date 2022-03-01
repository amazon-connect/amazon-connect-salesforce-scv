# Using the Custom Delivery Option
The VMXPackager Lambda function includes the option to use your own delivery model, allowing you to save voicemails to whatever you want. When the packager gets to the point where it writes the voicemail record, it invokes your custom code and proceeds normally. This provides flexibility in the deployment model.

## Create Your Custom Delivery Function
In the VMXPackager function, there are multiple sub functions that deliver the voicemails using the appropriate model. These functions are included as saperate files, embedded with the Lambda package. You can modify the **sub_other.py** file to write the voicemail to whatever you like.

When VMXPackager invokes the **sub_other.py** file, it passes along collected data as `writer_payload`. Below is an example of what can be included:
```
{
   "instance_id":"%YOUR_INSTANCE_ID%",
   "contact_id":"%THIS_CONTACT_ID%",
   "queue_id":"%THIS_QUEUE_ID%",
   "loop_counter":1,
   "entity_type":"queue",
   "json_attributes":{
      "vm_core_flow":"arn:aws:connect:us-east-1:%YOUR_ACCOUNT%:instance/%YOUR_INSTANCE%/contact-flow/%YOUR_CORE_FLOW%",
      "vm_mode":"other",
      "vm_from":"+15555551212",
      "vm_lang":"en-US",
      "vm_test_agent":"jsmith",
      "vm_queue_arn":"arn:aws:connect:us-east-1:%YOUR_ACCOUNT%:instance/%YOUR_INSTANCE%/queue/6c1bcc74-1bed-4edd-9f03-05a8f1ba5e82",
      "vm_flag":"1",
      "vm_test_queue":"arn:aws:connect:us-east-1:%YOUR_ACCOUNT%:instance/%YOUR_INSTANCE%/queue/6c1bcc74-1bed-4edd-9f03-05a8f1ba5e82",
      "entity_name":"BasicQueue",
      "entity_id":"arn:aws:connect:us-east-1:%YOUR_ACCOUNT%:instance/%YOUR_INSTANCE%/queue/6c1bcc74-1bed-4edd-9f03-05a8f1ba5e82",
      "entity_description":"A simple, basic voice queue. QVMB::test_to@example.com",
      "transcript_contents":"This is a test voicemail on March 1st. At 11:47 a.m.",
      "callback_number":"+15555551212",
      "presigned_url":"https://RECORDINGSBUCKET.s3.amazonaws.com/c64a88e5-5eba-43ce-b694-e83861900775.wav?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAW5VSGOPHDEYJOR2P%2F20220301%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20220301T194857Z&X-Amz-Expires=345600&X-Amz-SignedHeaders=host&X-Amz-Signature=SIGNTUREDATA"
   }
}
```
The **sub_other.py** file includes the code to log the incoming data in the `writer_payload` if the Lambda function logging level is set to DEBUG.
`logger.debug(writer_payload)`
This is helpful as it allows you to get an idea of what data is coming to your function from the VMXPackager.

What is done in this function is entirely up to you. The only functional requirement is that the **sub_other.py*** function returns either a `success` or `fail` so that the VMXPackager function knows the outcome of the write. This has been coded into the sample file already. 
