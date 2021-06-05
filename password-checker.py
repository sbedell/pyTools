"""
/**
 * Calls out to Troy Hunt's Have I Been Pwned APIs
 *  
 * Checks a password against Troy Hunt's haveibeenpwned service.
 * This can check plain text passwords and SHA1 hashes of passwords.
 *  
 * https://haveibeenpwned.com/Passwords
 * https://www.troyhunt.com/introducing-306-million-freely-downloadable-pwned-passwords/
 * https://www.troyhunt.com/ive-just-launched-pwned-passwords-version-2/
 * https://www.troyhunt.com/authentication-and-the-have-i-been-pwned-api/
 */
 """ 

import hashlib, urllib.request, argparse

def makeHttpRequest(url):
	try:
		with urllib.request.urlopen(url) as apiResponse:
			pageResponse = apiResponse.read()
			return pageResponse
	except urllib.error.URLError as e:
		return e.reason

def checkPwnedPassword(password):
  hashedPw = hashlib.sha1()
  hashedPw.update(password.encode())
  sha1HashedPasswordDigest = hashedPw.hexdigest()
  print("SHA1 Hash Digest:", sha1HashedPasswordDigest) # debug
  slicedPwHash = sha1HashedPasswordDigest[:5]

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

"""
function hasPasswordBeenPwned(yourPassword) {

  const options = {
    hostname: 'api.pwnedpasswords.com',
    path: '/range/' + sha1hashedPasswordDigest.slice(0,5),
    headers: {
      'User-Agent': 'Pwnage-Checker-nodejs',
      'Add-Padding': true
    }
  };
  
  console.log("Querying " + options.hostname + options.path); // INFO

  https.get(options, (response) => {
    if (response.statusCode == 200) {
      let str = '';
      response.on('data', (chunk) => {
        str += chunk;
      });

      response.on('end', () => {        
        let match = false;
        let count = 0;
        
        str.split("\n").forEach(line => {
          // console.log(line.slice(0, line.indexOf(":"))); // DEBUG
          
          if (sha1hashedPasswordDigest.slice(5).toUpperCase() == line.slice(0, line.indexOf(":"))) {
            // console.log("[!!] we have a match!!\n"); // DEBUG
            count = Number.parseInt(line.slice(line.indexOf(":") + 1));
            // TODO - Check if count is 0, that's just padding then, throw it out.
            match = true;
          }
        });

        if (match) {
          console.log(`\n[!] PWNED - this password has been seen ${count} times before.`);
          console.log("\"This password has previously appeared in a data breach and should never be used. If you've ever used it anywhere before, change it!\"");
          console.log(" - Troy Hunt");
        } else {
          console.log(`\nGood news — no pwnage found.
          This password wasn't found in any of the Pwned Passwords loaded into Have I been pwned. That doesn't necessarily mean it's a good password, merely that it's not indexed on this site.
          - Troy Hunt
          `);
        }
      });
    } else {
      console.log('Status Code: ' + response.statusCode);
      if (response.statusCode == 429) { console.log("Rate limited :("); }
    }
  }).on('error', e => {
    console.error(e);
  });
}

"""