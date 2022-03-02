# Delivering Voicemails to a Salesforce Custom Object
This is a variation of the Salesforce Case routing and, as such, is nearly identical from a delivery perspective. Voicemails are created using a custom object in Salesforce. This custom object must be defined as a part of the prerequisites and the appropriate values used when deploying this template. In this configuration,  all data elements are written to the custom fields created for the custom object. When using this model, voicemails targeted at a specific agent are created with that agent as the owner. Voicemails targeted at a queue are created with configured API user as the owner. In either circumstance, the intent is for the configured case routing rules in salesforce to manage the routing and assignment of voicemail cases.

## Additional Contact Attributes Specific to Salesforce Custom Objects
Outside of those configured as a part of the prerequisites, there are no additional contact attributes required for this model to work.

## Accessing Contact Attributes
All of the contact attributes for the call are stored as a string in the custom contact attributes field that was created as a part of the prerequisites for Salesforce. This can be modified, if desired, by editing the **sub_salesforce_other.py** file in the VMXPackager function, beginning at line 66 and again at line 75. Please note that there are two versions of the write in that file, one for agent voicemails and one for queue voicemails.
