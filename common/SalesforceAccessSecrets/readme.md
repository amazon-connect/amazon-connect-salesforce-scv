# Salesforce Secrets
Establishes a Connected App, User, and other resources in Salesforce and saves the access and login credentials to the AWS account using AWS Secrets Manager for secure storage and retrieval of the credentials as needed. These credentials are then used for the projects in this repository where authentication with Salesforce is required.

# Setup
Follow the following steps to prepare your Salesforce Org before running the CloudFormation template. As you proceed through these instructions, it is reccomended that you use a text editor to save important information along the way. Each item you need to save will be specifically called out.

## Check your Salesforce API Version
1. Log in into your Salesforce org and go to Setup 
2.	In the Quick Find field, type `apex`, then select Apex Classes from the results 
3.	Select New
4.	Select the Version Settings tab
5.	**Note the Salesforce.com API version in your notepad**

## Create a New Connected App
1.	Log in into your Salesforce org and go to Setup 
2.	In the Quick Find field, type `app manager`, then select App Manager from the results 
3.	In the upper right corner, select New Connected App
4.	On the New Connected App form, enter `AWS_Utility` as the name for the Connected App. This will populate the API Name automatically. Then provide a contact email address
5.	Select the checkbox to Enable OAuth Settings 
6.	Set the Callback URL to `https://www.salesforce.com`
7.	In the Selected OAuth Scopes section, select the following and add them to the Selected OAuth Scopes:
  * Access and manage your data (api)
  * Access your basic information (id, profile, email, address, phone)
8.	Select the checkbox for Require Secret for Web Server Flow
9.	Select Save at the bottom of the screen.
10.	Select Continue on the New Connected App page
11.	You should now be at the new app’s page
12.	**Copy the value for Consumer Key to your notepad**
13.	Select Click to reveal next to Consumer Secret and **copy the value for Consumer Secret to your notepad**
14.	At the top of the detail page, select Manage
15.	On the Connected App Detail page, select the Edit Policies button
16.	Set Permitted Users to Admin approved users are pre-authorized and choose OK on the pop-up dialog
17.	Set IP Relaxation to Relax IP restrictions
18.	Select Save

## Create a new Profile and API user
1.	Log in into your Salesforce org and go to Setup 
2.	In the Quick Find field, type `profiles`, then select Profiles from the results 
3.	Select New Profile
4.	Enter `AWS_Utility` as the Profile Name
5.	From the Existing Profile dropdown, select System Administrator
6.	Select Save to create the new profile
7.	Once the new profile saves, select it from the Profiles list
8.	In the System section, select System Permissions
9.	Select Edit
10.	Scroll down to Lightning Experience User and clear the checkbox, if selected
11.	Scroll down and select Password Never Expires 
  * NOTE: Failure to this may lead to production outages.
12.	Select Save
13.	In the Quick Find field, type connect, then select Manage Connected Apps from the results 
14.	Select the app you have created earlier, AWS_Utility 
15.	In the profiles section, select Manage Profiles
16.	Select the new AWS_Utility profile that you just created
17.	Select Save at the bottom of the page
18.	In the Quick Find field, type `users` then select Users from the results 
19.	Select New User
20.	Set the required fields as:
  a.	Last Name: awsutil
  b.	Alias: awsutil
  c.	Email: provide a valid email address
  d.	Username: awsutil@<yoursalesforcedomain>.com
  e.	Nickname: awsutil
21.	On the right-hand side, set User License to Salesforce
22.	Set Profile to AWS_Utility
23.	Choose Save
24.	**Copy the username to your notepad**
25.	A confirmation email with an activation link will be sent to the email address provided. Choose the link to activate your user and set their password
26.	Fill out the form to set a password for the API user. **Copy the new password to your notepad**
27.	Select Change Password. The API user will log into the Salesforce Classic view
28.	Access the API user’s personal settings by selecting the username in the top right corner, then choose My Settings 
29.	In the Quick Find field, type `security` then select Reset My Security Token from the results
  - NOTE: if you do not see Reset My Security Token, you can get there by goint to the following URL: `https://[SalesforceDomainHere]/_ui/system/security/ResetApiTokenEdit?retURL=%2Fui%2Fsetup%2FSetup%3Fsetupid%3DPersonalInfo&setupid=ResetApiToken`
30.	Select Reset Security Token. Your security token will be emailed to you
31.	**Copy the security token from the email to your notepad**

## Store Salesforce Credentials in AWS Secrets Manager
To ensure that your Salesforce credentials are secure, the Lambdas require that the credentials are stored in AWS Secrets Manager. AWS Secrets Manager is a highly secure service that helps you store and retrieve secrets.

1.	Download the [CloudFormation template](CloudFormation/scv-ssm.yaml).
2. In a new browser tab, login to the AWS console
3.	Make sure you are in the same region as your Amazon Connect instance. You can set the region by expanding the region selector in the upper right and choosing the region
4.	Navigate to the CloudFormation console
5.	Select Create Stack, and choose With new resources (standard)
6.	In the Specify Template section, choose Upload a template file
7.	Select Choose file
8.	Navigate to the folder where you saved scv_ssm.yaml
9.	Select Next
10.	In the Stack Name field, enter SCVSSM
11.	Enter the parameters as follows (most from your notepad):
  a.	AWSRegion: Select the region that you have deployed Amazon Connect in
  b.	ConnectInstanceName: Your connect instance name
  c.	SFAccessToken: The user access token
  d.	SFConsumerKey: The consumer key from your connected app
  e.	SFConsumerSecret: The consumer secret from your connected app
  f.	SFPassword: Your voicemail user’s password
  g.	SFUsername: Your voicemail username
12.	Select Next
13.	In Service Cloud Voice deployments, it is normal to see a warning on the next page, Configure stack options
14.	Scroll to the bottom and select Next
15.	Scroll to the bottom and select Create Stack
16.	After a minute or two, the stack should complete.
