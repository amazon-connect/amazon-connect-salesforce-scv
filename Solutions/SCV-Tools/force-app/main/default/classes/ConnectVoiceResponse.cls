/*
 *
 * Copyright 2024 Amazon.com, Inc. or its affiliates. All Rights Reserved.
 * Licensed under the Apache License Version 2.0 (the 'License'). You may not
 * use this file except in compliance with the License. A copy of the License
 * is located at:
 *
 *          http://www.apache.org/licenses/
 *
 * or in the 'license' file accompanying this file. This file is distributed on
 * an 'AS IS' BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, express or
 * implied. See the License for the specific language governing permissions and
 * limitations under the License.
 *
 */

public with sharing class ConnectVoiceResponse {
    public Long total;
    public ContactCenter[] contactCenters;

    public class ContactCenter {
        public String adapterUrl;
        public String callCenterId;
        public String callCenterName;
        public String callCenterType;
        public String connectedAppId;
        public String currentCCVersion;
        public String displayName;
        public String identityUrl;
        public String instanceId;
        public String instanceName;
        public String instanceRecordingRole;
        public Boolean isACGREnabled;
        public Boolean presenceStatusSyncAccess;
        public String region;
        public String relayState;
        public String restApiConnectedAppId;
        public String telephonyIntegrationKeyPairExpDate;
        public String telephonyProvider;
        public String transferTargetForOmniFlowTransfer;
        public String transferTargetForOmniFlowTransferDisplayName;
        public String trustedRoleARN;
        public Boolean universalCallRecordingAccess;
    }
}