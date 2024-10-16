({
    doInit : function(cmp, event, helper) {
        const baseUtilityLabel = cmp.get('v.baseUtilityLabel');
        const action = cmp.get('c.getVisualforceHostname');
        action.setCallback(this, response => {
            if (response.getState() === 'SUCCESS') {
                const vfHost = response.getReturnValue();
                cmp.set('v.vfHost', vfHost);
            }
        })
        $A.enqueueAction(action);

        if (window && window.addEventListener != null) {
            window.addEventListener('message',
                $A.getCallback((postMessageEvent) => {
                    if (postMessageEvent.data.name === 'agent-event') {
                        const agentState = postMessageEvent.data.payload.agentState;

                        cmp.set('v.agentState', agentState);

                        const utilityBar = cmp.find('utilityBar');
                        utilityBar.getEnclosingUtilityId()
                            .then(utilityId => {
                                const label = baseUtilityLabel + ' - ' + agentState;

                                if (agentState === 'MissedCallAgent' ) {
                                    utilityBar.setPanelHeaderIcon({
                                        utilityId: utilityId,
                                        icon: 'missed_call',
                                        options: {
                                            iconVariant: 'error'
                                        }
                                    })

                                    utilityBar.setUtilityIcon({
                                        utilityId: utilityId,
                                        icon: 'missed_call',
                                        options: {
                                            iconVariant: 'error'
                                        }
                                    })
                                }
                                else {
                                    utilityBar.setPanelHeaderIcon({
                                        utilityId: utilityId,
                                        icon: 'wifi',
                                        options: {
                                            iconVariant: 'success'
                                        }
                                    });

                                    utilityBar.setUtilityIcon({
                                        utilityId: utilityId,
                                        icon: 'wifi',
                                        options: {
                                            iconVariant: 'success'
                                        }
                                    });
                                }

                                utilityBar.setPanelHeaderLabel({
                                    utilityId: utilityId,
                                    label: label
                                });

                                utilityBar.setUtilityLabel({
                                    utilityId: utilityId,
                                    label: label
                                });
                            })
                            .catch(error => {
                                console.error(error);
                            });
                    }
                }))
        }
    },

    onAgentLogin: function(cmp, event, helper) {
        helper.postMessageToChild(cmp, {
            method: "agentLogin"
        });
    },

    toggleStatus: function(cmp, event, helper) {
        const omniToolkit = cmp.find('omniToolkit');

        omniToolkit.getServicePresenceStatusId()
            .then(result => {
                const statusId = result.statusId;

                omniToolkit.logout()
                    .then(logoutResult => {
                        omniToolkit.login({ statusId: statusId })
                            .then(loginResult => {
                            })
                            .catch(err => {
                                console.error(err);
                            });
                    })
                    .catch(err => {
                        console.error(err);
                    });
            })
            .catch(err => {
                console.error(err)
            });
    }
});