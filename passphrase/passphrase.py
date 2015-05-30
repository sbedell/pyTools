import re, random
import argparse

def generateWordlist(file):
    """ Creates a dictionary of words from a file
        Returns a dict
    """
    i = 0
    wordDict = {}
    with open(file, 'r') as wordListFile:
        for word in wordListFile:
            i = i + 1
            wordDict[i] = word.replace('<', ' ').replace('>', ' ').replace('/', '').replace('"', '').replace("'", "").replace(',', ' ').replace('.', ' ').strip()
    return wordDict
        
def generatePassphrase(wordlist, length):
    passPhrase = str()
    for x in range( length ):
        randomWordPos = int(round(random.random() * len(wordlist), 0)) - 1
        passPhrase += wordlist[randomWordPos] + " "
    return passPhrase

# ----------------------------------------

# Set up ArgParser
parser = argparse.ArgumentParser()
parser.add_argument('-l', dest='passlen', type=int, help='Specify length of passphrase. Optional, default is 4.', default=4)
parser.add_argument('-f', dest='file', type=str, help='Specify wordlist file to use.')

args = parser.parse_args()

# Prints usage and exits if no file given
if not args.file:
    print(parser.print_usage())
    exit(-1)

# Get a word dictionary from the file:
words = generateWordlist( args.file )
passphrase = generatePassphrase( words, args.passlen )

print("\n", passphrase, "\n")
