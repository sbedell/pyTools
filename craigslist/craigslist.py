#!/usr/bin/python

import urllib2, sys, optparse, re, string
from bs4 import BeautifulSoup

"""
TODOS:
0. Fix the duplicate link results thing
1. implement all city and multi-city searching
2. add category selection, for now it's searching through "all for sale"
3. implement state and all states
4. implement different output types - terminal, html page, xml, json?, idk?
5. move to an argparse implementation over optparse
"""
# *********** Subprocedures ***********************
# Uses urllib2 to request a call to the
# web API to get the geolocation data.
def getResponse(url):
	try:
		response = urllib2.urlopen(url).read()
	except:
		print "Unexpected HTTP Error"
		sys.exit(-1)
	return response

#******************************************************
# Create the option parser.
# OptionParser( sample usage text)
parser = optparse.OptionParser('python craigslist.py -t searchterms <options>')

# (option flag, variable destination, [action to take], type of the variable, help text)
parser.add_option('-s', dest='state', type='string', help='Specify what state to search in. Optional - Default is Ohio. Type \'all\' to search through all states [not recommended, slow]', default='ohio')
parser.add_option('-c', dest='city', type='string', help='Specify city to search in. Comma separated. Optional - Default is Columbus. Type \'all\' to search through all cities of the selected state.', default='columbus')
#parser.add_option('-a', dest='category', type='string', help='Specify which category to search within. Optional - Default is all categories', default='sss'
parser.add_option('-t', dest='searchterm', type='string', help='Type search terms here, comma separated. Required.')
parser.add_option('-m', dest='maxprice', type='int', help='Specify max price. Optional.')
parser.add_option('-n', dest='minprice', type='int', help='Specify min price. Optional.')
parser.add_option('-r', dest='numresults', type='int', help='Set max amount of results. Optional.')
parser.add_option('-o', dest='outputType', type='string', help='Set the output type: terminal or html. Optional. Default is print to console.')
parser.add_option('-p', dest='pic', action='store_true', help='Flag this if you want pics required. Default is false.', default = False)
parser.add_option('-v', dest='verbose', action='store_true', help='Set verbose output. Default is verbose turned on.', default = True)
parser.add_option('-q', dest='verbose', action='store_false', help='Set quiet output.')

(options, args) = parser.parse_args()

# *******************************************************************
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

# building the url: http://city.craigslist.org/search/category
# ex: http://columbus.craigslist.org/search/sss?zoomToPosting=&catAbb=sss&query=testingtesting&minAsk=&maxAsk=&hasPic=1
# categories = sss is all cats

searchTerms = str(options.searchterm)
if re.search(",", searchTerms):
	searchTerms = string.replace(searchTerms, ',', '%20')
# print searchTerms

url = 'http://' + options.city + '.craigslist.org/search/sss?zoomToPosting=&catAbb=sss&query=' + searchTerms + '&minAsk='

if options.minprice != None:
	url = url + str(options.minprice)

if options.maxprice != None:
	url = url + '&maxAsk=' + str(options.maxprice)
else:
	url = url + '&maxAsk='

if options.pic:
	if options.verbose: print "pictures required"
	url = url + '&hasPic=1'

print "\nSearching " + url
craigsResponse = getResponse(url)	 # Making the Web Call
soup = BeautifulSoup(craigsResponse) # Creating a Beautifulsoup object
# print soup.prettify()  			 # Pretty Printing the output HTML

# Pulling All Links
count = 0
for link in soup.find_all('a'):
	if options.numresults != None:
		if count > options.numresults: break
	if not re.search("/\w+/\d+.html", link.get('href')):
		continue	# Skipping shit links
	print "\n" + link.get_text()
	print "http://" + options.city + ".craigslist.org" + link.get('href')
	count = count + 1

print "\n"

# for item in soup.find_all("p", class_="row")
