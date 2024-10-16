const Connector = (function(exports) {
    'use strict'

    const OMNI_CHANNEL_AGENT_LOGIN = "agentLogin";

    function init(lightningHostname, ccpUrl, loginUrl) {
        const ccpContainer = document.getElementById('ccpContainer')

        if (!ccpContainer) {
            console.error('Unable to initialize CCP. Container element [ccpContainer] not found.')
            return
        }

        connect.getLog().setLogLevel(connect.LogLevel.ERROR)

        const ccpConfig = {
            ccpUrl: ccpUrl,
            loginUrl: loginUrl,
            softphone: {
                disableRingtone: true,
                allowFramedSoftphone: false
            },
            chat: {
                "disableRingtone": true
            },
            task: {
                "disableRingtone": true
            },
            ccpLoadTimeout: 3000,
            loginPopup: false
        }

        subscribeToOmniChanelEvents(lightningHostname, ccpContainer, ccpConfig)
    }

    function subscribeToConnectAgentEvents(lightningHostname) {
        connect.agent((agent) => {
            try {
                window.parent.postMessage({ name: 'agent-event', payload: { agentState: agent.getState().name } }, lightningHostname)
            }
            catch (err) {
                console.error(err)
            }

            agent.onRefresh((agent) => {
                window.parent.postMessage({ name: 'agent-event', payload: { agentState: agent.getState().name } }, lightningHostname)
            })

            agent.onStateChange((agentStateChange) => {
                window.parent.postMessage({ name: 'agent-event', payload: { agentState: agentStateChange.newState } }, lightningHostname)
            })
        })
    }

    function subscribeToOmniChanelEvents(lightningHostname, ccpContainer, ccpConfig) {
        window.addEventListener('message', event => {
            if (lightningHostname === event.origin && event.data) {
                switch (event.data.method) {
                    case OMNI_CHANNEL_AGENT_LOGIN:
                        onAgentLogin(lightningHostname, ccpContainer, ccpConfig)
                        break
                }
            }
        })
    }

    function onAgentLogin(lightningHostname, ccpContainer, ccpConfig) {
        if (!connect.core.initialized) {
            connect.core.initCCP(ccpContainer, ccpConfig)
            subscribeToConnectAgentEvents(lightningHostname)
            connect.core.onInitialized(() => console.info('Successfully initialized CCP and subscribed to agent and omni-channel events'))
        }
    }

    exports.init = init

    return exports
})({})

