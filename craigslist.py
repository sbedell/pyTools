import re
import argparse
import urllib.request
from bs4 import BeautifulSoup

import optparse # remove this, it's deprecated in favor of argparse
import urllib2 # remove this too

"""
TODOS:
1. implement all city searching
2. add category selection, for now it's searching through "all for sale"
- implement different output types - terminal, html page, xml, json?, idk?
- move to an argparse implementation over optparse - Python 3

Notes: 
# building the url: https://city.craigslist.org/search/category
# ex: https://columbus.craigslist.org/search/sss?zoomToPosting=&catAbb=sss&query=testingtesting&minAsk=&maxAsk=&hasPic=1
# categories = sss is all categories
"""

# ***************** Subprocedures *********************
def getResponse(url):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en; rv:1.8.1.11) Gecko/20121207 Firefox/3.5.16')]
    try:
        response = opener.open(url).read()
    except:
        print("Unexpected HTTP Error")
    return response

# ******************************************************
# Create the option parser. OptionParser( sample usage text)
parser = optparse.OptionParser('python craigslist.py -s searchterms <options>')

# (option flag, variable destination, [action to take], type of the variable, help text)
parser.add_option('-c', dest='city', type='string', help='Specify city (or cities) to search in. Comma separated! Optional - Default is Columbus. Type \'all\' to search through all cities.', default='columbus')
parser.add_option('-m', dest='maxprice', type='int', help='Specify max price - number only. Optional.')
parser.add_option('-n', dest='minprice', type='int', help='Specify min price - number only. Optional.')
parser.add_option('-p', dest='pic', action='store_true', help='Flag this if you want pics required. Default is false.', default = False)
parser.add_option('-s', dest='searchterms', type='string', help='Type search terms here, comma separated or put terms in quotes. Required.')
parser.add_option('-v', dest='verbose', action='store_true', help='Set verbose output. Default is quiet output.', default = False)
#parser.add_option('-r', dest='numresults', type='int', help='Set max amount of results. Optional.')
# parser.add_option('-a', dest='category', type='string', help='Specify which category to search within. Optional - Default is all categories', default='sss'
#parser.add_option('-o', dest='outputType', type='string', help='Set the output type: terminal or html. Optional. Default is print to console.')

(options, args) = parser.parse_args()

# *********************** Main Program ***************************
if options.verbose:
    # print all excess/non parsed arguments
	for arg in args:
        print("Arg = " + arg)

if not options.searchterms:
	print("\nError, type in 'python craigslist.py -h' for more help.")
	print(parser.print_usage())

# Parse City (or cities):
if options.city == 'all':
	print("This is not implemented yet.")
elif re.search("\d+", options.city):
    print("Invalid city - no numbers in cities!")
else:
    userCiti = str(options.city).strip().lower()

if re.search(',', userCiti):        # Comma separated cities
    cityList = [city.strip() for city in userCiti.split(',')]
else:
    cityList = [userCiti]

# Parse Search Terms and HTML encode them:
searchTerms = str(options.searchterms)
if re.search(",", searchTerms):
	searchTerms = searchTerms.replace(',', '+')
if re.search(" ", searchTerms):
    searchTerms = searchTerms.replace(' ', '+')

for city in cityList:
    # Building the URL: 
    url = 'https://' + city + '.craigslist.org/search/sss?zoomToPosting=&catAbb=sss&query=' + searchTerms + '&minAsk='

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
        print('\n' + link.get_text())
        if re.search("https://", link.get('href')):
            print(link.get('href'))
        else:
            print("https://" + city + ".craigslist.org" + link.get('href'))
    print("\n")
