import pandas
import requests
import json
import time
import timeit
from Excel_Handler import Excel_Handler

class Config_Convertor_Handler:
    def __init__(self):
        self.configuration_book =  Excel_Handler("test.xlsm")

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
        print(multi_net_dic)
        net_class_xl_format = self.configuration_book.read_table("Network Classes")
        for index in range(len(net_class_xl_format)):
            network_name = self.configuration_book.get_network_name(index)
            network_subnet = self.configuration_book.get_network_address(index)
            network_mask = self.configuration_book.get_network_mask(index)
           
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

def create_single_net_dic(network_name, netowrk_subnet, sub_index, net_mask):

    single_net_class_dic = {
        "rsBWMNetworkName": network_name,
        "rsBWMNetworkSubIndex": sub_index,
        "rsBWMNetworkMode": "1",
        "rsBWMNetworkAddress": netowrk_subnet,
        "rsBWMNetworkMask": net_mask
    }
    return single_net_class_dic


# d1 = Config_Convertor_Handler()
# #d1.print_table("Network Classes")
# d1.create_net_class_list()
