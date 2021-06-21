import hashlib, argparse

# Hash a file using MD5, SHA-1, or SHA-256. 
# Optionally check that hash against a checksum.
# Using argparse to let the user choose the file and hashing algorithm.
# -----------------------------------------------------------------------

def getFileHash(fileToHash, hashAlgo):
  filehash = hashlib.sha256()
  if (hashAlgo == "md5"):
    filehash = hashlib.md5()
  elif (hashAlgo == "sha1"):
    filehash = hashlib.sha1() 
  
  with open(fileToHash, 'rb') as f:
    fileBuffer = f.read()
    filehash.update(fileBuffer)
  return filehash

def checkChecksum(filehash, checksum):
  return "Yes" if (filehash.lower() == checksum.lower()) else "No"

# -----------------------------------------------------------------------

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description="Hash a file using SHA-1, SHA-256, or MD5.")
  parser.add_argument('-f', dest='file', help='File to hash', required=True)
  parser.add_argument('--hash', dest='hashType', help="The hashing algoritm to use", default="sha256")
  parser.add_argument("-c", dest="hashChecksum", help="Hash / Checksum to check against the file hash.")
  parser.add_argument("-v", dest="verbose", action="store_true", help="Enables verbose output (not implemented yet).")

  args = parser.parse_args()

  if (args.file):
    if (not args.hashType): 
      print("Error, please enter a valid hashing algorithm to use.")
    else:
      filehashdigest = getFileHash(args.file, args.hashType).hexdigest()
      if (args.verbose):
        print("\nThe {} of {} is \n{}".format(args.hashType, args.file, filehashdigest))
      else:
        print(filehashdigest)

      if (args.hashChecksum):
        print(args.hashChecksum)
        print("\nChecksum match? ", checkChecksum(filehashdigest, args.hashChecksum))
