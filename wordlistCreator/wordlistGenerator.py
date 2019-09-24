import re
import argparse
import urllib.request
    
# Taken from Django documentation
def is_valid_url(url):
    regex = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url is not None and regex.search(url)

def getResponse(url):
    braveUserAgent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
    firefoxUserAgent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0'
    headers = {'User-Agent': firefoxUserAgent}

    if (not is_valid_url(url)):
        return "\n [!] Invalid URL provided"
    else:
        httpRequest = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(httpRequest) as response:
                pageResponse = response.read().decode('UTF-8')
                return pageResponse
        except urllib.error.URLError as e:
            return e.reason  

def createWordlistFromUrl(response):
    """ Creates a wordlist given a urllib response """
    try:
        # Strip out useless characters
        wordlist = response.replace('<', ' ').replace('>', ' ').replace('/', '').replace('.', ' ').strip()
        wordlist = re.split(r'[^a-zA-Z]+', wordlist) #split on non a-Z characters
        theWordList = set()
        for word in wordlist:
            if (re.match(r'\w+', word)):
                theWordList.add(word)
    except UnicodeEncodeError:
        print("Encoding Error")
    
    return theWordList

def createWordlistFromFile(file):
    with open(args.inFileName, 'r') as f:
        wordlist = set()
        for line in f:
            splitLine = line.replace(',', ' ').replace('.', ' ').strip().split()
            for word in splitLine:                
                wordlist.add(word)
        return wordlist

# Get command line args:
argParser = argparse.ArgumentParser(description="Generate a wordlist from a website or text file")
argParser.add_argument('-u', metavar='URL', help = 'URL to make dictionary from', dest='url')
argParser.add_argument('-f', metavar='infile', help = 'Name of a file to read-in', dest='inFileName')

args = argParser.parse_args()

# "Main Program"
if not args.url and not args.inFileName:
    print(argParser.print_help())
elif args.url and args.inFileName:
    print("\nError - can only generate a dictionary from a URL or a file, not both.\nIf you really need to do this, " \
    "run this program once with the url, and redirect it to a file ('>' on the command line), " \
    "then re-run this program with your infile and append it to the file you JUST created (using '>>')\n")
elif args.url:
    response = getResponse(args.url)
    wordlist = createWordlistFromUrl(response)
    for word in wordlist:
        print(word)
elif args.inFileName:
    wordlist = createWordlistFromFile(args.inFileName)
    for word in wordlist:
        try:
            print(word)
        except UnicodeEncodeError:
            print("Encoding Error")
else:
    print("Unexpected Error")
