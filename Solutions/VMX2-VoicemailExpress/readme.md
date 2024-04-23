| :warning: IMPORTANT          |
|:---------------------------|
| This solution will have limited updates for Salesforce environments, with only critical updates to runtime versions or to correct significant issues. Salesforce Service Cloud Voice customers are encouraged to utilize the [native voicemail offering](https://developer.salesforce.com/docs/atlas.en-us.voice_developer_guide.meta/voice_developer_guide/voice_example_voicemail.htm), which is based on this code but updated and developed by salesforce. 

Amazon Connect customers that require a voicemail solution should use the [new version of this solution,](https://github.com/amazon-connect/voicemail-express-amazon-connect), which has been specificly refined for Amazon Connect customers who do not use Service Cloud Voice.|


# Voicemail Express V2
Voicemail Express is designed to provide basic voicemail functionality to Amazon Connect Customers. It has been designed to work in a variety of customer deployment models, including Service Cloud Voice. Voicemail express provides delivery of voicemail via a variety of mechanism and also offers customization patterns for other delivery models. This version natively supports voicemail delivery via Amazon Connect Task, e-mail delivery via Amazon Simple Email Service, Salesforce Case, Salesforce custom objects, or a custom delivery mode of your own design. It has also been redesigned to support different modes on a call-by-call basis.

![Voicemail Express Architecture](Docs/Img/vmx2.png)

## What's new (2024.02.28)
-  Updated presigner for better reliability
-  Updated node version to 18

With Voicemail Express, customers can have the option to leave a voicemail for an agent or queue. Once the voicemail is recorded, a series of processes take place that ultimately result in:
1. Voicemail stored in S3 as a .wav file
2. Transcription of the voicemail
3. Presigned URL that provides access to the voicemail from Salesforce without the need for authentication into AWS.
4. Voicemail is packaged for delivery, including the transcription, presigned URL, and contact data. It is then delivered via the chosen mechanism.

Voicemails in this solution are configured for a lifecycle of up to 7 days. After 7 days, the recordings are lifecycled and the presigned URL is no longer valid. During deployment, you have the option to reduce this lifecycle window, if desired. Additionally, you have the option to keep, archive, or delete voicemail recordings. However recordings are lifecycled, the data (with transcript) will reside in the selected delivery system.

To deploy Voicemail Express, you will need to complete the following:
1. For customers that are deploying Salesforce delivery modes, complete the [AWSSCV Salesforce Config](../../Common/AWSSCV-SalesforceConfig/readme.md) setup
2. Complete the [Voicemail Express Prerequisites](Docs/vmx_prerequistes.md)
3. Complete the [Voicemail Express Installation](Docs/vmx_installation_instructions.md)

Once Voicemail Express has been deployed, you can learn more about the different modes by referencing the following documents:
1. [High-level overview of the Voicemail Express solution](Docs/vmx_core.md)
2. [Delivering Voicemails as Amazon Connect Tasks](Docs/vmx_tasks.md)
3. [Delivering Voicemails via Amazon Simple Email Service](Docs/vmx_email.md)
4. [Delivering Voicemails as Salesforce Cases](Docs/vmx_sfcase.md)
5. [Delivering Voicemails as Salesforce Custom Objects](Docs/vmx_sfcustom.md)
6. [Creating your own custom delivery mode for Voicemails](Docs/vmx_custom.md)

To remove Voicemail Express, once deployed:
1.  [Removing/Uninstalling Voicemail Express](Docs/vmx_uninstall.md)

Finally, some basic troubleshooting steps can be found on the [Troubleshooting Common Voicemail Issues](Docs/vmx_troubleshooting.md) page.

**Current Published Version:** 2024.02.28
Current published version is the version of the code and templates that has been deployed to our S3 buckets
