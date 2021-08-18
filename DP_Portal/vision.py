from os import error
from Excel_Handler import Excel_Handler
from requests import Session
from requests.sessions import session
from error_handling import Error_handler, VISION_LOGIN_ERROR
import json
import time

Vision_IP = "10.213.17.49"
Vision_user = "radware"
Vision_password = "radware1"

class Vision:

	def __init__(self, ip, username, password):
		self.ip = ip
		self.login_data = {"username": username, "password": password}
		self.base_url = "https://" + ip
		self.session = Session()
		self.session.headers.update({"Content-Type": "application/json"})
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

	def lock_device(self): 
			url = f"https://{self.ip}/mgmt/system/config/tree/device/byip/10.213.17.52/lock"
			response = self.session.post(url, verify=False)
			print(response)

	def bdos_profile_confg(self,BDoS_config):
		url = f"https://{self.ip}/mgmt/device/byip/10.213.17.52/config/rsNetFloodProfileTable/{BDoS_config['profile_name']}/"
		bdos_profile_body = {
                            "rsNetFloodProfileName": BDoS_config['profile_name'],
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
                      						"rsNetFloodProfileBandwidthIn": BDoS_config['BW_in'],
                      						"rsNetFloodProfileBandwidthOut":  BDoS_config['BW_out'],
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
		response = self.session.post(
			url, data=json.dumps(bdos_profile_body), verify=False)
		print(response)



# MAIN Prog #

config = {
            "profile_name": "maor_bdos",
    		"BW_in": "100000",
  			"BW_out": "100000",

         }

# v1 = Vision(Vision_IP, Vision_user, Vision_password)
# v1.lock_device()
# v1.bdos_profile_confg(config)

v1 = Excel_Handler("sars", 10, 50)
print(v1.fare())
