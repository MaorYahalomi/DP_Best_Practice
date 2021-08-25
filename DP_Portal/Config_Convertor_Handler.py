import pandas
import requests
import json
import time
import timeit
import math
from Excel_Handler import Excel_Handler

class Config_Convertor_Handler:
    def __init__(self):
        self.configuration_book =  Excel_Handler("Policy_Editor_micro_new_V7.xlsm")

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
        
        #print(BDoS_Profile_list)
        return BDoS_Profile_list

def create_single_BDoS_dic(BDoS_Profile_Name, BDoS_Profile_BW):
    bdos_profile_body = {
        "rsNetFloodProfileName": f"{BDoS_Profile_Name}_auto",
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
    

d1 = Config_Convertor_Handler()
#d1.print_table("Network Classes")
#d1.create_net_class_list()
#d1.create_BDoS_Profile_dic()
