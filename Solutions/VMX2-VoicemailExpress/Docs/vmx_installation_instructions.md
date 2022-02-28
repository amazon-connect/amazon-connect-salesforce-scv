# Installing Voicemail Express
This document will walk you through the steps required to deploy the Voicemail Express solution to your AWS account. This solution was specifically designed to operate in a number of different deployment scenarios, including Service Cloud Voice.

In order to deploy this template, you must first complete the [installation prerequisites](vmx_prerequistes.md). Once those are complete, you can continue with the process below.

**Note:** You will need to save information to a notepad during the entire setup process.

## Gather Required Information
The Voicemail Express solutions Uses AWS CloudFormation to deploy the solution. In order to launch the template, you will need the following information:
- ARN for the Amazon Kinesis data stream used for streaming your CTRs from the [Amazon Kinesis Data streams console](https://console.aws.amazon.com/kinesis/home)
- Amazon Connect Instance Alias from the [Amazon Connect console](https://console.aws.amazon.com/connect/home)
- Amazon Connect Instance ARN from the [Amazon Connect console](https://console.aws.amazon.com/connect/home)
- (SALESFORCE MODES ONLY) ARN for the Salesforce Config Secrets from the [AWS Secrets Manager console](https://console.aws.amazon.com/secretsmanager/home)
- (SALESFORCE MODES ONLY) The object and field names for the custom objects/fields that you created in the prerequisites
- Default agent ID to use for the test function
- Default Queue ARN to use for the test function
- (EMAIL MODE ONLY) Default email address to send voicemails FROM
- (EMAIL MODE ONLY) Default email address to send voicemails TO

Once you have the required information, you are ready to continue with installation.

## Delploy the Cloudformation Template
The next step is to deploy the CloudFormation template. This template builds all of the AWS resources required to make Voicemail Express work.
1.  Right-click/control-click to download the [Voicemail Express CloudFormation template](../CloudFormation/vmx.yaml) and save it to your computer
2.  Log into the [AWS console](https://console.aws.amazon.com/console/home)
3.  Navigate to the [AWS CloudFormation console](https://console.aws.amazon.com/cloudformation/home)
4.  Choose **Create stack**
5.  In the **Specify template** section, select **Upload a Template file**
6.  Select **Choose file**
7.  Navigate to the **vmx.yaml** file that you downloaded previously and choose **Open**
8.  Wait a moment for the S3 URL to update, then select **Next**
9.  Provide a name for the stack, such as `VMX-MyInstanceName`
10. **Complete the parameters** using the information that you have gathered.
  - **NOTE:** Section 1 is required for all deployments. Sections 2 & 3 are used for specific deployment models. You only need to complete the sections that apply to your selected deployment modes.
11. Once the parameters are complete, choose **Next**
  - **NOTE:** In Service Cloud Voice bundle deployments, it is normal to see a warning on the next page, Configure stack options
12.	Scroll to the bottom and select **Next**
13.	Scroll to the bottom, select the boxes to **acknowledge that IAM resources will be created**
14. Select **Create Stack**
15. The deployment will take 5-10 minutes. During this time, multiple nested stacks will be deployed. Once the main stack shows **CREATE_COMPLETE**, you are ready to proceed.

## Assign a test number
1.  Login to the Amazon Connect administration interface
2.  Select **Routing** from the navigation menu, then choose **Phone numbers**
2.  Either select an existing number, or claim a new number
3.  Set the contact flow for the number to either **VMXAWSTestFlow-YOURINSTANCE** for AWS delivery modes or **VMXSFDCTestFlow-YOURINSTANCE** for Salesforce delivery modes.
4.  Select **Save**
5.  After ~2 minutes, your configuration will be ready to test.

## Test Voicemail
Now that the solution has been deployed, you are ready to test.
1.  **Dial** the phone number you configured for the Voicemail Test Line
2.  At the main menu, choose the option that matches the delivery mode that you wish to test.
3.  At the next menu, **press 1** to leave a voicemail for an agent or **press 2** to leave a voicemail for a queue
4.  When you hear the tone, **record your voicemail**. Hang up at any time after recording a message.
5.  Once you have completed the recording, **wait approximately 2 minutes**.
6.  For Amazon Connect Tasks, log the appropriate agent in and put them into the available state. The Task should arrive shortly. For email, the email should be delivered to the box provided. For Salesforce models, log into Salesforce and navigate the new cases or custom object records to see the voicemail.

**Voicemail Validation is complete!**

Once Voicemail Express has been deployed and tested successfully, you can learn more about the different modes by referencing the following documents:
1. [High-level overview of the Voicemail Express solution](Docs/vmx_core.md)
2. [Delivering Voicemails as Amazon Connect Tasks](Docs/vmx_tasks.md)
3. [Delivering Voicemails via Amazon Simple Email Service](Docs/vmx_email.md)
4. [Delivering Voicemails as Salesforce Cases](Docs/vmx_sfcase.md)
5. [Delivering Voicemails as Salesforce Custom Objects](Docs/vmx_sfcustom.md)
6. [Creating your own custom delivery mode for Voicemails](Docs/vmx_custom.md)
