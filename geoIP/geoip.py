import optparse, re, sys, urllib2
# TO TRY: import threading

# Uses urllib2 to request a call to the
# web API to get the geolocation data.
def getResponse(urlparam):
	try:
		response = urllib2.urlopen(urlparam).read()
	except:
		print "Unexpected HTTP Error"
	return response
 
# Create the option parser.
# OptionParser( sample usage text)
parser = optparse.OptionParser('geoIP2.py <options>')

# (option flag, variable destination, [action to take], type of the variable, help text)
parser.add_option('-f', dest='ipFile', type='string', help='specify ip address file to be read in.')
parser.add_option('-i', dest='ipaddr', type='string', help='specify ip address to be checked.')
parser.add_option('-t', dest='outType', type='string', help='Set output type [csv, xml, or json] Default is csv.', default='csv')
parser.add_option('-v', dest='verbose', action='store_true', help='Set verbose output. Default is verbose turned on.', default=True)
parser.add_option('-q', dest='verbose', action='store_false', help='Set quiet output.')

"""options is parsed as a 'struct' of sorts, where the variables from above are filled
  args is just any shit that is left over, ideally not used """
(options, args) = parser.parse_args()

# Setting global variables: 
ipAddrFile = options.ipFile
ipAddr = options.ipaddr
Verbose = options.verbose
outputFormat = options.outType

# Prints help and exits if no inputs are supplied
if (ipAddrFile == None and ipAddr == None):
	print "\nPlease supply an ip address or a file of addresses to be checked."
	print "Type in \'python geoIP.py -h\' for help"
	sys.exit(-1)
 
if Verbose: print "\nProcessing starting...\n"

if ipAddrFile != None:
	try:
		ipInFile = open(ipAddrFile, 'r')
	except IOError as e:
		print "Error when opening file " + str(ipAddrFile) + ". " + e.strerror + "\n"
		sys.exit(-1)
	for ip in ipInFile:
		# building the url:
		url = 'http://freegeoip.net/' + outputFormat + '/' + ip.strip()
		response = getResponse(url)
		geoloc = response.strip()
		print geoloc
elif ipAddr != None:
	url = 'http://freegeoip.net/' + outputFormat + '/' + ipAddr.strip()
	geoloc = getResponse(url)
	print geoloc
else:
	print "I think this is an error..."

if Verbose: print '\nProcessing Complete.\n'
