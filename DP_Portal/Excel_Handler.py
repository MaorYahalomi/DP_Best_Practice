import pandas
import pandas as pd
from collections import Counter
import requests
import json
import time
import timeit

class Excel_Handler:
    def __init__(self, path):
        self.path = path

    def read_table(self,sheet):
        excel_data_df = pandas.read_excel(
            self.path, sheet_name=sheet)
        table = excel_data_df.to_dict('records')
        return table

    def get_network_entry_details(self, index):
        net_class_xl_format = self.read_table("Network Classes")
        return net_class_xl_format[index]["Network Name"], net_class_xl_format[index]["Network Address"], net_class_xl_format[index]["Mask"]

    def get_application_type(self, index):
        application_type_xl_format = self.read_table("Policy Editor")
        application_type = application_type_xl_format[index]["Application Type"]
        #Checks if the value is not NAN
        if pd.isna(application_type) == False:
            return application_type
        else:
            return False

    def get_Policy_Name(self, index):
        xl_format = self.read_table("Policy Editor")
        policy_name = xl_format[index]["Policy Name"]
        if pd.isna(policy_name) == False:
            return policy_name
        else:
            return False

    def get_Full_Inspection_Flag_Status(self, index):
        xl_format = self.read_table("Policy Editor")
        Full_inspect_flag = xl_format[index]["Is Full Inspection needed?"]
        if pd.isna(Full_inspect_flag) == False:
            return Full_inspect_flag
        else:
            return False   
    
    def get_CDN_Flag_Status(self, index):
        xl_format = self.read_table("Policy Editor")
        CDN_Flag = xl_format[index]["Is Service Behind CDN?"]
        if pd.isna(CDN_Flag) == False:
            return CDN_Flag
        else:
            return False

    def get_CDN_Method(self, index):
        xl_format = self.read_table("Policy Editor")
        CDN_Type = xl_format[index]["CDN Method"]
        if pd.isna(CDN_Type) == False:
            return CDN_Type
        else:
            return False

    def check_multi_network(self):
        #Function Description:
            # Checks which networks class contains multiple entries,
            # Retuern Dictoenry {Net_Name,count_of_entries}
        net_class_xl_format = self.read_table("Network Classes")
        network_name_list = [net_class_xl_format[index]["Network Name"]
                             for index in range(len(net_class_xl_format))]

        multi_net = dict(Counter(network_name_list))
        multi_net_dic = {item: multi_net[item] for (
            item, value) in multi_net.items() if multi_net[item] != 1}
        #print(multi_net_dic)
        return multi_net_dic

    def get_BDoS_profile_details(self,index):
        net_class_xl_format = self.read_table("Policy Editor")
        BDoS_profile_name = net_class_xl_format[index]["Policy Name"]
        BDoS_profile_BW= net_class_xl_format[index]["Policy BW"]
        return BDoS_profile_name, BDoS_profile_BW
    
    def get_DNS_profile_details(self,index):
        net_class_xl_format = self.read_table("Policy Editor")
        DNS_profile_name = net_class_xl_format[index]["Policy Name"]
        DNS_Expected_QPS = net_class_xl_format[index]["DNS QPS"]
        DNS_Max_QPS = net_class_xl_format[index]["DNS MAX QPS"]
        return DNS_profile_name, DNS_Expected_QPS, DNS_Max_QPS


v1 = Excel_Handler("server_test.xlsm")
#v1.create_net_class_dic()
#v1.get_BDoS_profile_details()
#v1.get_CDN_Flag_Status(1)
