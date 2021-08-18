import pandas
import requests
import json
import time
import timeit
from Excel_Handler import Excel_Handler

class Config_Convertor_Handler:
    def __init__(self):
        self.configuration_book =  Excel_Handler("test.xlsm")

    def print_table(self):
        print(self.configuration_book.read_table("Network Classes"))


v1 = Config_Convertor_Handler()
v1.print_table()
