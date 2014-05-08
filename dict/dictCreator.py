#!/usr/bin/python

import urllib2, sys, optparse, re, string

# Gets an HTTP response from a url, returns string
# This spoofs the user agent because Google blocks
# bot requets from urllib usually
def getResponse(url):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11')]

    try:
        response = opener.open(url).read()
    except:
        print "Unexpected HTTP Error"
        sys.exit(-1)
    return response

# Get command line args:
parser = optparse.OptionParser('python dictcreator.py <options>')
parser.add_option('-u', metavar='URL', help = 'URL to make dictionary from', dest='url')
parser.add_option('-f', metavar='file', help = 'filename to write to', dest='filename')

options, args = parser.parse_args()

if not options.url:
	print parser.print_usage()
	sys.exit(-1)
else:
	# probably need to regex verify a correct URL
	response = getResponse(options.url)
	#wordlist = response.replace('.', ' ').replace(':', ' ').replace('?', '').split(' ')
	wordlist = response.replace('<', ' ').replace('>', ' ').replace('/', '').split(' ')

"""
with open('testDict', 'a') as f:
	for word in set(wordlist):
		f.write(str(word.strip()) + '\n')
"""
for word in set(wordlist):
    print word
