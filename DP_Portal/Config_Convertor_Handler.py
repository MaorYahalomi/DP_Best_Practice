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
        list_of_net = []
        multi_net_dic = self.configuration_book.check_multi_network()
        print(multi_net_dic)
        net_class_xl_format = self.configuration_book.read_table("Network Classes")
        for index in range(len(net_class_xl_format)):
            network_name = self.configuration_book.get_network_name(index)
            network_subnet = net_class_xl_format[index]["Network Address"]
            if network_name == "Mail":
             list_of_net.append(create_single_net_dic(
                 network_name, network_subnet, 0, "255.255.255.240"))
        print(list_of_net[0])

def create_single_net_dic(network_name, netowrk_subnet, index, net_mask):

    single_net_class_dic = {
        "rsBWMNetworkName": network_name,
        "rsBWMNetworkSubIndex": index,
        "rsBWMNetworkMode": "1",
        "rsBWMNetworkAddress": netowrk_subnet,
        "rsBWMNetworkMask": net_mask
    }
    return single_net_class_dic




d1 = Config_Convertor_Handler()
#d1.print_table("Network Classes")
d1.create_net_class_list()
