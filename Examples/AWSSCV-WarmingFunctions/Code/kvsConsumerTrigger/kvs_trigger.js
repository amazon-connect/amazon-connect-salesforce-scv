/**********************************************************************************************************************
 *  Lambda function to trigger real time transcription service in Java                                                *
 **********************************************************************************************************************/
'use strict';
const AWS = require('aws-sdk');
const SCVLoggingUtil = require('./SCVLoggingUtil.js');

AWS.config.correctClockSkew = true;
const lambda = new AWS.Lambda();

exports.handler = (event, context, callback) => {
    console.log("SCV - kvs_trigger.handler: function invoked");
    let result = {};
    
    // BEGIN AWS modification for EventBridge
    let eventSource = event.source || 'undefined';
    if (eventSource == 'aws.events') {
        result = {'eventStatusCode': 200,'eventResponse' : 'warm', 'eventType' : 'EventBridge'};
        console.log(result)
        return result
    }
    // END AWS modification for EventBridge

    let payload = "";
    let languageCodeSelected = "en-US";

    if (typeof event.Details.ContactData.Attributes.languageCode !== 'undefined' && event.Details.ContactData.Attributes.languageCode !== null) {
        languageCodeSelected = event.Details.ContactData.Attributes.languageCode;
    }

    payload = {
        streamARN: event.Details.ContactData.MediaStreams.Customer.Audio.StreamARN,
        startFragmentNum: event.Details.ContactData.MediaStreams.Customer.Audio.StartFragmentNumber,
        audioStartTimestamp: event.Details.ContactData.MediaStreams.Customer.Audio.StartTimestamp,
        customerPhoneNumber: event.Details.ContactData.CustomerEndpoint.Address,
        voiceCallId: event.Details.ContactData.InitialContactId,
        languageCode: languageCodeSelected,
        // These default to true for backwards compatability purposes
        streamAudioFromCustomer: event.Details.ContactData.Attributes.streamAudioFromCustomer !== "false",
        streamAudioToCustomer: event.Details.ContactData.Attributes.streamAudioToCustomer !== "false",
        instanceARN: event.Details.ContactData.InstanceARN
    };

    const params = {
        // not passing in a ClientContext
        'FunctionName': process.env.transcriptionFunction,
        // InvocationType is RequestResponse by default
        // LogType is not set so we won't get the last 4K of logs from the invoked function
        // Qualifier is not set so we use $LATEST
        'InvokeArgs': JSON.stringify(payload)
    };

    lambda.invokeAsync(params, function(err, data) {
        if (err) {
            throw (err);
        } else {
            if (callback)
                callback(null, buildResponse());
            else
                SCVLoggingUtil.info("kvs_trigger.handler.handler", SCVLoggingUtil.EVENT_TYPE.TRANSCRIPTION, "nothing to callback so letting it go");
        }
    });

    callback(null, buildResponse());
};

function buildResponse() {
    return {
        // Async Java lambda is trigger, return "Success" for now
        lambdaResult:"Success"
    };
}
