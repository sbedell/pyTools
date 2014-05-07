#!/usr/bin/python

# make words into wdros and shit like that
# first and last digit same rest blah

import re, optparse, sys, random

# Create option parser and shit:
parser = optparse.OptionParser('python wordscramble.py <options>')
# parser.add_option('-l', dest='passlen', type='int', help='Specify length of passphrase. Optional, default is 4.', default=4)
parser.add_option('-f', dest='file', type='string', help='Specify file to scramble')
parser.add_option('-s', dest='sentence', type='string', help='Specify a sentence to scramble', default='This is a test sentence.')

(options, args) = parser.parse_args()

if not options.file and not options.sentence:
    print parser.print_usage()
    sys.exit(-1)

# Get a random decimal from 0 - 1
rando = random.random()
print rando

if options.sentence:
    for word in set(str(options.sentence).split(" ")):
        print word
        count = 0
        scrambledWord = ""‮‮
        for c in word: #iterate thru word
            
