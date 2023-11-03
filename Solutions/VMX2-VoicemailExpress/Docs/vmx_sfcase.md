# Delivering Voicemails to Salesforce as Cases
This is the original delivery mode for Voicemail Express. Voicemails are created as cases in Salesforce with the transcript as the case description. When using this model, voicemails targeted at a specific agent are created with that agent as the owner. Voicemails targeted at a queue are created with configured API user as the owner. In either circumstance, the intent is for the configured case routing rules in salesforce to manage the routing and assignment of voicemail cases.

## Additional Contact Attributes Specific to Salesforce Cases
There is only one additional contact attribute required for routing voicemails as cases, and that is the case priority. It is defied as follows:
-  **vmx_priority**: (String) set to the appropriate priority level as defined by your organization.
Example: 'vmx_priority':'low'

## Accessing Contact Attributes
All of the contact attributes for the call are stored as a string in the custom contact attributes field that was created as a part of the prerequisites for Salesforce. This can be modified, if desired, by editing the **sub_salesforce_case.py** file in the VMXPackager function, beginning at line 70 and again at line 82. Please note that there are two versions of the write in that file, one for agent voicemails and one for queue voicemails.
