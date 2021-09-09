from typing import Protocol
import pandas
import requests
import json
import time
import timeit
import math
from Excel_Handler import Excel_Handler

class Config_Convertor_Handler:
    def __init__(self):
        self.configuration_book = Excel_Handler("server_test.xlsm")
        self.policy_editor_book = self.configuration_book.read_table("Policy Editor")
        self.network_class_book = self.configuration_book.read_table(
            "Network Classes")
    def print_table(self,worksheet): 
        print(self.configuration_book.read_table(worksheet))

    def build_network_config(self):
        self.configuration_book.check_multi_network()
    
    def create_net_class_list(self):

        net_class_list = []
        key_found_sub_index = 0
        key_to_remove = 0
        sub_index = 0
        multi_sub_index = 0

        multi_net_dic = self.configuration_book.check_multi_network()
        net_class_xl_format = self.network_class_book
        
        for index in range(len(net_class_xl_format)):

            network_name, network_subnet, network_mask = self.configuration_book.get_network_entry_details(index)

            for net_name_key in multi_net_dic.keys():
                #IF There is a netowrk call with multiple sub-indexes:
                if network_name == net_name_key and key_found_sub_index == 0:
                    key_found_sub_index = 1
                    sub_index = 0
                    multi_sub_index = multi_net_dic[net_name_key]
                    key_to_remove = net_name_key
                    print(multi_sub_index)
                    print(key_to_remove)

            if key_found_sub_index == 1:
                #Remove the Entry with sub-indexes from dictionary.
                multi_net_dic.pop(key_to_remove)
            key_found_sub_index = 0

            if sub_index < multi_sub_index:
                net_class_list.append(create_single_net_dic(
                    network_name, network_subnet, sub_index, network_mask))
                sub_index += 1
            else:
                # Network Class with only 1 Entry:
                sub_index = 0
                net_class_list.append(create_single_net_dic(
                    network_name, network_subnet, sub_index, network_mask))
                        
        #print(list_of_net)
        return net_class_list

    def create_BDoS_Profile_dic(self):
        BDoS_Profile_list = []
        # net_class_xl_format = self.configuration_book.read_table(
        #     "Policy Editor")
        BDoS_Pro_xl_format = self.policy_editor_book

        for index in range(len(BDoS_Pro_xl_format)):
            Policy_Name, BDos_BW = self.configuration_book.get_BDoS_profile_details(
                index)
            Application = self.configuration_book.get_application_type(index)
            if Policy_Name != False:
                if math.isnan(BDos_BW) == False:
                    if protection_per_application_check(Application) or Application == "DNS":
                        BDoS_Profile_list.append(
                            create_single_BDoS_dic(Policy_Name, int(BDos_BW)))
        
        return BDoS_Profile_list
    
    def create_DNS_Profile_dic(self):
        DNS_Profile_list = []
        # net_class_xl_format = self.configuration_book.read_table(
        #     "Policy Editor")
        Dns_Pro_xl_format = self.policy_editor_book
        
        for index in range(len(Dns_Pro_xl_format)):
            Policy_Name, DNS_Expected_QPS, DNS_Max_QPS = self.configuration_book.get_DNS_profile_details(
                index)
            Application_type = self.configuration_book.get_application_type(index)
            if Policy_Name != False:
                if Application_type == "DNS":
                    if math.isnan(DNS_Expected_QPS) == False and math.isnan(DNS_Max_QPS) == False:
                        #print(DNS_Expected_QPS)
                        DNS_Profile_list.append(
                            create_single_DNS_dic(Policy_Name, int(DNS_Expected_QPS), int(DNS_Max_QPS)))
        
        return DNS_Profile_list

    def create_Syn_Profile_dic(self):
        # Function Description:
            # Creats List of Tuples for Syn Flood Profile configuration
            # [0] - Syn Profile configuarion
            # [1] - Syn Application paramater configuarion 
     
        Syn_Profile_list = []
        # Syn_Profile_xl_format = self.configuration_book.read_table(
        #     "Policy Editor")
        Syn_Profile_xl_format = self.policy_editor_book

        for index in range(len(Syn_Profile_xl_format)):
            Application_type = self.configuration_book.get_application_type(
                index)
            Policy_Name = self.configuration_book.get_Policy_Name(
                index)
            if Policy_Name != False:
                if protection_per_application_check(self.configuration_book.get_application_type(index)):
                        Syn_Profile_list.append(
                                create_single_Syn_dic(Policy_Name, Application_type))
        return Syn_Profile_list

    def create_Syn_App_dic(self):
        Syn_App_list = []
        #Syn_App_list.append(create_single_Syn_App("Mail"))
        Syn_App_list.append(create_single_Syn_App("DNS"))

        return Syn_App_list

    def create_OOS_Profile_dic(self):
        # Function Description:
            # Creats List of dictorney OOS Profile configuration

        OOS_Profile_list = []
        # OOS_Profile_xl_format = self.configuration_book.read_table(
        #     "Policy self.policy_editor_book")
        OOS_Profile_xl_format = self.policy_editor_book

        for index in range(len(OOS_Profile_xl_format)):
            Policy_Name = self.configuration_book.get_Policy_Name(
                index)
            if Policy_Name != False:
                if protection_per_application_check(self.configuration_book.get_application_type(index)):
                    OOS_Profile_list.append(
                        create_single_OOS_dic(Policy_Name))
        return OOS_Profile_list

    def create_AS_Profile_dic(self):
        # Function Description:
        # Creats List of dictorney AS Profile configuration

        AS_Profile_list = []
        # AS_Profile_xl_format = self.configuration_book.read_table(
        #     "Policy Editor")
        AS_Profile_xl_format = self.policy_editor_book

        for index in range(len(AS_Profile_xl_format)):
            Policy_Name = self.configuration_book.get_Policy_Name(
                index)
            if Policy_Name != False:
               AS_Profile_list.append(
                   create_single_AS_dic(Policy_Name))
        return AS_Profile_list

    def create_ERT_Profile_dic(self):
        # Function Description:
        # Creats List of dictorney ERT Profile configuration

        ERT_Profile_list = []
        # ERT_Profile_xl_format = self.configuration_book.read_table(
        #     "Policy Editor")
        ERT_Profile_xl_format = self.policy_editor_book

        for index in range(len(ERT_Profile_xl_format)):
            Policy_Name = self.configuration_book.get_Policy_Name(
                index)
            if Policy_Name != False:
               ERT_Profile_list.append(
                   create_single_ERT_dic(Policy_Name))
        return ERT_Profile_list    

    def create_GEO_Profile_dic(self):
        # Function Description:
        # Creats List of dictorney GEO Profile configuration

        GEO_Profile_list = []
        # GEO_Profile_xl_format = self.configuration_book.read_table(
        #     "Policy Editor")
        GEO_Profile_xl_format = self.policy_editor_book

        for index in range(len(GEO_Profile_xl_format)):
            Policy_Name = self.configuration_book.get_Policy_Name(
                index)
            if Policy_Name != False:
               GEO_Profile_list.append(
                   create_single_GEO_dic(Policy_Name))
        return GEO_Profile_list

    def create_Singature_Profile_dic(self):
        # Function Description:
        # Creats List of dictorney Sig Profile configuration
        #https://10.213.17.49/mgmt/device/byip/10.213.17.52/config/rsIDSSignaturesProfilesTable/dns_custom/1/Complexity/Low/
        Sig_Profile_list = []
        # Sig_Profile_xl_format = self.configuration_book.read_table(
        #     "Policy Editor")
        Sig_Profile_xl_format = self.policy_editor_book

        for index in range(len(Sig_Profile_xl_format)):
            Policy_Name = self.configuration_book.get_Policy_Name(
                index)
            if Policy_Name != False:
               Sig_Profile_list.append(
                   create_custom_signature(Policy_Name))
        return Sig_Profile_list
        
    def create_HTTPS_Profile_dic(self):
        # Function Description:
        # Creats List of dictorney HTTPS Profile configuration

        HTTPS_Profile_list = []
        # HTTPS_Profile_xl_format = self.configuration_book.read_table(
        #     "Policy Editor")
        HTTPS_Profile_xl_format = self.policy_editor_book

        for index in range(len(HTTPS_Profile_xl_format)):
            Policy_Name = self.configuration_book.get_Policy_Name(
                index)
            full_inspection_flag = self.configuration_book.get_Full_Inspection_Flag_Status(
                index)
            if Policy_Name != False:
               HTTPS_Profile_list.append(
                   create_single_HTTPS_dic(Policy_Name,full_inspection_flag))
        return HTTPS_Profile_list

    def create_Protections_Per_Policy_dic(self):
        # Maybe Delete
        # Function Description:
        # Creats List of protections per policy configuration
        # basic app = ["HTTP", "HTTPS", "FTP", "SMTP"]
        Policy_priorty = 300
        signature_list = ["DoS-All", "Corp-DMZ-Web", "Corp-DMZ-Mail", "dns_custom_profile"]
        Protection_per_policy_list = []
        protections_xl_format = self.policy_editor_book
        for index in range(len(protections_xl_format)):
            application_type = self.configuration_book.get_application_type(
                index)
            Policy_Name = self.configuration_book.get_Policy_Name(index)
            dest_net_per_policy = protections_xl_format[index]["DST Networks Name"]
            if Policy_Name != False:
                policy_type = protection_per_policy_check(self.configuration_book.get_application_type(index))
                if policy_type == "basic_app":
                    #print(application_type)
                    #Basic Application Policy Section:
                    if application_type == "HTTP" or application_type == "HTTPS":
                        signature_selected = signature_list[1]
                    elif application_type == "SMTP":
                        signature_selected = signature_list[2]
                    elif application_type == "DNS":
                        signature_selected = signature_list[3]
                    elif application_type == "Global": 
                        signature_selected = signature_list[0]
                        
                    Protection_per_policy_list.append(
                        create_single_Policy_dic(Policy_Name, policy_type, Policy_priorty, signature_selected,dest_net_per_policy))
                
                if policy_type == "DNS_app":
                    signature_selected = signature_list[1]
                    Protection_per_policy_list.append(
                        create_single_Policy_dic(Policy_Name, policy_type, Policy_priorty, signature_selected, dest_net_per_policy))
            Policy_priorty +=5
        #print(Protection_per_policy_list)
        return Protection_per_policy_list
            
def create_single_Syn_dic(Syn_Profile_name, application_type_list):
        
        syn_profile_body = {
            "rsIDSSynProfilesParamsName": f"{Syn_Profile_name}_auto_syn",
            "rsIDSSynProfileTCPResetStatus": "1",
            "rsIDSSynProfilesParamsWebEnable": "1",
            #Enables JavaScript Challenge:
            "rsIDSSynProfilesParamsWebMethod": "2"
        }
        syn_paramaters_body = {
            "rsIDSSynProfilesName": f"{Syn_Profile_name}_auto",
            "rsIDSSynProfileServiceName": application_type_list,
            "rsIDSSynProfileType": "3"
        }

        return syn_profile_body, syn_paramaters_body

def create_single_Syn_App(application_type):
    
    # For Clean DP Installtion
    # if application_type == "Mail":
    #     app_port = "smtp"
    #     attack_id = "500001"
    # if application_type == "DNS":
    #     app_port = "dns"
    #     attack_id = "500002"
    
    #Other for test:
    if application_type == "Mail":
        app_port = "smtp"
        attack_id = "500013"
    if application_type == "DNS":
        app_port = "dns"
        attack_id = "500013"

    application_body = {
        "rsIDSSYNAttackName": application_type,
        "rsIDSSYNAttackId": attack_id,
        "rsIDSSYNAttackSourceType": "3",
        "rsIDSSYNDestinationAppPortGroup": app_port,
        "rsIDSSYNAttackActivationThreshold": "2500",
        "rsIDSSYNAttackTerminationThreshold": "1500",
        "rsIDSSYNAttackRisk": "2"
    }

    return application_body

def create_single_AS_dic(AS_Profile_name):

    as_profile_body = {
        "rsIDSScanningProfilesName": f"{AS_Profile_name}_auto_as",
        "rsIDSScanningProfilesTCPState": "1",
        "rsIDSScanningProfilesUDPState": "1",
        "rsIDSScanningProfilesICMPState": "1",
        "rsIDSScanningProfilesAction": "1",
        "rsIDSScanningProfilesPacketTraceStatus": "1",
        "rsIDSScanningProfilesSensitivity": "2",
        "rsIDSScanningProfilesProbesThreshold": "90",
        "rsIDSScanningProfilesTrackingTime": "5",
        "rsIDSScanningProfilesLowToHighBypass": "1",
        "rsIDSScanningProfilesHighPortsResp": "2",
        "rsIDSScanningProfilesSinglePort": "2",
        "rsIDSScanningProfilesFootprintStrictness": "2"
    }

    return as_profile_body

def create_single_OOS_dic(OOS_Profile_name):

    oos_profile_body = {
        "rsSTATFULProfileName": f"{OOS_Profile_name}_auto_oos",
        "rsSTATFULProfileactThreshold": "5000",
        "rsSTATFULProfiletermThreshold": "4000",
        "rsSTATFULProfileGPAfterUpdatePolicyorIdleState": "30",
        "rsSTATFULProfilesynAckAllow": "1",
        "rsSTATFULProfilenoEntryForOOSpacketsInSTduringGP": "2",
        "rsSTATFULProfileEnableIdleState": "2",
        "rsSTATFULProfileIdleStateBandwidthThreshold": "10000",
        "rsSTATFULProfileIdleStateTimer": "10",
        "rsSTATFULProfileAction": "1",
        "rsSTATFULProfileRisk": "2",
        "rsSTATFULProfilePacketReportStatus": "2"
    }
    
    return oos_profile_body
    
def create_single_BDoS_dic(BDoS_Profile_Name, BDoS_Profile_BW):
    bdos_profile_body = {
        "rsNetFloodProfileName": f"{BDoS_Profile_Name}_auto_BDoS",
  						"rsNetFloodProfilePacketReportStatus": "1",
  						"rsNetFloodProfileTransparentOptimization": "2",
  						"rsNetFloodProfileAction": "1",
  						"rsNetFloodProfileTcpSynStatus": "1",
  						"rsNetFloodProfileTcpFinAckStatus": "1",
  						"rsNetFloodProfileTcpRstStatus": "1",
  						"rsNetFloodProfileTcpSynAckStatus": "1",
  						"rsNetFloodProfileTcpFragStatus": "1",
  						"rsNetFloodProfileUdpStatus": "1",
  						"rsNetFloodProfileUdpFragStatus": "1",
  						"rsNetFloodProfileIcmpStatus": "1",
  						"rsNetFloodProfileIgmpStatus": "1",
  						"rsNetFloodProfileBandwidthIn": BDoS_Profile_BW,
  						"rsNetFloodProfileBandwidthOut":  BDoS_Profile_BW,
  						"rsNetFloodProfileTcpInQuota": "0",
  						"rsNetFloodProfileTcpOutQuota": "0",
  						"rsNetFloodProfileUdpInQuota": "0",
  						"rsNetFloodProfileUdpOutQuota": "0",
  						"rsNetFloodProfileUdpFragInQuota": "0",
  						"rsNetFloodProfileUdpFragOutQuota": "0",
  						"rsNetFloodProfileIcmpInQuota": "0",
  						"rsNetFloodProfileIcmpOutQuota": "0",
  						"rsNetFloodProfileIgmpInQuota": "0",
  						"rsNetFloodProfileIgmpOutQuota": "0",
  						"rsNetFloodProfileLevelOfReuglarzation": "2",
  						"rsNetFloodProfileUdpExcludedPorts": "None",
  						"rsNetFloodProfileAdvUdpDetection": "2",
  						"rsNetFloodProfileAdvUdpLearningPeriod": "2",
  						"rsNetFloodProfileAdvUdpAttackHighEdgeOverride": "0.0",
  						"rsNetFloodProfileAdvUdpAttackLowEdgeOverride": "0.0",
  						"rsNetFloodProfileBurstEnabled": "1",
  						"rsNetFloodProfileNoBurstTimeout": "30",
  						"rsNetFloodProfileOverMitigationStatus": "2",
  						"rsNetFloodProfileOverMitigationThreshold": "25",
  						"rsNetFloodProfileLearningSuppressionThreshold": "25",
  						"rsNetFloodProfileFootprintStrictness": "1",
  						"rsNetFloodProfileRateLimit": "0",
  						"rsNetFloodProfileUserDefinedRateLimit": "0",
  						"rsNetFloodProfileUserDefinedRateLimitUnit": "0"
    }
    return bdos_profile_body

def create_single_net_dic(network_name, netowrk_subnet, sub_index, net_mask):

    single_net_class_dic = {
        "rsBWMNetworkName": f"{network_name}_auto",
        "rsBWMNetworkSubIndex": sub_index,
        "rsBWMNetworkMode": "1",
        "rsBWMNetworkAddress": netowrk_subnet,
        "rsBWMNetworkMask": net_mask
    }
    return single_net_class_dic
    
def create_single_DNS_dic(DNS_Profile_Name, Expect_QPS, Allow_Max):

    dns_profile_body = {
        "rsDnsProtProfileName": f"{DNS_Profile_Name}_auto_DNS",
        "rsDnsProtProfileAction": "1",
        "rsDnsProtProfilePacketReportStatus": "1",
        "rsDnsProtProfileDnsAStatus": "1",
        "rsDnsProtProfileDnsMxStatus": "1",
        "rsDnsProtProfileDnsPtrStatus": "1",
        "rsDnsProtProfileDnsAaaaStatus": "1",
        "rsDnsProtProfileDnsTextStatus": "1",
        "rsDnsProtProfileDnsSoaStatus": "1",
        "rsDnsProtProfileDnsNaptrStatus": "1",
        "rsDnsProtProfileDnsSrvStatus": "1",
        "rsDnsProtProfileDnsOtherStatus": "1",
        "rsDnsProtProfileExpectedQps": Expect_QPS,
        "rsDnsProtProfileMaxAllowQps": Allow_Max,
        "rsDnsProtProfileManualTriggerActThresh": "0",
        "rsDnsProtProfileManualTriggerActPeriod": "3",
        "rsDnsProtProfileManualTriggerTermThresh": "0",
        "rsDnsProtProfileManualTriggerTermPeriod": "3",
        "rsDnsProtProfileManualTriggerMaxQpsTarget": "0",
        "rsDnsProtProfileManualTriggerEscalatePeriod": "3",
        "rsDnsProtProfileLearningSuppressionThreshold": "0",
        "rsDnsProtProfileFootprintStrictness": "0"
    }
    return dns_profile_body

def create_single_ERT_dic(ERT_Profile_name):
    ERT_profile_body = {
        "rsErtAttackersFeedProfileName": f"{ERT_Profile_name}_auto_ERT",
        "rsErtAttackersFeedCatErtHighAction": "3",
        "rsErtAttackersFeedCatErtMediumAction": "1",
        "rsErtAttackersFeedCatErtLowAction": "1",
        "rsErtAttackersFeedCatTorHighAction": "3",
        "rsErtAttackersFeedCatTorMediumAction": "2",
        "rsErtAttackersFeedCatTorLowAction": "2",
        "rsErtAttackersFeedCatWebHighAction": "3",
        "rsErtAttackersFeedCatWebMediumAction": "1",
        "rsErtAttackersFeedCatWebLowAction": "1"
    }
    return ERT_profile_body

def create_single_GEO_dic(GEO_Profile_name):
    GEO_profile_body = {
        "rsGeoProfileName": f"{GEO_Profile_name}_auto_GEO",
        "rsGeoProfilePacketAction": "1",
        "rsGeoProfileReportAction": "1"
    }

    return GEO_profile_body

def create_custom_signature(Sig_Profile_name,application):

    if application == "DNS":    
        DNS_service_body = {
            "rsIDSSignaturesProfileName": "dns_custom_profile",
            "rsIDSSignaturesProfileRuleName": "1",
            "rsIDSSignaturesProfileRuleAttributeType": "Services",
            "rsIDSSignaturesProfileRuleAttributeName": "Network Services-DNS"
        }
        
        Complexity_low_body = {
            "rsIDSSignaturesProfileName": "dns_custom_profile",
            "rsIDSSignaturesProfileRuleName": "1",
            "rsIDSSignaturesProfileRuleAttributeType": "Complexity",
            "rsIDSSignaturesProfileRuleAttributeName": "Low"
        }
        return DNS_service_body, Complexity_low_body

def create_single_HTTPS_dic(HTTPS_Profile_name,full_inspection_flag):
   
    Full_inspection_value = 1 if full_inspection_flag == "Yes" else 2
    HTTPS_profile_body = {
        "rsHttpsFloodProfileName": f"{HTTPS_Profile_name}_auto_HTTPS",
        "rsHttpsFloodProfileAction": "1",
        "rsHttpsFloodProfileSelectiveChallenge": "1",
        "rsHttpsFloodProfileRateLimitStatus": "1",
        "rsHttpsFloodProfileRateLimit": "250",
        "rsHttpsFloodProfileCollectiveChallenge": "2",
        "rsHttpsFloodProfileFullSessionDecryption": Full_inspection_value,
        "rsHttpsFloodProfileChallengeMethod": "2",
        "rsHttpsFloodProfilePacketReporting": "1"
    }
    return HTTPS_profile_body

def protection_per_application_check(application_type):
    general_app_list = ["HTTP","HTTPS","FTP","SMTP"]
    if application_type in general_app_list:
        return True
    return False

def protection_per_policy_check(application_type):
    #Checks which application type the policy uses, and return the policy type
    general_app_list = ["HTTP", "HTTPS", "FTP", "SMTP"]
    if application_type in general_app_list:
        app_type_response = "basic_app"
        return app_type_response
    if application_type == "DNS":
        app_type_response = "DNS_app"
        return app_type_response
    if application_type == "Global":
        app_type_response = "Global"
        return app_type_response

def create_single_Policy_dic(Policy_Name, policy_type, policy_Priority, signature_profile, Dest_net,):
    
    if policy_type == "basic_app":
        Policy_basic_body = {
            "rsIDSNewRulesState": "1",
            "rsIDSNewRulesName": f"{Policy_Name}_BP",
            "rsIDSNewRulesAction": "1",
            "rsIDSNewRulesPriority": policy_Priority,
            "rsIDSNewRulesSource": "any",
            "rsIDSNewRulesDestination": f"{Dest_net}_auto",
            "rsIDSNewRulesPortmask": "",
            "rsIDSNewRulesDirection": "1",
            "rsIDSNewRulesVlanTagGroup": "",
            "rsIDSNewRulesProfileScanning": f"{Policy_Name}_auto_as",
            "rsIDSNewRulesProfileNetflood": f"{Policy_Name}_auto_BDoS",
            "rsIDSNewRulesProfileConlmt": "",
            "rsIDSNewRulesProfilePpsRateLimit": "",
            "rsIDSNewRulesProfileDNS": "",
            "rsIDSNewRulesProfileErtAttackersFeed": "",
            "rsIDSNewRulesProfileGeoFeed": "",
            "rsIDSNewRulesProfileHttpsflood": "",
            "rsIDSNewRulesProfileStateful":  f"{Policy_Name}_auto_oos",
            "rsIDSNewRulesProfileAppsec": signature_profile,
            "rsIDSNewRulesProfileSynprotection":  f"{Policy_Name}_auto_syn",
            "rsIDSNewRulesProfileTrafficFilters": "",
            "rsIDSNewRulesCdnHandling": "2",
            "rsIDSNewRulesCdnHandlingHttps": "1",
            "rsIDSNewRulesCdnHandlingSig": "1",
            "rsIDSNewRulesCdnHandlingSyn": "1",
            "rsIDSNewRulesCdnHandlingTF": "1",
            "rsIDSNewRulesCdnAction": "2",
            "rsIDSNewRulesCdnTrueClientIpHdr": "1",
            "rsIDSNewRulesCdnXForwardedForHdr": "1",
            "rsIDSNewRulesCdnForwardedHdr": "2",
            "rsIDSNewRulesCdnTrueIpCustomHdr": "",
            "rsIDSNewRulesCdnHdrNotFoundFallback": "1",
            "rsIDSNewRulesPacketReportingEnforcement": "1"
        }
    
        return Policy_basic_body
    
    if policy_type == "DNS_app":
        Policy_DNS_body= {
            "rsIDSNewRulesState": "1",
            "rsIDSNewRulesName": f"{Policy_Name}_BP",
            "rsIDSNewRulesAction": "1",
            "rsIDSNewRulesPriority": policy_Priority,
            "rsIDSNewRulesSource": "any",
            "rsIDSNewRulesDestination":f"{Dest_net}_auto",
            "rsIDSNewRulesPortmask": "",
            "rsIDSNewRulesDirection": "1",
            "rsIDSNewRulesVlanTagGroup": "",
            "rsIDSNewRulesProfileScanning": "",
            "rsIDSNewRulesProfileNetflood":  f"{Policy_Name}_auto_BDoS",
            "rsIDSNewRulesProfileConlmt": "",
            "rsIDSNewRulesProfilePpsRateLimit": "",
            "rsIDSNewRulesProfileDNS": f"{Policy_Name}_auto_DNS",
            "rsIDSNewRulesProfileErtAttackersFeed": "",
            "rsIDSNewRulesProfileGeoFeed": "",
            "rsIDSNewRulesProfileHttpsflood": "",
            "rsIDSNewRulesProfileStateful": "",
            "rsIDSNewRulesProfileAppsec": signature_profile,
            "rsIDSNewRulesProfileSynprotection": "",
            "rsIDSNewRulesProfileTrafficFilters": "",
            "rsIDSNewRulesCdnHandling": "2",
            "rsIDSNewRulesCdnHandlingHttps": "1",
            "rsIDSNewRulesCdnHandlingSig": "1",
            "rsIDSNewRulesCdnHandlingSyn": "1",
            "rsIDSNewRulesCdnHandlingTF": "1",
            "rsIDSNewRulesCdnAction": "2",
            "rsIDSNewRulesCdnTrueClientIpHdr": "1",
            "rsIDSNewRulesCdnXForwardedForHdr": "1",
            "rsIDSNewRulesCdnForwardedHdr": "2",
            "rsIDSNewRulesCdnTrueIpCustomHdr": "",
            "rsIDSNewRulesCdnHdrNotFoundFallback": "1",
            "rsIDSNewRulesPacketReportingEnforcement": "1"
        }
        return Policy_DNS_body


d1 = Config_Convertor_Handler()
#d1.print_table("Network Classes")
#d1.create_net_class_list()
#d1.create_BDoS_Profile_dic()
#d1.create_Syn_Profile_dic()
#d1.create_Protections_Per_Policy_dic()

