import re
import argparse
import urllib.request

# Gets an HTTP response from a url
# Return type - string.
# opener.addheaders spoofs the UserAgent
def getResponse(url):
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/68.0')]
    
    try:
        response = opener.open(url).read().decode("utf-8")
    except urllib.request.HTTPError as e:
        print("Error = " + str(e.strerror))
        exit(-1)
    except:
        print("Unexpected HTTP Error")
        exit(-1)

    return response
    
# Taken from Django
def is_valid_url(url):
    urlRegex = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return urlRegex.search(url)
    
# TODO - use regex to match words only, no special char bs
def createWordlist(response):
    """ Creates a wordlist given a urllib response """
    try:
        wordlist = response.strip()
        wordlist = re.split(r'[^a-zA-Z]+', wordlist) #split on non a-Z characters
        theWordList = set()
        for word in wordlist:
            if (re.match(r'\w+', word)):
                theWordList.add(word) 
    except UnicodeEncodeError:
        print("Encoding Error")
    
    return theWordList

# Get command line args:
parser = argparse.ArgumentParser()
parser.add_argument('-u', metavar='URL', help = 'URL to make dictionary from', dest='url')
parser.add_argument('-f', metavar='infile', help = 'Name of a file to read-in', dest='inFileName')

args = parser.parse_args()

# "Main Program"
if args.url and args.inFileName:
    print("Cannot create a dictionary with a url and a file.")
    print(parser.print_usage())
elif args.url:
    if not is_valid_url(args.url):
        print("Invalid URL, exiting...")
        exit(-1)
    else:
        response = getResponse(args.url)
        wordlist = createWordlist(response)
        for word in wordlist:
            try:
                print(word)
            except UnicodeEncodeError:
                print("Unicode Encoding Error")
elif args.inFileName:
    with open(args.inFileName) as inputFile:
        for line in inputFile:
            splitLine = line.replace('<', ' ').replace('>', ' ').replace('/', '').replace('"', '').replace("'", "").replace(',', ' ').replace('.', ' ').strip().split()
            for word in set(splitLine):
                try:
                    print(word)
                except UnicodeEncodeError:
                    print("UnicodeEncodingError")
else:
    print(parser.print_usage())
