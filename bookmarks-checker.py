import json, urllib.request, argparse

def checkBookmarkForIssues(bookmark, folderName):
  if (bookmark.get("uri")):
    url = bookmark.get("uri")
    # Check for UTM or FBClid parameters
    if ("utm" in url) or ("fbclid" in url) or ("gclid" in url):
      print("[!] utm or fbclid found: {}: {} - {}".format(url, folderName, bookmark.get("title")))
    if "http://" in url:
      print("[!] HTTP found: {}: {} - {}".format(url, folderName, bookmark.get("title")))
    elif "https://" in url:
      #print(url)
      pass
      # TODO - This is not working correctly yet:
      # print(httpRequestBookmark(url))
      # httpRequestBookmark(url)

def readBookmarks(bookmarksFile):
  with open(bookmarksFile, 'rb') as inFile:
    bookmarks = json.load(inFile)
    return bookmarks

def httpRequestBookmark(bookmarkURL):
  try:
    with urllib.request.urlopen(bookmarkURL, timeout=10) as response:
      print("Response Status Code: ", response.status)
      #pageResponse = response.read(300)
      #return pageResponse
  except urllib.error.URLError as e:
    return e.reason
  except Exception:
    pass

# -----------------------------------------------------------------------

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description="Check a json bookmarks file for duplicates, 404s, http vs https, etc.")
  parser.add_argument('-f', dest='file', help='Bookmarks (backup) file to read in', required=True)

  args = parser.parse_args()

  if (args.file):
    bookmarksJson = readBookmarks(args.file)

    # children[0] is the Bookmarks Menu folder, the children of that seems to be each folder.
    bookmarksFolders = bookmarksJson["children"][0]["children"]

    for folder in bookmarksFolders:
      # print(folder["title"])
      bookmarks = folder.get("children")
      if bookmarks:
        for bookmark in bookmarks:
          #print(bookmark["title"])
          # Check for "children" bookmarks, which are subfolders in this case.
          if (bookmark.get("children")):
            for childBookmark in bookmark.get("children"):
              checkBookmarkForIssues(childBookmark, bookmark.get("title"))
          else:
            checkBookmarkForIssues(bookmark, folder.get("title"))
  else:
    parser.print_help()
