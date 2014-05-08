#!/usr/bin/python

# make words into wdros and shit like that
# Usage: python wordscramble.py -h
# Easter Egg: 'python wordscramble.py -f wordscramble.py'
#           This will scramble this file :D.

import optparse, sys, random, math

""" Returns the scrambled word. """
def scrambleWord(word):
    if len(word) < 3:       # cannot be scrambled
        return word
    elif len(word) == 4:    # scramble two middle letters        
        # 85% chance to NOT scramble a word       
        if random.random() > 0.80:
            return word
        else:               # return the middle two chars swapped
            return word[0] + word[2] + word[1] + word[3]
    else:
        newWord = word[0]   # start with the first letter
        letterList = list(word[1:-1])
        iterations = len(letterList)
        for i in range(iterations):
            rando = int(math.floor(random.random() * len(letterList)))
            #print rando
            newWord += letterList[rando]
            #print letterList[rando]
            #print letterList        
            letterList.remove(letterList[rando])
        newWord += word[-1]     # append the last letter
        return newWord

# *********************************************************
#Start Main Program:

# Create option parser:
parser = optparse.OptionParser('python wordscramble.py <options>')
parser.add_option('-f', dest='file', type='string', help='Specify file to scramble')
parser.add_option('-s', dest='sentence', type='string', help='Specify a sentence to scramble. Note: put quotes around this sentence or else you will get errors.', default='This is a test sentence')

(options, args) = parser.parse_args()

# No paramaters given, print usage and exit
if not options.file and not options.sentence:
    print parser.print_usage()
    sys.exit(-1)

if options.sentence:
    print
    for word in str(options.sentence).replace('.', ' ').split():
        print scrambleWord(word), 
    print "\n"

if options.file:
    with open(options.file, 'r') as f:
        for line in f:
            for word in str(line).replace('.', ' ').strip().split():
                print scrambleWord(word),
            print
