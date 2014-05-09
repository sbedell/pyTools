#!/usr/bin/python

import urllib2, sys, optparse, re, string

# Gets an HTTP response from a url, returns string
# This spoofs the user agent because Google blocks
# bot requets from urllib usually
def getResponse(url):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en; rv:1.8.1.11) Gecko/20121207 Firefox/3.5.16')]
    try:
        response = opener.open(url).read()
    except:
        print "Unexpected HTTP Error"
        sys.exit(-1)
    return response

# Get command line args:
parser = optparse.OptionParser('python dictcreator.py <options>')
parser.add_option('-u', metavar='URL', help = 'URL to make dictionary from', dest='url')
parser.add_option('-r', metavar='infile', help = 'Name of a file to read-in', dest='inFileName')

options, args = parser.parse_args()

# No arguments were given:
if not options.url and not options.inFileName:
	print parser.print_usage()
	sys.exit(-1)
elif options.url:
    # probably need to regex verify a correct URL
    response = getResponse(options.url)
    wordlist = response.replace('<', ' ').replace('>', ' ').replace('/', '').strip().split()
    for word in set(wordlist):
        print word
elif options.inFileName:
    with open(options.inFileName, 'r') as f:
    	for line in f:
            splitLine = line.replace(',', ' ').replace('.', ' ').strip().split()
            for word in set(splitLine):                
                print word
else:
    print "Error"
    sys.exit(-1)
