# Installing Voicemail Express
This document will walk you through the steps required to deploy the Voicemail Express solution to your AWS account. This solution was specifically designed to operate in a Service Cloud Voice created AWS account, but will work the same in a standarad Salesforce + Amazon Connect CTI Adapter configuration.

In order to deploy this template, you must first complete the [installation prerequisites](docs/vmx_prerequistes.md). Once those are complete, you can continue with the process below.

**Note:** You will need to save information to a notepad during the entire setup process. 

## Gather Required Information
The Voicemail Express solutions Uses AWS CloudFormation to deploy most of the solution. In order to launch the template, you will need the following information:
- ARN for the AWSSCV Common Layers - Node layer from the [Lambda console](https://console.aws.amazon.com/lambda/home)
- ARN for the AWSSCV Common Layers - Python layer from the [Lambda console](https://console.aws.amazon.com/lambda/home)
- ARN for the Amazon Kiesis data stream used for streaming your CTRs from the [Amazon Kinesis Data streams console](https://console.aws.amazon.com/kinesis/home)
- ARN for the Salesforce Config Secrets from the [AWS Secrets Manager console](https://console.aws.amazon.com/secretsmanager/home)
- Amazon Connect Instance Alias from the [Amazon Connect console](https://console.aws.amazon.com/connect/home)
- The field names for the two fields that you created in the prerequisites

Once you have the required information, you are ready to continue with installation. 

## Delploy the Cloudformation Template
The next step is to deploy the CloudFormation template. This template builds all of the AWS resources required to make Voicemail Express work. 
1. Right-click/control-click to download the [Voicemail Express CloudFormation template](https://raw.githubusercontent.com/amazon-connect/amazon-connect-salesforce-scv/master/projects/AWSSCV-VoicemailExpress/CloudFormation/awsscv_vmx.yaml) and save it to your computer
2. Log into the [AWS console](https://console.aws.amazon.com/console/home)
3. Navigate to the [AWS CloudFormation console](https://console.aws.amazon.com/cloudformation/home)
4. Choose **Create stack**
5. In the **Specify template** section, select **Upload a Template file**
6. Select **Choose file**
7. Navigate to the **scv_vmx.yaml** file that you downloaded previously and choose **Open**
8. Wait a moment for the S3 URL to update, then select **Next**
9. Provide a name for the stack, such as `AWSSCV-VoicemailExpresss`
10. **Complete the parameters** using the information that you have gathered. 
  - AWSRegion: select the region that you deployed your Amazon Connect instance to
  - AWSSalesforceCommonNodeLayer: The full ARN for your SCV Common Node layer
  - AWSSalesforceCommonPythonLayer: The full ARN for your SCV Common Python layer
  - ConnectCTRStreamARN: The full ARN for the Kinesis data stream that streams your CTRs (Contact Trace Records) from Amazon Connect
  - ConnectInstanceName: The instance alias or directory name for your Amazon Connect Instance
  - RecordingsExpireInDays: The number of days before the voicemails are deleted and the presigned URLs expire
  - sfDeploymentType: Indicate whether is is a Service Cloud Voice or CTI Adapter deployment
  - sfHost: The full https:// URL to of your Salesforce org. It **must** include https://
  - sfProduction: Is this a production org
  - sfSecrets: The full ARN for your Salesforce Access secrets
  - sfVersion: Your Salesforce API version
  - sfVoicemailField: The custom field that was created to store the voicemail transcript
  - sfVoicemailPhoneField: The custom field that was created to store the voicemail customer callback number
11. Once the parameters are complete, choose **Next**
  - **NOTE:** In Service Cloud Voice deployments, it is normal to see a warning on the next page, Configure stack options
12.	Scroll to the bottom and select **Next**
13.	Scroll to the bottom, select the box to **acknoledge that IAM resources will be created**
14. Select **Create Stack**
15. The deployemnt will take 8 - 10 minutes. Once the Stack shows **CREATE_COMPLETE**, you are ready to proceed. Remain in the CloudFormation console.

## Configure the Triggers
Now that the resources are deployed, we need to configure some triggers. These triggers move the voicemail process along as each step is completed.
1. While in the Stack details, select **Reources**
2. Find the Lambda function with the Logical ID **scvvmxkvstos3**
3. **Select the link** in the Physical ID column to open that resource in a new tab and switch to that tab.
4. In the Designer section of the Lambda function, select **+ Add trigger**
5. In the Trigger configuration, **select Kinesis**
6. In the Kinsis stream drowpdown, select the Kinesis data stream for your CTRs
7. Change **Batch size to 10**
9. Leave all other values to their defaults and select **Add**
10. The trigger will save, close the browser tab and return to the CloudFormation tab
11. Find the S3 bucket with the Logical ID **scvvmxs3recordingsbucket**
12. **Select the link** in the Physical ID column to open that resource in a new tab and switch to that tab.
13. In the S3 Bucket detail page, select the **Properties** tab
14. In the Advanced settings section, select **Events**
15. Select **+ Add notification**
16. In the **Name** field, enter `SendToTranscriber`
17. In the Events section, select **PUT**
18. In the Suffix field, enter `.wav`
19. Drop down the **Send to** menu and choose **Lambda Function**
20. In the **Lambda** menu, select the function that begins with **scv_vmx_transcriber**
21. Select **Save**, close the browser tab and return to the CloudFormation tab
22. Find the S3 bucket with the Logical ID **scvvmxs3transcriptsbucket**
23. **Select the link** in the Physical ID column to open that resource in a new tab and switch to that tab.
24. In the S3 Bucket detail page, select the **Properties** tab
25. In the Advanced settings section, select **Events**
26. Select **+ Add notification**
27. In the **Name** field, enter `SendToPackager`
28. In the Events section, select **PUT**
29. In the Suffix field, enter `.json`
30. Drop down the **Send to** menu and choose **Lambda Function**
31. In the **Lambda** menu, select the function that begins with **scv_vmx_packager**
32. Select **Save**, close the browser tab and return to the CloudFormation tab

## Install the baseline Contact Flows
In order to test Voicemail Express, you will need to import two contact flows into your Amazon Connect instance. The first flow provides an example of how the voicemail system functions and ccan be triggered from any normal inbound contact flow. The second flow is the test contact flow. This allows you to test the voicemail system without going through normal call processing in your main flows. 
1. Right-click/control-click to download [001-VMX-Sample VM-SCV contact flow](https://raw.githubusercontent.com/amazon-connect/amazon-connect-salesforce-scv/master/projects/AWSSCV-VoicemailExpress/ContactFlows/001-VMX-SampleVM-SCV) and save it to your computer
2. Right-click/control-click to download [001-VMX-Test Function-SCV contact flow](https://raw.githubusercontent.com/amazon-connect/amazon-connect-salesforce-scv/master/projects/AWSSCV-VoicemailExpress/ContactFlows/001-VMX-TestFunction-SCV) and save it to your computer
3. Login to your Amazon Connect Administrative UI
4. Navigate to **Routing**, and select **Contact flows**
5. Select **Create contact flow**
6. In the upper right of the contact flow editor, select the **down arrow** to the right of the greyed out Save button
7. Select **Import flow (beta)**
8. Choose **Select**
9. Browse to the location that you downloaded the contact flows to, and select **001-VMX-SampleVM-SCV**
10. Choose **Import**
11. Once the contact flow is visible in the editor, select **Publish**, then select **Publish** again on the popup window
12. Once the contact flow refreshes, it has been saved and you can proceed to the next step.
13. Navigate to **Routing**, and select **Contact flows**
14. Select **Create contact flow**
15. In the upper right of the contact flow editor, select the **down arrow** to the right of the greyed out Save button
16. Select **Import flow (beta)**
17. Choose **Select**
18. Browse to the location that you downloaded the contact flows to, and select **001-VMX-TestFunction-SCV**
19. Choose **Import**
11. Once the contact flow is visible in the editor, find the **Set working queue** block that is currently set to transfer to an agent. Double-click the header  to edit the properties
12. **Remove the existing agent**, and **select an agent** that exists in your instance, then choose **save**
13. Find the **Set working queue** block that is currently set to transfer to a queue. Double-click the header to edit the properties
14. **Remove the existing queue**, and **select a queue** that exists in your instance, then choose **save**
15. Find the **Transfer to flow** block and double clil the header to edit the properties
16. **Remove the existing flow**, and select **001-VMX-SampleVM-SCV** from the dropdown list, then choose **save**
17. Select **Publish**, then select **Publish** again on the popup window
18. Navigate to **Routing**, and select **Phone numbers**
19. Select **Claim a number**
20. Select **DID (Direct Inward Dialing)** and then **set the country** as appropriate
21. Select the desired phone number
22. In the **Description**, enter `Voicemail Test Line`
23. Form the ***Contact flow / IVR*** list, select **001-VMX-TestFunction-SCV**
24. Select **Save**
25. After ~2 minutes, your configuration will be ready to test.

## Test Voicemail
Now that the solution has been deployed, you are ready to test. 
1. **Dial** the phone number you configured for the Voicemail Test Line
2. At the main menu, **press 2** to leave a voicemail for a queue
3. When you hear the beep, **record your voicemail**. Hang up at any time after recording a message.
4. Once you have completed the recording, **wait approximately 2 minutes**.
5. **Login to the Salesforce Lightning Experience**, and open the Service Console
6. Navigate to **Cases**
7. View **all cases**
8. Sort by Case number, descending
9. After a couple minutes, you should see a new case with the subject Queue voicemail for: YOURQUEUE, from: YOURPHONE
10. **Open the case** and observe:
  - The transcript in the description field
  - A Play Voicemail link in the Voicemail link field
  - A phone number in the Callback Phone field
  
**Voicemail Validation is complete!**
