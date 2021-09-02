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

    def print_table(self,worksheet): 
        print(self.configuration_book.read_table(worksheet))

    def build_network_config(self):
        self.configuration_book.check_multi_network()
    
    def create_net_class_list(self):

        net_class_list = []
        key_found = 0
        key_to_remove = 0
        sub_index = 0
        multi_sub_index = 0

        multi_net_dic = self.configuration_book.check_multi_network()
        net_class_xl_format = self.configuration_book.read_table("Network Classes")
        for index in range(len(net_class_xl_format)):

            # network_name = self.configuration_book.get_network_name(index)
            # network_subnet = self.configuration_book.get_network_address(index)
            # network_mask = self.configuration_book.get_network_mask(index)

            network_name, network_subnet, network_mask = self.configuration_book.get_network_entry_details(index)

            for net_name_key in multi_net_dic.keys():
                #print(net_name_key)
                if network_name == net_name_key and key_found == 0:
                    key_found = 1
                    sub_index = 0
                    multi_sub_index = multi_net_dic[net_name_key]
                    key_to_remove = net_name_key
                    print(multi_sub_index)
                    print(key_to_remove)

            if key_found == 1:
                multi_net_dic.pop(key_to_remove)
            key_found = 0

            if sub_index < multi_sub_index:
                net_class_list.append(create_single_net_dic(
                    network_name, network_subnet, sub_index, network_mask))
                sub_index += 1
            else:
                sub_index = 0
                net_class_list.append(create_single_net_dic(
                    network_name, network_subnet, sub_index, network_mask))
                        
        #print(list_of_net)
        return net_class_list

    def create_BDoS_Profile_dic(self):
        BDoS_Profile_list = []
        net_class_xl_format = self.configuration_book.read_table(
            "Policy Editor")

        for index in range(len(net_class_xl_format)):
            BDoS_name,BDos_BW = self.configuration_book.get_BDoS_profile_details(
                index)
            if math.isnan(BDos_BW) == False:
                print(BDoS_name, BDos_BW)
                BDoS_Profile_list.append(
                    create_single_BDoS_dic(BDoS_name, int(BDos_BW)))
        
        return BDoS_Profile_list
    
    def create_DNS_Profile_dic(self):
        DNS_Profile_list = []
        net_class_xl_format = self.configuration_book.read_table(
            "Policy Editor")

        for index in range(len(net_class_xl_format)):
            DNS_profile_name, DNS_Expected_QPS, DNS_Max_QPS = self.configuration_book.get_DNS_profile_details(
                index)
            if math.isnan(DNS_Expected_QPS) == False:
                print(DNS_Expected_QPS)
                DNS_Profile_list.append(
                    create_single_DNS_dic(DNS_profile_name, int(DNS_Expected_QPS), int(DNS_Max_QPS)))
        
        return DNS_Profile_list

    def create_Syn_Profile_dic(self):
        # Function Description:
            # Creats List of Tuples for Syn Flood Profile configuration
            # [0] - Syn Profile configuarion
            # [1] - Syn Application paramater configuarion 
     
        Syn_Profile_list = []
        Syn_Profile_xl_format = self.configuration_book.read_table(
            "Policy Editor")

        for index in range(len(Syn_Profile_xl_format)):
            application_type = self.configuration_book.get_application_type(
                index)
            Policy_Name = self.configuration_book.get_Policy_Name(
                index)
            if application_type != False and Policy_Name != False:
               Syn_Profile_list.append(
                    create_single_Syn_dic(Policy_Name, application_type))
        return Syn_Profile_list

    def create_OOS_Profile_dic(self):
        # Function Description:
            # Creats List of dictorney OOS Profile configuration

        OOS_Profile_list = []
        OOS_Profile_xl_format = self.configuration_book.read_table(
            "Policy Editor")

        for index in range(len(OOS_Profile_xl_format)):
            Policy_Name = self.configuration_book.get_Policy_Name(
                index)
            if Policy_Name != False:
               OOS_Profile_list.append(
                   create_single_OOS_dic(Policy_Name))
        return OOS_Profile_list

    def create_AS_Profile_dic(self):
        # Function Description:
        # Creats List of dictorney AS Profile configuration

        AS_Profile_list = []
        AS_Profile_xl_format = self.configuration_book.read_table(
            "Policy Editor")

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
        ERT_Profile_xl_format = self.configuration_book.read_table(
            "Policy Editor")

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
        GEO_Profile_xl_format = self.configuration_book.read_table(
            "Policy Editor")

        for index in range(len(GEO_Profile_xl_format)):
            Policy_Name = self.configuration_book.get_Policy_Name(
                index)
            if Policy_Name != False:
               GEO_Profile_list.append(
                   create_single_GEO_dic(Policy_Name))
        return GEO_Profile_list

    def create_HTTPS_Profile_dic(self):
        # Function Description:
        # Creats List of dictorney HTTPS Profile configuration

        HTTPS_Profile_list = []
        HTTPS_Profile_xl_format = self.configuration_book.read_table(
            "Policy Editor")

        for index in range(len(HTTPS_Profile_xl_format)):
            Policy_Name = self.configuration_book.get_Policy_Name(
                index)
            if Policy_Name != False:
               HTTPS_Profile_list.append(
                   create_single_HTTPS_dic(Policy_Name))
        return HTTPS_Profile_list

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

def create_single_HTTPS_dic(HTTPS_Profile_name):
    HTTPS_profile_body = {
        "rsHttpsFloodProfileName": f"{HTTPS_Profile_name}_auto_HTTPS",
        "rsHttpsFloodProfileAction": "1",
        "rsHttpsFloodProfileSelectiveChallenge": "1",
        "rsHttpsFloodProfileRateLimitStatus": "1",
        "rsHttpsFloodProfileRateLimit": "250",
        "rsHttpsFloodProfileCollectiveChallenge": "2",
        "rsHttpsFloodProfileFullSessionDecryption": "1",
        "rsHttpsFloodProfileChallengeMethod": "1",
        "rsHttpsFloodProfilePacketReporting": "1"
    }
    return HTTPS_profile_body

d1 = Config_Convertor_Handler()
#d1.print_table("Network Classes")
#d1.create_net_class_list()
#d1.create_BDoS_Profile_dic()
#d1.create_Syn_Profile_dic()
