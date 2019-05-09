#!/usr/bin/python

import sys, optparse, re, string, urllib2
from urlparse import urlparse

# Gets an HTTP response from a url
# Return type - string.
# opener.addheaders spoofs the UserAgent
def getResponse(url):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0 ')]
    
    try:
        response = opener.open(url).read()
    except urllib2.HTTPError as e:
        print "Error = " + str(e.strerror)
        sys.exit(-1)
    except:
        print "Unexpected HTTP Error"
        sys.exit(-1)
    
    #response = opener.open(url).read()
    return response
    
def is_valid_url(url):
    regex = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url is not None and regex.search(url)

# Get command line args:
parser = optparse.OptionParser('python dictcreator.py <options>')
parser.add_option('-u', metavar='URL', help = 'URL to make dictionary from', dest='url')
parser.add_option('-r', metavar='infile', help = 'Name of a file to read-in', dest='inFileName')

# populate the options
options, args = parser.parse_args()

# "Main Program"
if not options.url and not options.inFileName:
    print parser.print_usage()
    sys.exit(-1)
elif options.url and options.inFileName:
    print "\nError - can only generate a dictionary from a URL or a file, not both.\nIf you really need to do this, " \
    "run this program once with the url, and redirect it to a file ('>' on the command line), then re-run this program with your infile and append it to the file you JUST created (using '>>')\n"
    sys.exit(-1)
elif options.url:
    # probably need to regex verify a correct URL
    assert is_valid_url(options.url)
    response = getResponse(options.url)
    wordlist = response.replace('<', ' ').replace('>', ' ').replace('/', '').replace('.', ' ').strip().split()
    for word in set(wordlist):
        print word
elif options.inFileName:
    with open(options.inFileName, 'r') as f:
        for line in f:
            splitLine = line.replace(',', ' ').replace('.', ' ').strip().split()
            for word in set(splitLine):                
                print word
else:
    print "Unexpected Error"
    sys.exit(-1)
