# AWS SCV Launch Pack Installation


## Install and Setup Prerequisites
Make sure to complete all prerequisites before continuing.
* [Prerequisites](launchpack_prerequisites.md)

A number of parameters are required to install the AWS SCV Launch Pack.  Specific instructions on obtaining appropriate
values for these parameters may be found in the setup instructions of the individual projects below:

* [AWSSCV-CommonLayers](../../Common/AWSSCV-CommonLayers/readme.md)
* [AWSSCV-SalesforceConfig](../../Common/AWSSCV-SalesforceConfig/readme.md)
* [AWSSCV-VoicemailExpress](../../Solutions/AWSSCV-VoicemailExpress/readme.md)
* [AWSSCV-SampleContactFlows](../../Examples/AWSSCV-SampleContactFlows/readme.md)
* [AWSSCV-CTRLogger](../../Solutions/AWSSCV-CTRLogger/readme.md)
* [AWSSCV-DashboardAlarms](../../Solutions/AWSSCV-DashboardAlarms/readme.md)

## Gather required parameters
Gather the parameters listed below before starting the CloudFormation stack deployment.  The system from which to obtain the parameter is called out next to the parameter name.

### AWS
* **AWS Region** (us-east-1, us-west-2, ap-southeast-1, ap-southeast-2, ap-northeast-1, eu-central-1, eu-west-2)
* **AWS S3 Bucket Prefix** (not required, only used for development)
* **AWS Lambda Logging Level** (INFO, DEBUG)

### Amazon Connect
* **Amazon Connect Instance Name** (Amazon Connect)
* **Amazon Connect Instance Id** (Amazon Connect)
* **Amazon Connect CTR Stream ARN** (Amazon Kinesis Data Stream)
* **Amazon Connect Basic Queue ARN** (Amazon Connect)
* **Service Cloud Voice Invoke Telephony Function ARN** (AWS Lambda)
* **Service Cloud Voice Invoke Salesforce Rest API Function ARN** (AWS Lambda)
* **Service Cloud Voice KVS Consumer Trigger Function ARN** (AWS Lambda)

### Salesforce
* **Salesforce Org Id** (Salesforce Setup - Company Information)
* **Salesforce Host** (Salesforce Setup - My Domain)
* **Salesforce API Username** (Salesforce Setup - Users)
* **Salesforce API Version** (Salesforce Setup - Apex)
* **Salesforce Mode** (PROD, DEV, SANDBOX)
* **Salesforce Deployment Type** (CTI, SCV)
* **Salesforce Connected App Consumer Key** (Salesforce Setup - Connect Apps)
* **Salesforce Connected App Private Key** (Base64 encoded private key)
* **Salesforce Chatter Feed Id** (Salesforce - Chatter)

### Voicemail Express
- **Recordings Expire in Days**
- **Salesforce Voicemail Link Field** (Salesforce Setup - Case Object)
- **Salesforce Voicemail Phone Field** (Salesforce Setup - Case Object)
- **Salesforce Voicemail Contact Attributes Field** (Salesforce Setup - Case Object)

### Sample Contact Flows
* **Install Sample Contact Flows** (true, false)

### CTR Logger
* **CTR Logger Format Events** (true, false)
* **CTR Logger Write Events To** (console, S3, both)

### Dashboard Alarms
* **Cloudwatch Dashboard Name** (User entered value)


# Delploy the Cloudformation Template
The next step is to deploy the CloudFormation template. This template builds all of the AWS resources required to make Voicemail Express work.
1. Right-click/control-click to download the [Launch Pack CloudFormation template](../CloudFormation/awsscv_launch_pack.yaml) and save it to your computer
2. Log into the [AWS console](https://console.aws.amazon.com/console/home)
3. Navigate to the [AWS CloudFormation console](https://console.aws.amazon.com/cloudformation/home)
4. Choose **Create stack**
5. In the **Specify template** section, select **Upload a Template file**
6. Select **Choose file**
7. Navigate to the **awsscv_launch_pack.yaml** file that you downloaded previously and choose **Open**
8. Wait a moment for the S3 URL to update, then select **Next**
9. Provide a name for the stack, such as `AWSSCV-LaunchPack`
10. **Complete the parameters** using the information that you have gathered.
11. Once the parameters are complete, choose **Next**
- **NOTE:** In Service Cloud Voice deployments, it is normal to see a warning on the next page, Configure stack options
12.	Scroll to the bottom and select **Next**
13.	Scroll to the bottom, select the box to **acknowledge that IAM resources will be created**
14. Select **Create Stack**
15. The deployment will take 8 - 10 minutes. Once the Stack shows **CREATE_COMPLETE**, you are ready to proceed. Remain in the CloudFormation console.
