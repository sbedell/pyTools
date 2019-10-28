"""
Make API Requests to https://isc.sans.edu/api/ and https://dshield.org/api/

TODO
	1. Make some flags to let the user choose return type - currently json, text, xml, csv are available
	2. Actually fix the json formatting / printing
"""

import re
# import json
import argparse
import urllib.request

apiUrl = "https://isc.sans.edu/api/"
apiUrlMirror = "https://dshield.org/api/"

def makeHttpRequest(url):
	try:
		with urllib.request.urlopen(url) as apiResponse:
			pageResponse = apiResponse.read()
			return pageResponse
	except urllib.error.URLError as e:
		return e.reason

def searchIpAddr(ipAddr):
	if (re.match(r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$', ipAddr)):
		ipUrl = apiUrl + "ip/" + ipAddr + "?text"
		apiResponse = makeHttpRequest(ipUrl)
		return apiResponse.decode("utf-8")
	else:
		return "\n[!] Invalid IP Address"

def searchPort(portNumber):
	if (re.match(r'^\d+$', portNumber) and int(portNumber) > 0 and int(portNumber) < 65536):
		portUrl = apiUrl + "port/" + portNumber + "?text"
		apiResponse = makeHttpRequest(portUrl)
		return apiResponse.decode("utf-8")
		
		# -- JSON Attempt:
		# portUrl = apiUrl + "port/" + portNumber + "?json"
		# jsonResponse = json.load(apiResponse.decode("utf-8"))
		# print(jsonResponse)
		# this json dumps only kinda works how I want it to...
		# return json.dumps(apiResponse.decode("utf-8"), indent=2)
	else:
		return "\n[!] Invalid port number"

# -=-=-=-=-=-= "Main Program" -=-=-=-=-=-=-=-=-=-=- #

# Set up the arg parser:
parser = argparse.ArgumentParser(description="Make HTTP(S) Requests to the SANS DShield API")
parser.add_argument("-i", dest="ipAddr", help="Specify IP Address to search.")
parser.add_argument("-p", dest="port", help="Specify port to search.")
# parser.add_argument("--csv", help="Flag this for CSV output")
# parser.add_argument("--text", help="Flag this for plain text output")
args = parser.parse_args()

if not args.ipAddr and not args.port:
  parser.print_help()
elif args.port:
	print(searchPort(args.port))
elif args.ipAddr:
	print(searchIpAddr(args.ipAddr))
else:
	print("[!] Unknown Error")
	parser.print_help()