# Voicemail Express V2
Voicemail Express is designed to provide basic voicemail functionality to Amazon Connect Customers. It has been designed to work in a variety of customer deployment models, including Service Cloud Voice. Voicemail express provides delivery of voicemail via a variety of mechanism and also offers customization patterns for other delivery models. This version natively supports voicemail delivery via Amazon Connect Task, e-mail delivery via Amazon Simple Email Service, Salesforce Case, Salesforce custom objects, or a custom delivery mode of your own design. It has also been redesigned to support different modes on a call-by-call basis.

![Voicemail Express Architecture](Docs/Architecture.png)

With Voicemail Express, customers can have the option to leave a voicemail for an agent or queue. Once the voicemail is recorded, a series of processes take place that ultimately result in:
1. Voicemail stored in S3 as a .wav file
2. Transcription of the voicemail
3. Presigned URL that provides access to the voicemail from Salesforce without the need for authentication into AWS.
4. Voicemail is packed for delivery, including the transcription, presigned URL, and contact data. It is then delivered via the chosen mechanism.

Voicemails in this solution are configured for a lifecycle of up to 7 days. After 7 days, the recordings are lifecycled and the presigned URL is no longer valid. During deployment, you have the option to reduce this lifecycle window, if desired. Additionally, you have the option to keep, archive, or delete voicemail recordings. However recordings are lifecycled, the data (with transcript) will reside in the selected delivery system.

To deploy Voicemail express, you will need to complete the following:
1. For customers that are deploying Salesforce delivery modes, complete the [AWSSCV Salesforce Config](../../Common/AWSSCV-SalesforceConfig/readme.md) setup
2. Complete the [Voicemail Express Prerequisites](Docs/vmx_prerequistes.md)
3. Complete the [Voicemail Express Installation](Docs/vmx_installation_instructions.md)
