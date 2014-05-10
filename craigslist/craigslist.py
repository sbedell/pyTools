#!/usr/bin/python

import urllib2, sys, optparse, re, string
from bs4 import BeautifulSoup

"""
TODOS:
1. implement all city and multi-city searching
2. add category selection, for now it's searching through "all for sale"
3. implement state and all states
4. implement different output types - terminal, html page, xml, json?, idk?
5. maybe add user agent selection/spoofing?
6. move to an argparse implementation over optparse - Python 3
"""

# *********** Subprocedures ***********************
# Uses urllib2 to request a call to the
# web API to get the geolocation data.
def getResponse(url, userAgent = None):
    opener = urllib2.build_opener()
    userAgent = 'User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en; rv:1.8.1.11) Gecko/20121207 Firefox/3.5.16'
    opener.addheaders = [(userAgent)]
    try:
        response = opener.open(url).read()
    except:
        print "Unexpected HTTP Error"
        sys.exit(-1)
    return response

# ******************************************************
# Create the option parser. OptionParser( sample usage text)
parser = optparse.OptionParser('python craigslist.py -t searchterms <options>')

# (option flag, variable destination, [action to take], type of the variable, help text)
parser.add_option('-c', dest='city', type='string', help='Specify city to search in. Comma separated. Optional - Default is Columbus. Type \'all\' to search through all cities of the selected state.', default='columbus')
parser.add_option('-s', dest='state', type='string', help='Specify what state to search in. Optional - Default is Ohio. Type \'all\' to search through all states [not recommended, slow]', default='ohio')
parser.add_option('-t', dest='searchterm', type='string', help='Type search terms here, comma separated. Required.')
parser.add_option('-m', dest='maxprice', type='int', help='Specify max price. Optional.')
parser.add_option('-n', dest='minprice', type='int', help='Specify min price. Optional.')
parser.add_option('-p', dest='pic', action='store_true', help='Flag this if you want pics required. Default is false.', default = False)
parser.add_option('-v', dest='verbose', action='store_true', help='Set verbose output. Default is quiet output.', default = False)
# parser.add_option('-a', dest='category', type='string', help='Specify which category to search within. Optional - Default is all categories', default='sss'
#parser.add_option('-u', dest='userAgent', type='string', help='Input a custom User-Agnent string.')
#parser.add_option('-r', dest='numresults', type='int', help='Set max amount of results. Optional.')
#parser.add_option('-o', dest='outputType', type='string', help='Set the output type: terminal or html. Optional. Default is print to console.')

(options, args) = parser.parse_args()

# *********************** MAIN *************************************
# Main Program is starting here: 
if options.verbose:
    # print all excess/non parsed arguments
	for arg in args:
		print "Arg = " + arg

# Pull a list of cities, should be slurping this with bsoup
ohioCities = ['akroncanton', 'ashtabula', 'athens', 'chillicothe', 'cincinnati', 'cleveland', 'columbus', 'dayton', 'limaohio', 'mansfield', 'sandusky', 'toledo', 'tuscarawas', 'youngstown', 'zanesville']

if options.searchterm == None:
	print "Error, please provide search term(s)."
	print parser.print_usage()
	sys.exit(-1)

if options.city == 'all':
	print "TODO"

if options.state == 'all':
    print "TODO"
    # scrape the page of all the city names and shit

# building the url: http://city.craigslist.org/search/category
# ex: http://columbus.craigslist.org/search/sss?zoomToPosting=&catAbb=sss&query=testingtesting&minAsk=&maxAsk=&hasPic=1
# categories = sss is all categories

# Grab the search terms and html encode them:
# There's probably a better way lol
searchTerms = str(options.searchterm)
if re.search(",", searchTerms):
	searchTerms = string.replace(searchTerms, ',', '+')
# print searchTerms

# Building the URL: 
url = 'http://' + str(options.city) + '.craigslist.org/search/sss?zoomToPosting=&catAbb=sss&query=' + searchTerms + '&minAsk='

if options.minprice: url += str(options.minprice)

url += '&maxAsk='

if options.maxprice: url += str(options.maxprice)

if options.pic:
	if options.verbose: print "Pictures required."
	url += '&hasPic=1'

if options.verbose: print "\nSearching " + url

craigsResponse = getResponse(url)	 # Making the Web Call
soup = BeautifulSoup(craigsResponse) # Creating a Beautifulsoup object
# print soup.prettify()  			 # Pretty Printing the output HTML

# Pulling All Links
# links = [link for link in soup.find_all('a')]

for link in soup.find_all('a'):
    #print type(link), link                          # type = bs4.element.Tag
    #print type(link.get('href')), link.get('href')  # type = unicode
    #print type(link.get_text()), link.get_text()    # type = unicode
    # skips blank href, blank link text, any links beginning with dollar signs, and any links not ending in .html
    if not link.get('href') or not link.get_text() or (re.search("^\$", link.get_text())) or (not re.search(".html", link.get('href'))):
        continue
    if re.search("top", link.get_text()):
        break       # Found the end of results - breaking out
    print '\n' + link.get_text()
    print "http://" + options.city + ".craigslist.org" + link.get('href')
print "\n"

""" 
if options.numresults:
        if count > options.numresults: break
    # Break if over the specified result limit
"""
