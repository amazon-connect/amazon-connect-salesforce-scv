#Call Categorisation (using Contact Lens Post Call Analysis)

Call Categorisation example uses Amazon Connect Contact Lens to identify call categories based on the conversation between agent and the customer. This capability is for a use case where customer wants to automatically categorise calls based on the business rules. Also, customer wants to know overall sentiment of the call from the caller and the agent perspective.

High level call flow:

1. User sets up business rules for call categorisation using Amazon Connect console
2. User enables Contact Lens Post Call analysis\* within Contact Flow
3. Customer calls and converser with the agent
4. Once the call is over, based on call recording Contact Lens generates post call analysis which includes call categories (based on Rules) and overall sentiment, along with other information
5. The lambda function provided inserts the call categories and overall sentiment to corresponding Voice Call Object in Salesforce

High Level Architecture

Following high level architecture diagram shows the all the components involved as well as the flow.

1. Caller places a call on Amazon Connect phone number
2. Once the call lands on Amazon Connect, associated contact flow is triggered which has Contact Lens post call analysis enabled
3. Call gets transferred to Salesforce Omni Channel agent interface, and agent answers the call
4. Conversation between the agent and the caller takes place
5. Once the call is completed, Contact Lens analyses the call and put the analysis in pre-defined S3 bucket (same bucket which used for call recording as well)
6. Once the analysis is in the S3 bucket, the Lambda function is triggered
7. The Lambda function extracts the information from the Contact Lens analysis and inserts into pre-defined fields of Salesforce Voice call object (using out-of-the-box Telephony Integration API)

Deployment

In order to deploy this capability, following configurations need to be done in Salesforce and AWS.

_Salesforce - adding required fields in Voice Call Object_

1. Log in into your Salesforce org and go to Setup
2. In the Quick Find field type Object Manager
3. Select Object Manager from the results
4. In Object Manager find Voice Call
5. Choose Fields & Relationships
6. Select New
7. Choose Long Text Area , then select Next
8. Set a value for field label, such as Call Categories
9. Select Next
10. On the Step 3 page, select Next
11. On the step 4 page, select Save
12. When the page reloads, scroll to the new field you created and notice that it ends in \_\_c
13. Repeat steps 5 to 12 to add Overall Customer Sentiment and Overall Agent Sentiment fields with the exception of step 7 - please choose Number instead of Long Text Area

_Amazon Connect Console - configurations to enable Contact Lens post call analysis_

1. To add Rules for Contact Lens, please refer - https://docs.aws.amazon.com/connect/latest/adminguide/build-rules-for-contact-lens.html
2. To enable Contact Lens post call analysis within your Contact Flow, please refer - https://docs.aws.amazon.com/connect/latest/adminguide/enable-analytics.html

_AWS CloudFormation - created required AWS resources to enable this capability_

1. Right-click/control-click to download the AWSSCV Call Categorisation
2. In a new browser tab, login to the AWS Console (https://console.aws.amazon.com/console/home)
3. Make sure you are in the same region as your Amazon Connect instance. You can set the region by expanding the region selector in the upper right and choosing the region
4. Navigate to the CloudFormation console
5. Select Create Stack, and choose With new resources (standard)
6. In the Specify Template section, choose Upload a template file
7. Select Choose file
8. Navigate to the folder where you saved awsscv_call_categorisation.yaml
9. Select Next
10. In the Stack Name field, enter AWSSCV-Call-Categorisation
11. Enter the parameters as follows (most from your notepad):
12. _AWSRegion_: Select the region where Amazon Connect is deployed
13. _ConnectInstanceName_:Provide the instance name for Amazon Connect
14. _ContactLensS3Bucket_: Provide S3 bucket configured for storing call recording (same bucket used for storing Contact Lens post call analysis) from Amazon Connect instance configurations, refer: https://docs.aws.amazon.com/connect/latest/adminguide/update-instance-settings.html
15. _TelephonyIntegrationLambda_: ARN of out-of-the-box lambda function called InvokeTelephonyIntegrationApiFunction Lambda function
16. _LambdaLoggingLevel_: Logging level of the new Lambda function which this CloudFormation template is going to create, default is INFO
17. Select Next
18. In Service Cloud Voice deployments, it is normal to see a warning on the next page, Configure stack options
19. Scroll to the bottom and select Next
20. Scroll to the bottom and select Create Stack
21. After a minute or two, the stack should complete

Testing

Contact Lens configurations

1. From Amazon Connect configure Contact Lens post call analysis rule
2. In the rule, add keywords or phrases such as “change to next version”, “need latest model”, “upgrade”
3. In action section, configure assign contact category and name category as “upgrade”
4. Save the rule

Enable Contact Lens

1. Create new Contact Flow called “Test Contact Lens Post Call Analysis”
2. Enable post call analysis using Contact Lens in that contact flow, ref: https://docs.aws.amazon.com/connect/latest/adminguide/enable-analytics.html
3. Associate phone number with the contact flow, ref: https://docs.aws.amazon.com/connect/latest/adminguide/associate-phone-number.html
4. Place a call and get the call transfer to an agent
5. Converser with the agent and use keywords / phrases configured in the Contact Lens rule - “upgrade”, “need latest model” or “change to next version”
6. Once the call is completed, check the Details section Salesforce Voice Call object created for the call, you will find populated fields Call Categories, Overall Customer Sentiment and Overall Agent Sentiment

Conclusion

This document shows how Contact Lens post call analysis can be leveraged to categorise a call based on business rules as well as gauge the overall sentiment of the call. This capability can be easily extended to add more fields from Contact Lens post call analysis to Salesforce Voice call object. For more information on Contact Lens post call analysis output ref: https://docs.aws.amazon.com/connect/latest/adminguide/contact-lens-example-output-files.html

\*_Note -_ as of today, for additional fees Salesforce provides only post call analysis capability of Contact Lens (not real time), please talk to Salesforce team before implementing this capability.
