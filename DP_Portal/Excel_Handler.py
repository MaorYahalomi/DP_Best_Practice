import pandas
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
        table = excel_data_df.to_dict(orient='record')
        return table
        #print(table_sheet)

    def get_network_name(self,index):
        net_class_xl_format = self.read_table("Network Classes")
        #print(net_class_xl_format[index]["Network Name"])
        return net_class_xl_format[index]["Network Name"]
        
    def get_network_address(self,index):
        net_class_xl_format = self.read_table("Network Classes")
        #print(net_class_xl_format[index]["Network Address"])
        return net_class_xl_format[index]["Network Address"]

    def get_network_mask(self,index):
        net_class_xl_format = self.read_table("Network Classes")
        #print(net_class_xl_format[index]["Mask"])
        return net_class_xl_format[index]["Mask"]

    def check_multi_network(self):
        net_class_xl_format = self.read_table("Network Classes")
        network_name_list = [net_class_xl_format[index]["Network Name"]
                             for index in range(len(net_class_xl_format))]

        multi_net = dict(Counter(network_name_list))
        multi_net_dic = {item: multi_net[item] for (
            item, value) in multi_net.items() if multi_net[item] != 1}
        #print(multi_net_dic)
        return multi_net_dic


        #network_name = net_class_xl_format[index]["Network Name"]
        network_name_mask = [net_class_xl_format[index]["Network Address"]
                                for index in range(len(net_class_xl_format))]
        #return network_name_address
        print(network_name_mask)



def create_single_net_dic(network_name, netowrk_subnet,index,net_mask):

        single_net_class_dic = {
            "rsBWMNetworkName": network_name,
            "rsBWMNetworkSubIndex": index,
            "rsBWMNetworkMode": "1",
            "rsBWMNetworkAddress": netowrk_subnet,
            "rsBWMNetworkMask": net_mask
        }
        return single_net_class_dic


v1 = Excel_Handler("test.xlsm")
#v1.create_net_class_dic()
#v1.get_network_name()
