import random, math
import argparse

def scrambleWord(word):
    """ Returns the scrambled word. """
    if len(word) < 3:       # cannot be scrambled
        return word
    elif len(word) == 4:    # scramble two middle letters        
        # 85% chance to NOT scramble the word       
        if random.random() > 0.85:
            return word
        else:    # return the middle two chars swapped
            return word[0] + word[2] + word[1] + word[3]
    else:
        newWord = word[0]   # start with the first letter
        letterList = list(word[1:-1])
        for i in range(len(letterList)):
            rando = int(math.floor(random.random() * len(letterList)))
            newWord += letterList[rando]
            letterList.remove(letterList[rando])
        newWord += word[-1]     # append the last letter
        return newWord

# *********************************************************

# Setting up the Argparser:
parser = argparse.ArgumentParser()
parser.add_argument('-f', dest='file', type=str, help='Specify file to scramble')
parser.add_argument('-s', dest='sentence', type=str, help='Specify a word or sentence to scramble. Note: put quotes around this sentence or else you will get errors.')

args = parser.parse_args()

print()
if args.sentence:
    for word in str(args.sentence).replace('.', ' ').split():
        print(scrambleWord(word), end=" ")       # Trailing comma to print them all on the same line
elif args.file:
    with open(args.file, 'r') as f:
        for line in f:
            for word in str(line).replace('.', ' ').strip().split():
                print(scrambleWord(word) , end=" ")
else:
    print(parser.print_usage())