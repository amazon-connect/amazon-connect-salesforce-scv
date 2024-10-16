

public with sharing class UtilityBarHelperController {
    /**
         * @return The Visualforce hostname.  This value is without any namespace in the case of managed package content.
         */
    @AuraEnabled(Cacheable=true)
    public static String getVisualforceHostname() {
        return System.DomainCreator.getVisualforceHostname(null);
    }

    /**
     * @return The Lightning hostname.
     */
    @AuraEnabled(Cacheable=true)
    public static String getLightningHostname() {
        return System.DomainCreator.getLightningHostname();
    }

    /**
     * @return The org's MyDomain hostname.
     */
    @AuraEnabled(Cacheable=true)
    public static String getOrgMyDomainHostname() {
        return System.DomainCreator.getOrgMyDomainHostname();
    }

    /**
     * @return The Lightning container component hostname.
     */
    @AuraEnabled(Cacheable=true)
    public static String getLightningContainerComponentHostname() {
        return System.DomainCreator.getLightningContainerComponentHostname(null);
    }

    @AuraEnabled(Cacheable=true)
    public static String getConnectVoiceContactCenterConfig(Id callCenterId) {
        String config = null;

        try {
            Http http = new Http();

            HttpRequest req = new HttpRequest();
            req.setMethod('GET');
            req.setEndpoint('callout:SCV_CONNECT_VOICE_API_NC/services/data/v62.0/connect/voice/contactcenter/' + callCenterId + '?vendor_type=AMAZON&offset=0');
            req.setHeader('Accept', 'application/json');

            HttpResponse res = http.send(req);

            config = res.getBody();
        }
        catch (Exception e) {
            throw e;
        }

        return config;
    }

    @AuraEnabled(Cacheable=true)
    public static String getAmazonConnectInstanceName() {
        String instanceName = null;

        try {
            Id callCenterId = [SELECT CallCenterId FROM User WHERE Id = :UserInfo.getUserId()].CallCenterId;

            if (callCenterId != null) {
                ConnectVoiceResponse.ContactCenter cc = (ConnectVoiceResponse.ContactCenter) JSON.deserialize(getConnectVoiceContactCenterConfig(callCenterId), ConnectVoiceResponse.ContactCenter.class);

                if (cc != null) {
                    instanceName = cc.instanceName;
                }
            }
        }
        catch (Exception e) {
            throw e;
        }

        return instanceName;
    }
}