# Follow-Me Routing
Follow-Me routing provides an option to allow users to flag themselves as available via external phone number then, when customers call specifically for them, the call is redirected to their external line. The basic flow for this experience is as follows:
1. Caller is routed directly to the agent personal queue.
2. Agent is not logged in
3. Caller is redirected to agent's external number.
4. If agent does not answer, customer is offered the opportunity to switch queues.

## Deployment Resources
To enable Follow-Me routing, we need to deploy one AWS Lambda function and import one contact flow. Additionally, we need to configure a custom field in the Salesforce User object, and ensure that users have an appropriate phone number in the Mobile field.

### AWS Lambda Function
For these deployments, the following AWS Lambda function is provided:
- awsscv_follow_me_%InstanceName% (AWSSCV-FollowMe.py): Provides ability to query Salesforce to find user external phone based on user ID parameter providedZ

### Contact Flow Example
Example contact flow has been provided to show you how to use the Follow-Me Routing feature.
- AWSSCV-FollowMe: Standard contact flow that checks the provided agent ID to see if they are logged in. If not, queries Salesforce to determine if they are configured for Follow Me routing. If so, connects the agent externally and provides a follow-up menu post call.

## Prerequisites for all deployments
1. In order to make the follow me option work, the user must be configured with two items:
- External phone number
- Follow-Me flag set to True
  - NOTE: As the Follow-Me flag does not exist, you will need to add it
2. [AWSSCV Salesforce Config](https://github.com/amazon-connect/amazon-connect-salesforce-scv/tree/master/common/AWSSCV-SalesforceConfig) deployed
3. [AWSSCV Common Layers](https://github.com/amazon-connect/amazon-connect-salesforce-scv/tree/master/common/AWSSCV-CommonLayers) deployed
4. Access to the [AWS Console](https://console.aws.amazon.com/console/home)

### Adding the Follow-Me flag
1. Log in into your Salesforce org and go to **Setup** 
2. In the **Quick Find** field type `Object`
3. Select **Object Manager** from the results
4. Find and select **User**
5. Choose **Fields & Relationships**
6. Select New
7. Choose **Checkbox**, then select Next
8. **Set a value** for field label, such as `Enable Follow-Me`
9. Select Next
10. On the Step 3 page, select Next
11.	On the step 4 page, select Save
12.	When the page reloads, scroll to the new field you created and **copy the field name (not the label) to your notepad**. It should end in __c

### Set Follow-Me flag and validate phone field
1. Log in into your Salesforce org and go to **Setup** 
2. In the **Quick Find** field type `Users`
3. Select **Users** from the results
4. **Select the user** that you wish to modify and choose **Edit**
5. Find the Enable **Follow-Me** (Or whatever you named your field) checkbox and select it.
6. **Validate** that an E.164 formatted phone number exists for the agent in either the Phone (Phone) or Mobile (MobilePhone) fields. Note which field you are using. This should be consistent across users.
7. **Save** the user

## Deplyoment instructions
### Deploy the CloudFormation template
1. Right-click/control-click to download the [AWSSCV FollowMe Routing CloudFormation template](https://raw.githubusercontent.com/amazon-connect/amazon-connect-salesforce-scv/master/examples/FollowMeRouting/CloudFormation/awsscv_follow_me_routing.yaml).
2. In a new browser tab, login to the [AWS Console](https://console.aws.amazon.com/console/home)
3.	Make sure you are in the **same region** as your Amazon Connect instance. You can set the region by expanding the region selector in the upper right and choosing the region
4.	Navigate to the **CloudFormation console**
5.	Select **Create Stack**, and choose **With new resources (standard)**
6.	In the Specify Template section, choose **Upload a template file**
7.	Select **Choose file**
8.	Navigate to the folder where you saved a**wsscv_follow_me_routing.yaml**
9.	Select **Next**
10.	In the Stack Name field, enter `AWSSCV-FollowMe`
11.	**Enter the parameters** as follows (most from your notepad):
  a. AWSRegion: Select the region that you have deployed Amazon Connect in
  b. AWSSCVCommonLambdaPythonLayer: ARN of the common python layer
  c. AWSSCVCommonRole: ARN of the awsscv_common_role role
  d. ConnectInstanceName: Provide the instance name for Amazon Connect.
  e. sfDeploymentMode: Is this for a CTI-Based install (cti) or a Service Cloud Voice (scv) deployment?
  f. sfFollowField: The name of the checknox field that you created in Salesforce to enable the Follow-Me function.
  g. sfPhoneField: Which phone field will you be using? Phone or MobilePhone?
  h. sfConfig: ARN for your Salesforce config in AWS Secrets Manager
  i. sfUserField: Field is used as your Connect Username? For Service Cloud Voice, select Id. For CTI, choose the appropriate option.
12.	Select **Next**
13.	In Service Cloud Voice deployments, it is normal to see a warning on the next page, Configure stack options
14.	Scroll to the bottom and select **Next**
15.	Scroll to the bottom and select **Create Stack**
16.	After a minute or two, the stack should complete.

### Update you Amazon Connect Instance
1. Right-click/control-click to download the [AWSSCV-FollowMe contact flow](https://raw.githubusercontent.com/amazon-connect/amazon-connect-salesforce-scv/master/examples/FollowMeRouting/ContactFlows/AWSSCV-FollowMe-Test).
2. Access to the [AWS Console](https://console.aws.amazon.com/console/home)
3. Navigate to the [Amazon Connect Console](https://console.aws.amazon.com/connect/home)
4. Select your **Amazon Connect instance**
5. Select **Contact Flows** from the left navigation menu
6. Go to the **AWS Lambda** section
7. In the **Function Dropdown**, choose the function that begins with **awsscv_follow_me**
8. Select **+ Add Lambda Function
9. Select **Overview** from the left navigation menu
10. Select **Log in for emergency access** to open the Amazon Connect admin UI
11. In the left navigation menu, choose **Routing**, then select **Contact flows**
12. Select **Create contact flow**
13. In the upper-right, select the down arrow and choose **Import flow(beta)**
14. Choose **Select** and navigate to the AWSSCV-FollowMe-Test flow you dowloaded, then select **Import**
15. In the imported flow, find the **Set contact attributes** block and set it to use the connect username that you want to test with.
16. Find the Invoke AWS Lambda function block.
17. Change that block to use the function that begins with **awsscv_follow_me**.
18. **OPTIONAL:** There are a couple Set wworking queue blocks on the right of the flow. They are set to the default BasicQueue. If you would like the calls that fail to connect to the agent to go elsewhere, modify the destination here.
19. **Save and Publish** the flow
20. Navigate to **Routing**, and select **Phone numbers**
21. Select **Claim a number**
22. Select **DID (Direct Inward Dialing)** and then **set the country** as appropriate
23. Select the desired phone number
24. In the **Description**, enter `Follow Me Test`
25. Form the ***Contact flow / IVR*** list, select **AWSSCV-FollowMe-Test**
26. Select **Save**
27. After ~2 minutes, your configuration will be ready to test.
