# Installing Dashboard Alarms
This document will walk you through the steps required to deploy the Dashboard Alarms solution to your AWS account. This solution was specifically designed to operate in a Service Cloud Voice created AWS account, but will work the same in a standard Salesforce + Amazon Connect CTI Adapter configuration.

In order to deploy this template, you must first complete the [installation prerequisites](dashboard_alarms_prerequisites.md). Once those are complete, you can continue with the process below.

**Note:** You will need to save information to a notepad during the entire setup process.

## Gather Required Information
The Dashboard Alarms solution Uses AWS CloudFormation to deploy the solution. In order to launch the template, you will need the following information:
- ARN for the AWSSCV Common Layers - Python layer from the [Lambda console](https://console.aws.amazon.com/lambda/home)
- ARN for the Amazon Kiesis data stream used for streaming your CTRs from the [Amazon Kinesis Data streams console](https://console.aws.amazon.com/kinesis/home)
- ARN for the Salesforce Config Secrets from the [AWS Secrets Manager console](https://console.aws.amazon.com/secretsmanager/home)
- Amazon Connect Instance Alias from the [Amazon Connect console](https://console.aws.amazon.com/connect/home)

Once you have the required information, you are ready to continue with installation.

## Delploy the Cloudformation Template
The next step is to deploy the CloudFormation template. This template builds all of the AWS resources required to make Voicemail Express work.
1. Right-click/control-click to download the [Voicemail Express CloudFormation template](https://raw.githubusercontent.com/amazon-connect/amazon-connect-salesforce-scv/master/Solutions/AWSSCV-DashboardAlarms/CloudFormation/awsscv_connect_dashboard_alarms.yaml) and save it to your computer. 
2. Log into the [AWS console](https://console.aws.amazon.com/console/home)
3. Navigate to the [AWS CloudFormation console](https://console.aws.amazon.com/cloudformation/home)
4. Choose **Create stack**
5. In the **Specify template** section, select **Upload a Template file**
6. Select **Choose file**
7. Navigate to the **awsscv_vmx.yaml** file that you downloaded previously and choose **Open**
8. Wait a moment for the S3 URL to update, then select **Next**
9. Provide a name for the stack, such as `AWSSCV-DashboardAlarms`
10. **Complete the parameters** using the information that you have gathered.
>Environment
- AWSRegion: select the region that you deployed your Amazon Connect instance to
- AWSSCVCommonRole: The full ARN for your awsscv_common_role role
- AWSSalesforceCommonPythonLayer: The full ARN for your SCV Common Python layer
- ConnectInstanceId: The instance id of your Amazon Connect instance
- SalesforceConfig: The full ARN of your Salesforce Access secret
- SalesfordeOrgId: The org id of your Salesforce org
- SalesforceChatterFeedId: The chatter feed id in your Salesforce org that will receive alarm messages
- DashboardName: The dashboard name
  
> Concurrent Calls Alarm
- ConcurrentCallsPeriod: Data evaluation period in seconds
- ConcurrentCallsEvaluationPeriods: Group size of data evaluation periods
- ConcurrentCallsThreshold: Limit above which alarms are raised

> Concurrent Calls Percentage Alarm
- ConcurrentCallsPercentagePeriod: Data evaluation period in seconds
- ConcurrentCallsPercentageEvaluationPeriods: Group size of data evaluation periods
- ConcurrentCallsPercentageThreshold: Limit above which alarms are raised

> Throttled Calls Percentage Alarm
- ThrottledCallsPeriod: Data evaluation period in seconds
- ThrottledCallsEvaluationPeriods: Group size of data evaluation periods
- ThrottledCallsThreshold: Limit above which alarms are raised

> Misconfigured Phone Numbers Alarm
- MisconfiguredPhoneNumbersPeriod: Data evaluation period in seconds
- MisconfiguredPhoneNumbersEvaluationPeriods: Group size of data evaluation periods
- MisconfiguredPhoneNumbersThreshold: Limit above which alarms are raised

> Missed Calls Calls Alarm
- MissedCallsPeriod: Data evaluation period in seconds
- MissedCallsEvaluationPeriods: Group size of data evaluation periods
- MissedCallsThreshold: Limit above which alarms are raised

> Contact Flow Alarms
- ContactFlowName
- ContactFlowFatalErrorsPeriod
- ContactFlowFatalErrorsEvaluationPeriods
- ContactFlowFatalErrorsThreshold

11. Once the parameters are complete, choose **Next**
- **NOTE:** In Service Cloud Voice deployments, it is normal to see a warning on the next page, Configure stack options
12.	Scroll to the bottom and select **Next**
13.	Scroll to the bottom, select the box to **acknowledge that IAM resources will be created**
14. Select **Create Stack**
15. The deployemnt will take 2 -3. Once the Stack shows **CREATE_COMPLETE**, you are ready to proceed. Remain in the CloudFormation console.

**Dashboard Alarms installation is complete!**
