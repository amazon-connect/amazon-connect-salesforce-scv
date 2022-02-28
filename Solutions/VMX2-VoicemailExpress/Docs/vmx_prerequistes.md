# Voicemail Express Prerequisites
Before deploying the Voicemail Express solutions, you will need to complete a few prerequisites. These will lay the foundation and prepare both environments for the voicemail solution. These **must be completed** prior to the deployment of Voicemail Express.
- FOR SALESFORCE DELIVERY MODES ONLY: Complete the [AWSSCV Salesforce Config](../../../Common/AWSSCV-SalesforceConfig) setup

**Note:** You will need to save information to a notepad during the entire setup process.

## **Salesforce Delivery Modes Only:** Additional Requirements for Salesforce Delivery Modes
There are two primary Salesforce delivery modes: Case and Custom. For cases, we are creating a new case and including the data related to voicemail in that case. Once the case is created, your Salesforce case routing rules take effect and cases are assigned based on those rules. For custom delivery, we will write the voicemail data to a custom object that you provide, for example a "voicemail" custom object. The steps below will walk through the configuration in both. We will start with custom objects to configure the requirements there, then move to elements that relate to both cases and custom objects.

### Setup steps for Custom Object delivery
### Create a custom object to receive the voicemail
1.	Log in into your Salesforce org and go to Setup
2.	In the Quick Find field type `Object`
3.	Select Object Manager from the results
4.  Choose Create, then select Custom Object
5.  Set a value for the label, such as `Voicemail`
6.  Set a value for the Plural Label, such as `Voicemails`
7.  Leave everything else to the defaults and select Save
8.	When the page reloads, **copy the API name (not the label) to your notepad**. It should end in __c

### Create a custom field for the voicemail transcription
1.	Log in into your Salesforce org and go to Setup
2.	In the Quick Find field type `Object`
3.	Select Object Manager from the results
4.	Find and select your custom object
5.	Choose Fields & Relationships
6.	Select New
7.	Choose Text Area (Rich), then select Next
8.	Set a value for field label, such as `Voicemail Transcript`
9.	Select Next
10.	On the Step 3 page, select Next
11.	On the step 4 page, select Save
12.	When the page reloads, scroll to the new field you created and **copy the field name (not the label) to your notepad**. It should end in __c

### Setup steps for all Salesforce Models
### Create a custom field for the voicemail callback number
1.	Log in into your Salesforce org and go to Setup
2.	In the Quick Find field type `Object`
3.	Select Object Manager from the results
4.	Find and select Case
5.	Choose Fields & Relationships
6.	Select New
7.	Choose Phone, and select Next
8.	Set a value for field label, such as `Callback Phone`
9.	Select Next
10.	On the Step 3 page, select Next
11.	On the step 4 page, select Save
12.	When the page reloads, scroll to the new field you created and **copy the field name (not the label) to your notepad**. It should end in __c

### Create a custom field for the contact Attributes
1.	Log in into your Salesforce org and go to Setup
2.	In the Quick Find field type `Object`
3.	Select Object Manager from the results
4.	Find and select Case
5.	Choose Fields & Relationships
6.	Select New
7.	Choose Text Area (Rich), then select Next
8.	Set a value for field label, such as `Connect Contact Attributes`
9.	Set # Visible Lines to 25
10.	Select Next
11.	On the Step 3 page, select Next
12.	On the step 4 page, select Save
13.	When the page reloads, scroll to the new field you created and **copy the field name (not the label) to your notepad**. It should end in __c

## **AWS Delivery Modes Only:** Additional Requirements AWS Delivery Modes
There are two primary AWS delivery modes: Amazon Connect Task and Email Delivery via Amazon Simple Email Service (SES). There are a few steps required to prepare for either delivery mode.

### Setup steps for Amazon Connect Tasks
For Amazon Connect Task delivery, you simply need to ensure that you have routing profiles with Tasks enabled, and that the agents are assigned to those routing profiles.

### Update routing profiles to include Tasks
1.  Login to the Amazon Connect administration interface
2.  From the navigation menu, select Users and then choose Routing Profiles
3.  Select the routing profile that you wish to edit
4.  In the **Set channels and concurrency** section, make sure Task is selected and set a value for Maximum tasks (per agent)
5.  In the **Routing profile queues** section, make sure that the Task channel is selected for all queues that you wish to activate for tasks/voicemail
6.  Select Save

Make sure that your agents are assigned to the routing profiles with tasks enabled, and thats it!

### Setup steps for Email delivery
For email delivery, Voicemail Express uses SES. If you have not already configured SES for use in your account, you will need to perform some minimal configuration to validate email addresses. There are two types of email addresses in this solution: `from` and `to`. The from address will indicate where the email is from, for example contact_center@yourcompany.com. You can dynamically assign the from address, or simply use a default. This decision can be made on a call-by-call basis. The `to` address will be where the email is being delivered to. For agent voicemails, it should be the email address of the agent, for example: joe.smith@yourcompany.com. For queue voicemails, it would be a group address or distribution list, for example: customer_support@yourcompany.com. In order for SES to send emails using your email addresses ,you need to validate ownership of either the individual addresses or the entire email domain. You can follow the instructions online for [creating and verifying identities in Amazon SES](https://docs.aws.amazon.com/ses/latest/dg/creating-identities.html) to accomplish this. You must use verified identities/domains, or the emails will not be delivered.

### Voicemail to agent emails
This solution is designed to use the agents login ID as the email address. If you are not using the agent email as their login ID, the packager function will need to be modified to account for that. If you are, then nothing further needs to be done.

### Voicemail to queues
For queues, the solution is designed to extract the email address from the queue description. This allows you to set the address by queue. If no address is specified, the solution will used the provided default address.

### Update the queue to include the email address
1.  Login to the Amazon Connect administration interface
2.  Select Routing, then choose Queues
3.  Select the Queue that you wish to modify
4.  In the description section, enter a space at the end of the existing description (if any), then enter `QVMB::`
5.  Immediately after the `::` enter the email address for this queue
6.  The queue description should now be similar to: `Basic queue description. QVMB::myqueue@mycompany.com`
7.  Save the queue

## Prerequistes Complete
You have completed the perquisites for the Voicemail Express solution. You may now proceed to the [installation instructions](vmx_installation_instructions.md).
