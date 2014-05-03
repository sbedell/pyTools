#!/usr/bin/python

import re, optparse, sys, random

parser = optparse.OptionParser('python passphrase.py <options>')
parser.add_option('-l', dest='passlen', type='int', help='Specify length of passphrase. Optional, default is 4.', default=4)
parser.add_option('-f', dest='file', type='string', help='Specify wordlist file to use. Optional, default is american.0', default='american.0')

(options, args) = parser.parse_args()

# read-in the wordlist
try:
	wordlistFile = open(options.file, 'r')
except IOError as e:
	print "Error when opening file " + str(wordlistFile) + ". " + e.strerror + "\n"
	sys.exit(-1)

# Build a lookup dictionary:
i = 0
worddict = {}
for word in wordlistFile:
	i = i + 1
	worddict[i] = word.strip()

wordlistFile.close()

totalwords = len(worddict)
print "" 			# for padding

for x in range(options.passlen):
	rando = random.random()
	wordnum =  int(round(rando * totalwords, 0))
	# print wordnum
	print worddict[wordnum],

print "\n"			# for more padding
