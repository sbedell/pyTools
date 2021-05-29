import hmac, hashlib, os, binascii, json

# Challenge from - https://hackattic.com/challenges/password_hashing

"""
Problem JSON structure is:
  password: the password you'll operate on
  salt: the salt we'll use - also user as a secret where necessary; keep in mind it comes base64 encoded - decode for the raw bytes
  pbkdf2:
    hash: the digest to use
    rounds: the number of rounds to use
  scrypt:
    N: the N parameter for scrypt's KDF
    p: the parallelization parameter
    r: the blocksize parameter
    buflen: intended output length in octets
    _control: example scrypt calculated for password="rosebud", salt="pepper", N=128, p=8, n=4
"""

"""
Your solution should be a JSON file with the following keys:
  sha256: the calculated SHA256
  hmac: the calculated HMAC-SHA256
  pbkdf2: the calculated PBKDF2 digest
  scrypt: finally, the calculated scrypt value

  Send all values in hexlified form, e.g. md5('foo') -> 7ddd5f60c97d589b0becc3c55d6afd25.
"""

with open("passwordTest.json", 'r') as inFile:
  jsonData = json.load(inFile)
  inputPassword = jsonData['password']
  # print(inputPassword)

  outputData = dict()

  pwhash = hashlib.sha256(inputPassword.encode())
  hexPwHash = pwhash.hexdigest()      # Got it - SHA256 calculated!
  outputData['sha256'] = pwhash.hexdigest()
  # print(hexPwHash)

  # Calculating the HMAC with SHA-256:
  pwHmac = hmac.HMAC(os.urandom(1024), inputPassword.encode(), hashlib.sha256)
  outputData['hmac'] = pwHmac.hexdigest()
  # print(pwHmac.hexdigest())

  # Calculate the pbkdf2:
  derivedKey = hashlib.pbkdf2_hmac(jsonData['pbkdf2']['hash'], inputPassword.encode(), jsonData['salt'].encode(), jsonData['pbkdf2']['rounds'])
  outputData["pbkdf2"] = binascii.hexlify(derivedKey).decode()
  # print(binascii.hexlify(derivedKey).decode()) # Got it! This works.

  # Calculate scrypt: Need Python 3.6+ to use scrypt. 
  # I keep getting this error... "ValueError: Invalid parameter combination for n, r, p, maxmem."
  # Checked out the documentation spec: https://datatracker.ietf.org/doc/html/rfc7914.html
  # "At the current time, r=8 and p=1 appears to yield good results..."
  # So now my values are "n": 16384 [side note: 2^14], "p": 1, "r": 8, and this appears to work
  try:
    finalScrypt = hashlib.scrypt(inputPassword.encode(), salt=jsonData['salt'].encode(), n=jsonData['scrypt']['n'], r=jsonData['scrypt']['r'], p=jsonData['scrypt']['p'])
    # print("Password scrypt: ", binascii.hexlify(finalScrypt).decode())
    outputData["scrypt"] = binascii.hexlify(finalScrypt).decode()
  except ValueError as verr:
    print("scrypt: ValueError: {0} \n".format(verr))
    outputData["scrypt"] = "error"

  print(json.dumps(outputData))