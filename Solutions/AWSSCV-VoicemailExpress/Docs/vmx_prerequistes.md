# Voicemail Express Prerequisites
Before deploying the Voicemail Express solutions, you will need to complete a few prerequsites. These will lay the foundation and prepare both environments for the voicemail solution. These **must be completed** prior to the deployment of Voicemail Express.
- Complete the [AWSSCV Salesforce Config](../../../Common/AWSSCV-SalesforceConfig) setup
- Complete the [AWSSCV Common Layers](../../../Common/AWSSCV-CommonLayers) Setup
- Complete the steps below to configure new fields for the Voicemail transcript and callback number in Salesforce.

**Note:** You will need to save information to a notepad during the entire setup process. 

## Create a custom field for the voicemail link
1.	Log in into your Salesforce org and go to Setup 
2.	In the Quick Find field type `Object`
3.	Select Object Manager from the results
4.	Find and select Case
5.	Choose Fields & Relationships
6.	Select New
7.	Choose Text Area (Rich), then select Next
8.	Set a value for field label, such as `Voicemail Link`
9.	Set the length to 4,000
10.	Set # Visible Lines to 10
11.	Select Next
12.	On the Step 3 page, select Next
13.	On the step 4 page, select Save
14.	When the page reloads, scroll to the new field you created and **copy the field name (not the label) to your notepad**. It should end in __c

## Create a custom field for the voicemail callback number
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

## Create a custom field for the contact Attributes
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

## Prerequistes Complete
You have copleted the prequisites for the Voicemail Express solution. You may now proceed to the [installation instructions](vmx_installation_instructions.md).
