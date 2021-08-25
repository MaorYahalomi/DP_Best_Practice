from os import error
from Excel_Handler import Excel_Handler
from Config_Convertor_Handler import Config_Convertor_Handler
from requests import Session
from requests.sessions import session
from error_handling import Error_handler, VISION_LOGIN_ERROR
import json
import time

Vision_IP = "10.213.17.49"
Vision_user = "radware"
Vision_password = "radware"
DP_IP = "10.213.17.52"

class Vision:

	def __init__(self, ip, username, password):
		self.ip = ip
		self.login_data = {"username": username, "password": password}
		self.base_url = "https://" + ip
		self.session = Session()
		self.session.headers.update({"Content-Type": "application/json"})
		self.config_file = Config_Convertor_Handler()
		self.login()
		
	def login(self):
		login_url = self.base_url + '/mgmt/system/user/login'

		r = self.session.post(url=login_url, json=self.login_data, verify=False)
		response = r.json()

		if response['status'] == 'ok':
			self.session.headers.update({"JSESSIONID": response['jsessionid']})
			print("Auth Cookie is:  " + response['jsessionid'])
			print(r.status_code)
			return str(r.status_code)
		else:
			# Error handling to be completed
			raise Error_handler(VISION_LOGIN_ERROR)

	def lock_device(self,dp_ip): 
		url = f"https://{self.ip}/mgmt/system/config/tree/device/byip/{DP_IP}/lock"
		response = self.session.post(url, verify=False)
		print(response)

	def BDoS_profile_config(self):
		BDoS_config_file = self.config_file.create_BDoS_Profile_dic()
		for index in range(len(BDoS_config_file)):
			url = f"https://{self.ip}/mgmt/device/byip/{DP_IP}/config/rsNetFloodProfileTable/{BDoS_config_file[index]['rsNetFloodProfileName']}/"		
			bdos_profile_body = json.dumps(BDoS_config_file[index])
			response = self.session.post(url, data=bdos_profile_body, verify=False)
			print(response)

	def DNS_profile_config(self):
		DNS_config_file = self.config_file.create_DNS_Profile_dic()
		for index in range(len(DNS_config_file)):
			url = f"https://{self.ip}/mgmt/device/byip/{DP_IP}/config/rsDnsProtProfileTable/{DNS_config_file[index]['rsDnsProtProfileName']}/"
			DNS_profile_body = json.dumps(DNS_config_file[index])
			response = self.session.post(url, data=DNS_profile_body, verify=False)
			print(response)

	def net_class_config(self):
		networks_config = self.config_file.create_net_class_list()
		for index in range (len(networks_config)):
				url = f"https://{self.ip}/mgmt/device/byip/{DP_IP}/config/rsBWMNetworkTable/{networks_config[index]['rsBWMNetworkName']}/{networks_config[index]['rsBWMNetworkSubIndex']}/"
				net_class_body = json.dumps(networks_config[index])
				response = self.session.post(url, data=net_class_body, verify=False)
				print(response)

# MAIN Prog #

v1 = Vision(Vision_IP, Vision_user, Vision_password)
#v1.lock_device()
#v1.net_class_config()
#v1.bdos_profile_config()
v1.DNS_profile_config()
