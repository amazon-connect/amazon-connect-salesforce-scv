# Removing/Uninstalling Voicemail Express
Whether it is to migrate to Salesforce's included voicemail solution, or to simply stop using this one, uninstalling Voicemail Express is a fairly straightforward process.

## Prepare the Amazon Connect Instance
First, you will need to prepare the instance for Voicemail removal. To do this, perform the following tasks:
1.  Log into your Amazon Connect instance as an administrator.
1.  Select **Channels**, then choose **Phone numbers**.
1.  Make sure that none of VMX default flows are set as the **Contact flow/IVR** for any phone numbers in your instance. The four default flows are:
    1.  VMXAWSTestFlow-%instance-name%
    1.  VMXBasicTaskFlow-%instance-name%
    1.  VMXCoreFlow-%instance-name%
    1.  VMXSFDCTestFlow-%instance-name%

| :warning: IMPORTANT          |
|:---------------------------|
| You may have referenced some of these flows from within your other flows. While not necessary to uninstall the solution, you should also validate that these default flows are not referenced elsewhere as that could result in flow failures.|

## Move your voicemail recordings/transcripts
Since the retention policy of the CloudFormation template used to deploy voicemail does not allow for the deletion of the S3 buckets that hold the voicemail recordings and temporary transcripts if they have objects in them, you should first either copy the contents elsewhere (if you wish to retain copies for archival) or delete the contents of the S3 buckets. 

To determine which S3 buckets are in use:
1.  Login to the [AWS Console](https://console.aws.amazon.com).
1.  Navigate to the [AWS CloudFormation console](https://console.aws.amazon.com/cloudformation/home).
1.  Make sure that you are in the correct region for your deployment.
1.  Select **Stacks**, then choose the **VMXCoreStack** stack.
1.  Select the **Resources** tab.
1.  In the **Logical ID** column, find both **VMXS3RecordingsBucket** and **VMXS3TranscriptsBucket**. 
1.  The link in the corresponding **Physical ID** column will take you to each bucket.
1.  Export or delete the objects as desired.

## Delete the CloudFormation Stack
Next, you will delete the CloudFormation stack. This will remove **ALL** AWS resources that were created with the conditional exception of the S3 buckets. By default, if the S3 buckets have any objects in them, they will not be deleted and all contents will remain in place. If you are not concerned with keeping your recordings, or if you wish to move them to 

1.  Login to the [AWS Console](https://console.aws.amazon.com).
1.  Navigate to the [AWS CloudFormation console](https://console.aws.amazon.com/cloudformation/home).
1.  Make sure that you are in the correct region for your deployment.
1.  Select **Stacks**, then choose the Voicemail Express stack that you deployed. If you don't recall the name, the description should include **Voicemail Express**.
1.  Select **Delete**, then confirm by choosing **Delete** from the popup.
1.  **IF** your stack deleted completely, you may move on to the next section.
1.  **IF** your stack failed to fully delete, it is most likely due to there being content in your S3 bucket. In this case, select the nested stack that failed, most likely the VMXCoreStack, and choose **Delete**. 
1.  In the popup window, you will likely see the resources that could not be deleted, which are probably the S3 buckets. Select both to retain them, and select **Delete**.
1.  Once the nested stack deletes, reselect the main stack, and select **Delete**. This time, the resources should delete without further issue.

## Delete the SF Config stack
The Voicemail Express solution required the SF Config deployment that is used by a number of solutions on this repo. If you are not using any other solutions, you can remove this stack as well. 

1.  Login to the [AWS Console](https://console.aws.amazon.com).
1.  Navigate to the [AWS CloudFormation console](https://console.aws.amazon.com/cloudformation/home).
1.  Make sure that you are in the correct region for your deployment.
1.  Select **Stacks**, then choose the SF Config stack that you deployed. If you don't recall the name, the description should include **Performs the base configuration**.
1.  Select **Delete**, then confirm by choosing **Delete** from the popup.
1.  This should be a very fast deletion, taking less than one minute to complete.

## Clean up your Salesforce Org
The last step is to remove the created entities that provided the API connection for Voicemail Express to work. Please make sure that you are not using these entities for any other purpose before removing them. Removal is not required.

1.  Login to Salesforce as an administrator and go to **Setup**.
1.  In the Quick Find, enter **app manager** and choose **App Manager** from the filtered list.
1.  Find the **AWS_Utility** app and select **View** from the dropdown on the right side of its row.
1.  On the detail page, select **Delete**, then choose **Delete** on the confirmation page.
1.  In the Quick Find, enter **user** and choose **Users** from the filtered list.
1.  Find the **awsutil** user and select **Edit** next to their name.
1.  Deselect the **Active** checkbox. Select **OK** on the popup, then choose **Save**.
1.  In the Quick Find, enter **permission** and choose **Permission Sets** from the filtered list.
1.  Select the **AWS_Utility** permission set.
1.  On the permission set details page, select **Manage Assignments**.
1.  Select the checkbox next to the **awsutil** user, then choose the **delete** button (looks like a trash can). Confirm your action by selecting **Remove** on the popup.
1.  Return to the list of **Permission Sets**
1.  Next to AWS_Utility, select **Del**. then choose **OK** from the popup.

You have successfully removed the Voicemail Express Solution. The existing voicemails (either cases or custom objects, depending on your deployment) will remain until manually deleted. 