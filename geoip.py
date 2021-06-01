import urllib.request
import argparse
# TODO: import threading

def getResponse(urlparam):
    """ Using urllib to request a call to
        the web API to get the geolocation data
    """
    response = str()
    try:
        response = urllib.request.urlopen(urlparam).read().decode("utf-8")
    except:
        print("Unexpected HTTP Error")
    return response
 
# ----------------------------------------------------

parser = argparse.ArgumentParser()

# (option flag, variable destination, [action to take], type of the variable, help text)
parser.add_argument('-f', dest='ipFile', type=str, help='specify ip address file to be read in.')
parser.add_argument('-i', dest='ipaddr', type=str, help='specify ip address to be checked.')
parser.add_argument('-t', dest='outType', type=str, help='Set output type [csv, xml, or json] Default is csv.', default='csv')
# parser.add_argument('-v', dest='verbose', action='store_true', help='Set verbose output. Default is verbose turned on.', default=False)

args = parser.parse_args()

ipAddrFile = args.ipFile
ipAddr = args.ipaddr
outputFormat = args.outType
    
if ipAddrFile:
    with open(ipAddrFile, 'r') as ipInFile:
        for ip in ipInFile:
            # building the url:
            url = 'http://freegeoip.net/' + outputFormat.strip() + '/' + ip.strip()
            geoloc = getResponse(url)
            print(geoloc.strip())
elif ipAddr:
	url = 'http://freegeoip.net/' + outputFormat.strip() + '/' + ipAddr.strip()
	geoloc = getResponse(url)
	print(geoloc.strip())
else:
    print(parser.print_usage())
