import urllib.request
import re

# Taken from Django
def is_valid_url(url):
    urlRegex = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return urlRegex.search(url)

def getResponse(url):
    firefoxUserAgent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0'
    headers = {'User-Agent': firefoxUserAgent}

    if (not is_valid_url(url)):
        return "\n [!] Invalid URL provided"
    else:
        httpRequest = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(httpRequest) as response:
                pageResponse = response.read()
                return pageResponse
        except urllib.error.URLError as e:
            return e.reason

# ----------------------------------------- #
# Tests
print(getResponse("https://www.python.org/"))
print(getResponse("badUrl.http"))
