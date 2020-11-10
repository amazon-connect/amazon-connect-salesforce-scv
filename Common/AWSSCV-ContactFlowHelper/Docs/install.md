# Contact Flow Helper Installation
This is a simple helper Lambda that can be used standalone to help manipulate data gathered in other managed functions. 

## Deplyoment instructions
### Deploy the CloudFormation template
1. Right-click/control-click to download the [AWSSCV Contact Flow Helper template](https://raw.githubusercontent.com/amazon-connect/amazon-connect-salesforce-scv/master/Common/AWSSCV-ContactFlowHelper/CloudFormation/awsscv_contact_flow_helper.yaml).
2. In a new browser tab, login to the [AWS Console](https://console.aws.amazon.com/console/home)
3.	Make sure you are in the **same region** as your Amazon Connect instance. You can set the region by expanding the region selector in the upper right and choosing the region
4.	Navigate to the **CloudFormation console**
5.	Select **Create Stack**, and choose **With new resources (standard)**
6.	In the Specify Template section, choose **Upload a template file**
7.	Select **Choose file**
8.	Navigate to the folder where you saved a**wsscv_follow_me_routing.yaml**
9.	Select **Next**
10.	In the Stack Name field, enter `AWSSCV-ContactFlowHelper`
11.	**Enter the parameters** as follows (most from your notepad):
  a. AWSRegion: Select the region that you have deployed Amazon Connect in
  b. AWSSCVCommonRole: ARN of the awsscv_common_role role
  c. ConnectInstanceName: Provide the instance name for Amazon Connect.
12.	Select **Next**
13.	In Service Cloud Voice deployments, it is normal to see a warning on the next page, Configure stack options
14.	Scroll to the bottom and select **Next**
15.	Scroll to the bottom and select **Create Stack**
16.	After a minute or two, the stack should complete.