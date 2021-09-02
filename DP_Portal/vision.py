import urllib3
urllib3.disable_warnings()
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
		url = f"https://{self.ip}/mgmt/system/config/tree/device/byip/{dp_ip}/lock"
		response = self.session.post(url, verify=False)
		print(response)

	def update_policy(self,dp_ip):
		self.lock_device(dp_ip)
		update_url = f"https://{self.ip}/mgmt/device/byip/{dp_ip}/config/updatepolicies?"
		response = self.session.post(update_url, verify=False)
		print(response)

	def BDoS_profile_config(self):
		BDoS_config_file = self.config_file.create_BDoS_Profile_dic()
		for index in range(len(BDoS_config_file)):
			url = f"https://{self.ip}/mgmt/device/byip/{DP_IP}/config/rsNetFloodProfileTable/{BDoS_config_file[index]['rsNetFloodProfileName']}/"		
			bdos_profile_body = json.dumps(BDoS_config_file[index])
			response = self.session.post(url, data=bdos_profile_body, verify=False)
			print(response)

	def OOS_profile_config(self):
		OOS_config_file = self.config_file.create_OOS_Profile_dic()
		for index in range(len(OOS_config_file)):
			url = f"https://{self.ip}/mgmt/device/byip/{DP_IP}/config/rsStatefulProfileTable/{OOS_config_file[index]['rsSTATFULProfileName']}/"
			oos_profile_body = json.dumps(OOS_config_file[index])
			response = self.session.post(url, data=oos_profile_body, verify=False)
			print(response)
				
	def SYN_profile_config(self):
		SYN_config_file = self.config_file.create_Syn_Profile_dic()
		#print(SYN_config_file[0])
		for index in range(len(SYN_config_file)):
				profile_url = f"https://{self.ip}/mgmt/device/byip/{DP_IP}/config/rsIDSSynProfilesParamsTable/{SYN_config_file[index][0]['rsIDSSynProfilesParamsName']}/"
				application_url = f"https://{self.ip}/mgmt/device/byip/{DP_IP}/config/rsIDSSynProfilesTable/{SYN_config_file[index][0]['rsIDSSynProfilesParamsName']}/{SYN_config_file[index][1]['rsIDSSynProfileServiceName']}/"
				application_body = json.dumps(SYN_config_file[index][1])
				syn_profile_body = json.dumps(SYN_config_file[index][0])

				response_application = self.session.post(
					application_url, data=application_body, verify=False)

				response_profile = self.session.put(
					profile_url, data=syn_profile_body, verify=False)

				print(response_profile, response_application)

	def DNS_profile_config(self):
		DNS_config_file = self.config_file.create_DNS_Profile_dic()
		for index in range(len(DNS_config_file)):
			url = f"https://{self.ip}/mgmt/device/byip/{DP_IP}/config/rsDnsProtProfileTable/{DNS_config_file[index]['rsDnsProtProfileName']}/"
			DNS_profile_body = json.dumps(DNS_config_file[index])
			response = self.session.post(url, data=DNS_profile_body, verify=False)
			print(response)

	def AS_profile_config(self):
		AS_config_file = self.config_file.create_AS_Profile_dic()
		for index in range(len(AS_config_file)):
			url = f"https://{self.ip}/mgmt/device/byip/{DP_IP}/config/rsIDSScanningProfilesTable/{AS_config_file[index]['rsIDSScanningProfilesName']}/"
			AS_profile_body = json.dumps(AS_config_file[index])
			response = self.session.post(url, data=AS_profile_body, verify=False)
			print(response)

	def ERT_profile_config(self):
		ERT_config_file = self.config_file.create_ERT_Profile_dic()
		for index in range(len(ERT_config_file)):
			url = f"https://{self.ip}/mgmt/device/byip/{DP_IP}/config/rsErtAttackersFeedProfileTable/{ERT_config_file[index]['rsErtAttackersFeedProfileName']}/"
			ERT_profile_body = json.dumps(ERT_config_file[index])
			response = self.session.post(url, data=ERT_profile_body, verify=False)
			print(response)

	def GEO_profile_config(self):
		GEO_config_file = self.config_file.create_GEO_Profile_dic()
		for index in range(len(GEO_config_file)):
			url = f"https://{self.ip}/mgmt/device/byip/{DP_IP}/config/rsGeoProfileTable/{GEO_config_file[index]['rsGeoProfileName']}/"
			GEO_profile_body = json.dumps(GEO_config_file[index])
			response = self.session.post(url, data=GEO_profile_body, verify=False)
			print(response)

	def HTTPS_profile_config(self):
		HTTPS_config_file = self.config_file.create_HTTPS_Profile_dic()
		#print(HTTPS_config_file)
		for index in range(len(HTTPS_config_file)):
			url = f"https://{self.ip}/mgmt/device/byip/{DP_IP}/config/rsHttpsFloodProfileTable/{HTTPS_config_file[index]['rsHttpsFloodProfileName']}/"
			HTTPS_profile_body = json.dumps(HTTPS_config_file[index])
			response = self.session.post(url, data=HTTPS_profile_body, verify=False)
			print(response)

	def net_class_config(self):
		networks_config = self.config_file.create_net_class_list()
		for index in range (len(networks_config)):
				url = f"https://{self.ip}/mgmt/device/byip/{DP_IP}/config/rsBWMNetworkTable/{networks_config[index]['rsBWMNetworkName']}/{networks_config[index]['rsBWMNetworkSubIndex']}/"
				net_class_body = json.dumps(networks_config[index])
				response = self.session.post(url, data=net_class_body, verify=False)
				print(response)

# MAIN Prog Tests#

v1 = Vision(Vision_IP, Vision_user, Vision_password)
#Protection tests
	#v1.lock_device()
	#v1.net_class_config()
	#v1.bdos_profile_config()
	#v1.DNS_profile_config()
	#v1.SYN_profile_config()
	#v1.OOS_profile_config()
	#v1.AS_profile_config()
	#v1.ERT_profile_config()
	#v1.GEO_profile_config()
	#v1.update_policy(DP_IP)
v1.HTTPS_profile_config()
