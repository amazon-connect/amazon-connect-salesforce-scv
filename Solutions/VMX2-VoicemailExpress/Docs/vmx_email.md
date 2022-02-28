# Delivering Voicemails as Email via Amazon Simple Email Service (SES)


## Additional Contact Attributes Specific to Tasks
There are two additional contact attribute that applies to this delivery model:
-  **email_from (Optional)**: (email address) email address to send the voicemail FROM. If this is not provided, the default FROM address configured during implementation will be used.
    -  Example: 'email_from':'my_company@example.com'
-  **email_to (Optional)**: (email address) email address to send the voicemail TO. If this is not provided, and it cannot be determined by looking at the agent or queue data, the default TO address configured during implementation will be used.
    -  Example: 'email_to':'my_company@example.com'

## Additional Notes
1.  
