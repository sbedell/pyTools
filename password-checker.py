################################################################
#  
#  Checks a password against Troy Hunt's haveibeenpwned service.
#
#  https://haveibeenpwned.com/Passwords
#  https://www.troyhunt.com/introducing-306-million-freely-downloadable-pwned-passwords/
#  https://www.troyhunt.com/ive-just-launched-pwned-passwords-version-2/
#  https://www.troyhunt.com/enhancing-pwned-passwords-privacy-with-padding/
#
################################################################

import hashlib, urllib.request, argparse

## TODO - Add Headers:
"""
  headers: {
    'User-Agent': 'Pwnage-Checker-nodejs',
    'Add-Padding': true
  }
"""

def makeHttpRequest(url):
  try:
    with urllib.request.urlopen(url) as res:
      apiResponse = res.read()
      return apiResponse
  except urllib.error.URLError as e:
    return e.reason

def checkResponse(resp, hashDigest):
  # print(hashDigest[5:].upper())
  count = 0
  for line in resp.decode().split("\n"):
    # print(line[:line.index(":")])
    # print(line)
    if line[:line.index(":")] == hashDigest[5:].upper():
      # print("[!] Match:", line)
      count = int(line[line.index(":") + 1:])
  
  if (count > 0):
    print("[!] Pwned! This password has appeared this many times:", count)
  else:
    print("Congrats, no pwnage found!")

def checkPwnedPassword(password):
  hashedPw = hashlib.sha1()
  hashedPw.update(password.encode())
  sha1HashedPasswordDigest = hashedPw.hexdigest()
  # print("SHA1 Hash Digest:", sha1HashedPasswordDigest) # debug
  resp = makeHttpRequest("https://api.pwnedpasswords.com/range/" + sha1HashedPasswordDigest[:5])
  checkResponse(resp, sha1HashedPasswordDigest)

#---------------- Main --------------------------

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description="Check if a password is from a breach reported on Have I Been Pwned")
  parser.add_argument('-p', dest='password', help="Password to check", required=True)
  # parser.add_argument("-v", dest="verbose", action="store_true", help="Enables verbose output (not implemented yet).")

  args = parser.parse_args()

  if (args.password):
    checkPwnedPassword(args.password.strip())
  else:
    parser.print_usage()
