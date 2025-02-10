
public with sharing class HelperController {
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
}