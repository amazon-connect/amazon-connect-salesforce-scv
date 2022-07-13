### AWS and Amazon Connect Configuration

These AWS and Amazon Connect configurations will enable triggering out-of-the-box InvokeSalesforceRestApiFunction Lambda function to update custom field in Salesforce Voice Call Object whenever Contact Lens real-time rule is matched.

**Important Notes**:

1. The features and capabilities of this solution/example may be incorporated or replicated in future releases of Service Cloud Voice
2. The code for this example is for non-production use only

### CloudFormation Template

This CloudFormation template will create:

1. EventBridge Rule: This rule is triggered by Amazon Connect when Contact Lens real-time rule matches
2. scv_cl_rt_nba lambda function: This lambda function is triggered by EventBridge rule set for Contact Lens real-time. This function updates custom field called "Current_Call_Category\_\_c" in Salesforce Voice Call Object, using InvokeSalesforceRestApiFunction lambda function

**Steps**

1. Click on [CL NBA CloudFormation](/Examples/AWSSCV-ContactLens-RealTime-NextBestAction/CloudFormation/awsscv_real_time_cl_nba.yaml) and save file named awsscv_real_time_nba.yaml
2. In a new browser tab, login to the AWS Console (https://console.aws.amazon.com/console/home)
3. Make sure you are in the same region as your Amazon Connect instance. You can set the region by expanding the region
   selector in the upper right and choosing the region
4. Navigate to the CloudFormation console
5. Select Create Stack, and choose With new resources (standard)
6. In the Specify Template section, choose Upload a template file
7. Select Choose file
8. Navigate to the folder where you saved awsscv_real_time_nba.yaml
9. Select Next
10. In the Stack Name field, enter awsscv-nba-example
11. Enter the parameters as follows:

- AWSRegion: enter the region where your Amazon Connect Instance is running
- AmazonConnectInstanceARN: enter Amazon Connect instance ARN, ref - https://docs.aws.amazon.com/connect/latest/adminguide/find-instance-arn.html
- EXPDevBucketPrefix: _leave it blank_
- EXPTemplateVersion: _2022-06-06_ (pre-filled)
- InvokeSalesforceRestApiFunction: ARN of out-of-the-box SCV Lambda function InvokeSalesforceRestApiFunction
- LambdaLoggingLevel : INFO

12. Select Next
13. Scroll to the bottom and select Next
14. Scroll to the bottom and select Create Stack
15. After a minute or two, the stack should complete

_Note - please ensure that InvokeSalesforceRestApiFunction lambda function is setup properly and working, more information on setup - https://developer.salesforce.com/docs/atlas.en-us.voice_developer_guide.meta/voice_developer_guide/voice_lambda_invokesalesforcerestapi.htm_

### Setup Contact Lens real-time rules

Contact Lens real-time rules can be matched based on one or more conversation characteristics such as specific spoken phrases, sentiment, contact attributes etc.

For reference : https://docs.aws.amazon.com/connect/latest/adminguide/build-rules-for-contact-lens.html

**Steps**

1. Logon to your Amazon Connect Instance
2. On the navigation menu, choose Rules
3. Select Create a rule, Contact Lens
4. Select When as A Contact Lens real-time analysis is available
5. Assign a name to the rule as **welcome**
6. Under When, use the dropdown list to choose real-time analysis
7. Choose Add condition as **Words or phrases - Exact match**
8. In Logic section choose the following:

- Any of the following words or phrases **were mentioned** during the **entire** length of the contact where speaker is **either** customer or agent speaking **English**

9. In Keywords and Phrases add the following:

- welcome
- hello
- hi there
- greetings

10. Click Next
11. Give Category name same as rule name
12. Add action as EventBridge event
13. Give Action name as same as rule name
14. Click Next and then Save and Publish

15. follow steps 3 to 14, except step 9, to setup Contact Lens rule named **sales** (change the name to sales in step 5) with following Keywords and Phrases:

- I want buy
- what is the new version of the product
- new product
- upgrade

Now, we will setup sentiment based Contact Lens real-time rule

16. Follow steps 3 to 6 to create Contact Lens rule named **retain** (change the name to retain in step 5)
17. Choose Add condition as **Sentiment - Time period**
18. Set up condition for average sentiment as per following:

- **Customer** sentiment was **negative** during the past **10** **seconds** of the contact

19. follow steps 10 to 14

### Amazon Connect Contact Flow Configurations

Salesforce provides set of example Contact Flows with Service Cloud Voice setup. For this exercise we are going to using one of these out-of-the-box Contact Flow called **Sample SCV Inbound Flow with Transcription using Contact Lens**

**Steps**

1. Go to Amazon Connect Admin console
2. Click on View phone numbers
3. Click on a phone number you have claimed
4. Add appropriate description such as Contact Flow to test Contact Lens
5. From Contact flow / IVR dropdown, select Contact Flow - **Sample SCV Inbound Flow with Transcription using Contact Lens**
6. Click Save

**Next** - [Salesforce Configurations](deployment_salesforce.md)
