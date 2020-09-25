# Extension Routing
Extension routing provides an option to allow callers to dial a specific extension to reach a given representative.This can be useful in circumstances where continuity of the relationship is critical. The basic flow for this experience is as follows:
1. Caller selects an option to dial by extension
2. Caller enters a 4-6 digit extension, terminating with #
3. Lambda query to Salesforce to find an agent by extension
4. Lambda function to process the Salesforce response accordingly
5. Route to agent personal queue

## Deployment Resources
To enable extension dialing, we need to deploy some resources. There is a slight difference in required resources depending on deployment model (SCV vs CTI), which is noted below:
- **AWS Lambda function** to query Salesforce for the user ID (CTI deployments)
- **AWS Lambda function** to parse the REST API reponse from the default InvokeRestApi function and generate the user ID (SCV deployments)
- **Amazon Connect contact flows** to manage the customer experience

### AWS Lambda Functions
For these deployments, the following AWS Lambda functions are provided:
- awsscv_extension_routing_query_%InstanceName% (AWSSCV-SFQuery.py): Provides ability to query Salesforce to find user based on extension and user ID parameter provided
- awsscv_extension_routing_processor_%InstanceName% (AWSSCV-ProcessExtension.py): Receives the raw user ID from the Salesforce Rest API query and formats it to match the user ID

### Contact Flow Examples
Example contact flows have been provided to show you how to use the Extension Routing feature.
- AWSSCV-ExtensionRouter-SCV: **(SCV ONLY)** Standard contact flow that uses the default Service Cloud Voice invoke REST Api Lambda funciton to query for the user by extension, then uses the awsscv_extension_routing_processor_%InstanceName% Lambda function to format the retrieved user ID to match the Amazon Connect user ID.
- AWSSCV-AgentWithStreaming: **(SCV ONLY)** Agent whisper flow for Service Cloud Voice deployments that iniates realtime transcription (OPTIONAL)
- AWSSCV-ExtensionRouter-CTI: **(CTI ONLY)** Standard contact flow that uses the default Service Cloud Voice invoke REST Api Lambda funciton to query for the user by extension, then uses the awsscv_extension_routing_query_%InstanceName% Lambda function to find the agent ID based on extension lookup. The Invoke API block must be modified to use the Salesforce field ID that stores the agent username.

## Prerequisites for Service Cloud Voice deployments
1. Service Cloud Voice enabled
2. Amazon Connect configuration complete
3. Users have extensions defined
4. [REST API authentication](https://developer.salesforce.com/docs/atlas.en-us.voice_developer_guide.meta/voice_developer_guide/voice_lambda_auth.htm) for AWS Lambda has been completed
5. Access to the [AWS Console](https://console.aws.amazon.com/console/home)

## Prereqiusites for CTI Adapter deployments
1. [CTI Adaptor for Amazon Connect](https://appexchange.salesforce.com/appxListingDetail?listingId=a0N3A00000EJH4yUAH) installed and configured
2. [Salesforce Access Secrets](https://github.com/amazon-connect/amazon-connect-salesforce-scv/tree/master/common/AWSSCV-SalesforceAccessSecrets) deployed
3. [AWSSCV Common Layers](https://github.com/amazon-connect/amazon-connect-salesforce-scv/tree/master/common/AWSSCV-CommonLayers) deployed
4. Access to the [AWS Console](https://console.aws.amazon.com/console/home)

## Service Cloud Voice deplyoment instructions
### Deploy the CloudFormation template
1. Right-click/control-click to download the [AWSSCV Extension Routing CloudFormation template](https://raw.githubusercontent.com/amazon-connect/amazon-connect-salesforce-scv/master/examples/ExtensionRouting/CloudFormation/awsscv_extension_routing_scv.yaml).
2. In a new browser tab, login to the AWS console
3.	Make sure you are in the same region as your Amazon Connect instance. You can set the region by expanding the region selector in the upper right and choosing the region
4.	Navigate to the CloudFormation console
5.	Select Create Stack, and choose With new resources (standard)
6.	In the Specify Template section, choose Upload a template file
7.	Select Choose file
8.	Navigate to the folder where you saved awsscv_extension_routing_scv.yaml
9.	Select Next
10.	In the Stack Name field, enter AWSSCV-ExtensionRouting-SCV
11.	Enter the parameters as follows (most from your notepad):
  a. AWSRegion: Select the region that you have deployed Amazon Connect in
  b. ConnectInstanceName: Your connect instance name
  c. Salesforce Org ID: Provide the ID for your Salesforce Org
  d. SalesforceRestApiFunctionRole: ARN of the InvokeSalesforceRestApiFunctionRole
12.	Select Next
13.	In Service Cloud Voice deployments, it is normal to see a warning on the next page, Configure stack options
14.	Scroll to the bottom and select Next
15.	Scroll to the bottom and select Create Stack
16.	After a minute or two, the stack should complete.

### Update you Amazon Connect Instance
1. Right-click/control-click to download the [AWSSCV-AgentWithStreaming agent whisper flow](https://raw.githubusercontent.com/amazon-connect/amazon-connect-salesforce-scv/master/examples/ExtensionRouting/ContactFlows/AWSSCV-AgentWithStreaming).
2. Right-click/control-click to download the [AWSSCV-ExtensionRouter-SCV Contact Flow](https://raw.githubusercontent.com/amazon-connect/amazon-connect-salesforce-scv/master/examples/ExtensionRouting/ContactFlows/AWSSCV-ExtensionRouter-SCV).
3. Access to the [AWS Console](https://console.aws.amazon.com/console/home)
4. Navigate to the [Amazon Connect Console](https://console.aws.amazon.com/connect/home)
5. Select your **Amazon Connect instance**
6. Select **Contact Flows** from the left navigation menu
7. Go to the **AWS Lambda** section
8. In the **Function Dropdown**, choose the function that begins with **awsscv_extension_routing_processor_scv**
9. Select **+ Add Lambda Function
10. Select **Overview** from the left navigation menu
11. Select **Log in for emergency access** to open the Amazon Connect admin UI
12. In the left navigation menu, choose **Routing**, then select **Contact flows**
13. Select the down arrow next to Create contact flow and choose **Create agent whisper flow**
14. In the upper-right, select the down arrow and choose **Import flow(beta)**
15. Choose **Select** and navigate to the AWSSCV-AgentWithStreaming flow you dowloaded, then select **Import**
16. In the imported flow, modify the Invoke AWS Lambda function block to use the **kvsConsumerTrigger* Lambda function that you have assigned to your instance.
17. **Save and Publish** the flow
18. Once the flow has published, in the left navigation menu, choose **Routing**, then select **Contact flows**
19. Select **Create contact flow**
20. In the upper-right, select the down arrow and choose **Import flow(beta)**
21. Choose **Select** and navigate to the AWSSCV-ExtensionRouter-SCV flow you dowloaded, then select **Import**
22. In the imported flow, find the **Set whisper flow** block and set it to use the whisper flow that you just published.
23. Find the Invoke AWS Lambda function block that includes the **soql** parameter. In the flow, it should be the first Lambda block the you find.
24. Change that block to use the **InvokeSalesforceRestApiFunction** function configured for your instance.
25. Immediately following the pprevious block, there is another Invoke AWS Lambda function block. Modify it to to use your **awsscv_extension_routing_processor** function.
26. Scroll to the right to find the last Invoke AWS Lambda function block.
27. Change that block to ouse the **InvokeTelephonyIntegrationApiFunction** function configured for your instance.
28. **OPTIONAL:** There is a Set wworking queue block on the bottom of the flow that is connected to the Complete branch on the flow loop. It is set to the default BasicQueue. If you would like calls that fail to connect to an extension to go elsewhere, modify the destination here.
29. **Save and Publish** the flow
30. You can now call this flow from your main IVR once a customer has indicated that they want to speak with a specific agent.

## CTI Adapter deplyoment instructions
### Deploy the CloudFormation template
1. Right-click/control-click to download the [AWSSCV Extension Routing CloudFormation template](https://raw.githubusercontent.com/amazon-connect/amazon-connect-salesforce-scv/master/examples/ExtensionRouting/CloudFormation/awsscv_extension_routing_cti.yaml).
2. In a new browser tab, login to the AWS console
3.	Make sure you are in the same region as your Amazon Connect instance. You can set the region by expanding the region selector in the upper right and choosing the region
4.	Navigate to the CloudFormation console
5.	Select Create Stack, and choose With new resources (standard)
6.	In the Specify Template section, choose Upload a template file
7.	Select Choose file
8.	Navigate to the folder where you saved awsscv_extension_routing_cti.yaml
9.	Select Next
10.	In the Stack Name field, enter AWSSCV-ExtensionRouting-CTI
11.	Enter the parameters as follows (most from your notepad):
  a. AWSRegion: Select the region that you have deployed Amazon Connect in
  b. AWSSCVCommonLambdaPythonLayer: ARN of the common python layer
  c. AWSSCVCommonRole: ARN of the awsscv_common_role role
  d. ConnectInstanceName: Provide the instance name for Amazon Connect.
  e. sfHost: The full https url to your salesforce org.
  f. sfProduction: Is this a production org (true/false)
  g. sfSecrets: ARN for your Salesforce credentials in AWS Secrets Manager
  h. sfVersion: The API version of your Salesforce org.
12.	Select Next
13.	In Service Cloud Voice deployments, it is normal to see a warning on the next page, Configure stack options
14.	Scroll to the bottom and select Next
15.	Scroll to the bottom and select Create Stack
16.	After a minute or two, the stack should complete.

### Update you Amazon Connect Instance
1. Right-click/control-click to download the [AWSSCV-ExtensionRouter-CTI Contact Flow](https://raw.githubusercontent.com/amazon-connect/amazon-connect-salesforce-scv/master/examples/ExtensionRouting/ContactFlows/AWSSCV-ExtensionRouter-CTI).
2. Access to the [AWS Console](https://console.aws.amazon.com/console/home)
3. Navigate to the [Amazon Connect Console](https://console.aws.amazon.com/connect/home)
4. Select your **Amazon Connect instance**
5. Select **Contact Flows** from the left navigation menu
6. Go to the **AWS Lambda** section
7. In the **Function Dropdown**, choose the function that begins with **awsscv_extension_routing_query_cti**
8. Select **+ Add Lambda Function
9. Select **Overview** from the left navigation menu
10. Select **Log in for emergency access** to open the Amazon Connect admin UI
11. In the left navigation menu, choose **Routing**, then select **Contact flows**
12. Select **Create contact flow**
13. In the upper-right, select the down arrow and choose **Import flow(beta)**
14. Choose **Select** and navigate to the AWSSCV-ExtensionRouter-CTI flow you dowloaded, then select **Import**
15. In the imported flow, find the Invoke AWS Lambda function block 
16. Change that block to use the **awsscv_extension_routing_query_cti** function configured for your instance.
17. In the same block, modify the sf_sso_object parameter value to match the Salesforce field that contains your Amazon Connect user name. The mos common configurations are:
  - Username
  - FederationIdentifier
  - Email
  - CommunityNickname
25. Immediately following the pprevious block, there is another Invoke AWS Lambda function block. Modify it to to use your **awsscv_extension_routing_processor** function.
26. Scroll to the right to find the last Invoke AWS Lambda function block.
27. Change that block to ouse the **InvokeTelephonyIntegrationApiFunction** function configured for your instance.
28. **OPTIONAL:** There is a Set wworking queue block on the bottom of the flow that is connected to the Complete branch on the flow loop. It is set to the default BasicQueue. If you would like calls that fail to connect to an extension to go elsewhere, modify the destination here.
29. **Save and Publish** the flow
30. You can now call this flow from your main IVR once a customer has indicated that they want to speak with a specific agent.