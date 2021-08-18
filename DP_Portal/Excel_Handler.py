import pandas
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

    def create_single_net_dic(self, network_name, netowrk_subnet,index,net_mask):

        single_net_class_dic = {
            "rsBWMNetworkName": network_name,
            "rsBWMNetworkSubIndex": index,
            "rsBWMNetworkMode": "1",
            "rsBWMNetworkAddress": netowrk_subnet,
            "rsBWMNetworkMask": net_mask
        }
        return single_net_class_dic

    def create_net_class_dic(self):
        net_class_xl_format = self.read_table("Network Classes")       
        # list_of_net_class_dict = [net_class_xl_format[index]["Subnet"]
        #                           for index in range(len(net_class_xl_format))]
        
        # print(list_of_net_class_dict)
        #print(net_class_xl_format[0]["Network Name"])
        for index in range(len(net_class_xl_format)):
            network_name = net_class_xl_format[index]["Network Name"]
            network_subnet = net_class_xl_format[index]["Subnet"]
            print(network_name)


# v1 = Excel_Handler("test.xlsm")
# v1.create_net_class_dic()
