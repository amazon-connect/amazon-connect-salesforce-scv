const UtilityBarHelperConnector = (function(exports) {
    'use strict'

    function init(lightningHostname, ccpUrl) {
        const ccpContainer = document.getElementById('ccpContainer')

        if (!ccpContainer) {
            console.error('UtilityBarHelper', 'Unable to initialize CCP. Container element [ccpContainer] not found.')
            return
        }

        const ccpConfig = {
            ccpUrl: ccpUrl,
            softphone: {
                disableRingtone: true,
                allowFramedSoftphone: false
            },
            chat: {
                disableRingtone: true
            },
            task: {
                disableRingtone: true
            },
            ccpLoadTimeout: 3000,
            loginPopup: false
        }

        subscribeToOmniChannelEvents(lightningHostname, ccpContainer, ccpConfig)
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

    function subscribeToOmniChannelEvents(lightningHostname, ccpContainer, ccpConfig) {
        window.addEventListener('message', event => {
            if (lightningHostname === event.origin && event.data) {
                switch (event.data.method) {
                    case 'agentLogin':
                        if (!connect.core.initialized) {
                            connect.core.initCCP(ccpContainer, ccpConfig)
                            subscribeToConnectAgentEvents(lightningHostname)
                            connect.core.onInitialized(() => console.info('Successfully initialized CCP and subscribed to agent and omni-channel events'))
                        }
                        break
                }
            }
        })
    }

    exports.init = init

    return exports
})({})

