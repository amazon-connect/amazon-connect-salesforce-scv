'use strict';

const SCVLoggingUtil = require('./SCVLoggingUtil.js');
const api = require('./sfRestApi.js');
const queryEngine = require('./queryEngine.js');
const utils = require('./utils.js');
const flatten = require('flat');

// --------------- Events -----------------------

// invoked by invoking lambda through amazon connect
async function dispatch_query(soql, event){
    const parameters = event.Details.Parameters;
    let response;
    try {
        const queryResult = await queryEngine.invokeQuery(soql, parameters);
        return flatten(queryResult);
    }
    catch (e) {
        response = {
            statusCode: e.response.status ? e.response.status : 500,
            result: e
        }
    }
    return flatten(response);
}

async function dispatch_search(sosl){
    const searchResult = await api.searchRecord(sosl);
    if (searchResult.length == 1){
        return flatten(searchResult[0])
    }else{
        return searchResult
    }
}

// --------------- Main handler -----------------------
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
    
    const { methodName, objectApiName, recordId, soql, sosl } = event.Details.Parameters;

    switch (methodName) {
        case 'createRecord':
            result = await api.createRecord(utils.formatObjectApiName(objectApiName), 
                                            utils.getSObjectFieldValuesFromConnectLambdaParams(event.Details.Parameters));
            break;
        case 'updateRecord':
            result = await api.updateRecord(utils.formatObjectApiName(objectApiName), recordId, 
                                            utils.getSObjectFieldValuesFromConnectLambdaParams(event.Details.Parameters));
            break;
        case 'queryRecord':
            result = dispatch_query(soql, event);
            break;
        case 'searchRecord':
            result = dispatch_search(sosl);
            break;
        default:
            SCVLoggingUtil.warn("invokeSfRestApi.handler.handler", SCVLoggingUtil.EVENT_TYPE.VOICECALL, "Unsupported method", {});
            throw new Error(`Unsupported method: ${methodName}`);
    }

    if(result.success === false){
        throw new Error(result.errorMessage);
    } else
        return result;
};
