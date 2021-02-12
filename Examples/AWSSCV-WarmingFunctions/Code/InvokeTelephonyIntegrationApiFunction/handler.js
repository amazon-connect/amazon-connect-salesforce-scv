'use strict';

const SCVLoggingUtil = require('./SCVLoggingUtil.js');
const api = require('./telephonyIntegrationApi.js');
const config = require('./config.js');
const utils = require('./utils.js');

exports.handler = async (event) => {
    let result = {};
    
    // BEGIN AWS modification for EventBridge
    let eventSource = event.source || 'undefined';
    if (eventSource == 'aws.events') {
        result = {'eventStatusCode': 200,'eventResponse' : 'warm', 'eventType' : 'EventBridge'};
        console.log(result)
        return result
    }
    // END AWS modification for EventBridge
    
    const { methodName, fieldValues, contactId } = event.Details.Parameters; 

    switch (methodName) {
        case 'createVoiceCall':
            var voiceCallFieldValues = {
                callCenterApiName: config.callCenterApiName,
                vendorCallKey: event.Details.ContactData.ContactId,
                to: event.Details.ContactData.SystemEndpoint.Address,
                from: event.Details.ContactData.CustomerEndpoint.Address,
                initiationMethod: "Inbound",
                startTime: new Date().toISOString(),
                callAttributes: utils.getCallAttributes(event.Details.ContactData.Attributes),
                participants: [
                    {
                    participantKey: event.Details.ContactData.CustomerEndpoint.Address,
                    type: "END_USER"
                    }
                ]
            };
            result = await api.createVoiceCall(voiceCallFieldValues);
            break;
        case 'updateVoiceCall':
            fieldValues["callCenterApiName"] = config.callCenterApiName;
            result = await api.updateVoiceCall(contactId, fieldValues);
            break;
        case 'createTransferVC':
            var voiceCallFieldValues = {
                callCenterApiName: config.callCenterApiName,
                vendorCallKey: event.Details.ContactData.ContactId,
                to: event.Details.ContactData.SystemEndpoint.Address,
                from: event.Details.ContactData.CustomerEndpoint.Address,
                parentVoiceCallId: event.Details.ContactData.PreviousContactId,
                initiationMethod: "Transfer",
                startTime: new Date().toISOString(),
                participants: [
                    {
                    participantKey: event.Details.ContactData.CustomerEndpoint.Address,
                    type: "END_USER"
                    }
                ]
            };
            result = await api.createVoiceCall(voiceCallFieldValues);
            break;
        default:
            SCVLoggingUtil.warn("invokeTelephonyIntegrationApi.handler.handler", SCVLoggingUtil.EVENT_TYPE.VOICECALL, "Unsupported method", {});
            throw new Error(`Unsupported method: ${methodName}`);
    }

    return result;
};

