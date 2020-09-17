# Installing Voicemail Express
This document will walk you through the steps required to deploy the Voicemail Express solution to your AWS account. This solution was specifically designed to operate in a Service Cloud Voice created AWS account, but will work the same in a standarad Salesforce + Amazon Connect CTI Adapter configuration.

In order to deploy this template, you must first complete the [installation prerequisites](docs/vmx_prerequistes.md). Once those are complete, you can continue with the process below.

**Note:** You will need to save information to a notepad during the entire setup process. 

## Gather Required Information
The Voicemail Express solutions Uses AWS CloudFormation to deploy most of the solution. In order to launch the template, you will need the following information:
- ARN for the SCV Common Layers - Node layer from the [Lambda console](https://console.aws.amazon.com/lambda/home)
- ARN for the SCV Common Layers - Python layer from the [Lambda console](https://console.aws.amazon.com/lambda/home)
- ARN for the Amazon Kiesis data stream used for streaming your CTRs from the [Amazon Kinesis Data streams console](https://console.aws.amazon.com/kinesis/home)
- ARN for the Salesforce Access Secrets from the [AWS Secrets Manager console](https://console.aws.amazon.com/secretsmanager/home)
- Amazon Connect Instance Alias from the [Amazon Connect console](https://console.aws.amazon.com/connect/home)
- The full domain for your Salesforce org, including the https://
- Your current Salesforce API version
- The field names for the two fields that you created in the prerequisites

Once you have the required information, you are ready to continue with installation. 

## Delploy the Cloudformation Template
1. Right-click/control-click to download the [Voicemail Express CloudFormation template](../../../../../raw/master/projects/SCV-VoicemailExpress/CloudFormation/scv_vmx.yaml) and save it to your computer
2. Log into the [AWS console](https://console.aws.amazon.com/console/home)
3. Navigate to the [AWS CloudFormation console](https://console.aws.amazon.com/cloudformation/home)
4. Choose **Create stack**
5. In the **Specify template** section, select **Upload a Template file**
6. Select **Choose file**
7. Navigate to the **scv_vmx.yaml** file that you downloaded previously and choose **Open**
8. Wait a moment for the S3 URL to update, then select **Next**
9. Provide a name for the stack, such as `VoicemailExpresssSCV`
10. Complete the parameters using the information that you have gathered. 
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
