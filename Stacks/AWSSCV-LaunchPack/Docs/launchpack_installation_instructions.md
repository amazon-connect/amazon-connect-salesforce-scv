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
### AWS
* AWS Region
* AWS S3 Bucket Prefix
* AWS Lambda Logging Level

### Amazon Connect
* Amazon Connect Instance Name
* Amazon Connect Instance Id
* Amazon Connect CTR Stream ARN
* Amazon Connect Basic Queue ARN
* Service Cloud Voice Invoke Telephony Function ARN
* Service Cloud Voice Invoke Salesforce Rest API Function ARN
* Service Cloud Voice KVS Consumer Trigger Function ARN

### Salesforce
* Salesforce Org Id
* Salesforce Host
* Salesforce API Username
* Salesforce API Version
* Salesforce Mode
* Salesforce Deployment Type
* Salesforce Connected App Consumer Key
* Salesforce Connected App Private Key
* Salesforce Chatter Feed Id

### Voicemail Express
- Recordings Expire in Days
- Salesforce Voicemail Link Field
- Salesforce Voicemail Phone Field
- Salesforce Voicemail Contact Attributes Field

### Sample Contact Flows
* Install Sample Contact Flows

### CTR Logger
* CTR Logger Format Events
* CTR Logger Write Events To

### Dashboard Alarms
* Cloudwatch Dashboard Name


# Delploy the Cloudformation Template
The next step is to deploy the CloudFormation template. This template builds all of the AWS resources required to make Voicemail Express work.
1. Right-click/control-click to download the [Voicemail Express CloudFormation template](https://raw.githubusercontent.com/amazon-connect/amazon-connect-salesforce-scv/master/Solutions/AWSSCV-VoicemailExpress/CloudFormation/awsscv_vmx.yaml) and save it to your computer
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
