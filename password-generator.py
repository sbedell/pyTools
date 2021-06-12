import math, random

def pickCharsFromString(inputStr, numChars):
  chars = ""
  for i in range(0, numChars):
    chars += inputStr[math.floor(random.random() * len(inputStr))]
  
  return chars

# Shuffle string, lol python has a built in shuffle thing
def shuffleString(inputStr):
  l = list(inputStr)
  random.shuffle(l)
  return ''.join(l)

#######
#  Generate a secure random password.
# 
#  @param {Number} length - length of the password to generate.
#######
def generateRandomPassword(length):
  numbers = "0123456789"
  lowercase = "abcdefghijklmnopqrstuvwxyz"
  uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
  specialCharsSafe = "!@#$%^&*-_=+?"
  # allSpecialChars = '~!@#$%^&*()_+=-"|\/<>.,?';
  # trimmedListOfSpecials = "!@#$%*?_-=.:|";
  allChars = numbers + lowercase + uppercase + specialCharsSafe

  password = pickCharsFromString(numbers, 1) + pickCharsFromString(specialCharsSafe, 1) + pickCharsFromString(lowercase, 1) + pickCharsFromString(uppercase, 1) + pickCharsFromString(allChars, length - 4)
  
  return shuffleString(password)

##--------------------------------------------
# Could do an argparse down here and get user input for password length:

print(generateRandomPassword(15))