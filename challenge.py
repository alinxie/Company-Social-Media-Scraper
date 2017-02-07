import requests
import re
from lxml import html
import json
from queue import Queue


# Regex Patterns for pattern matching the handles to links on the websites
patterns = {
    r'(https?:\/\/)?(www\.)?(twitter\.com\/)([a-zA-Z0-9_]{1,15})\/?': 'twitter',
    r'(https?:\/\/)?(www\.)?facebook\.com\/(pages\/)?([^\/\?]*)(\/|\?)?.*': 'facebook',
    r'(https?:\/\/)?(www\.)?itunes\.apple\.com\/(us\/)?app\/.*id([0-9]{8,11})\?.*' : 'ios',
    r'(https?:\/\/)?(www\.)?(play\.google\.com\/store\/apps\/details)\?id=((com|me)(\.[^&]+)+)&?.*': 'google',
    r'(https?:\/\/)?(www\.)?market\.android\.com\/(details)?\?id=(com(\.[^&]+)+)&?.*':'google'
    }

TARGET_GROUP = 4 # Regex structured so that 4th group is what we want
WEBSITE_R = r'(https?:\/\/)?(www\.)?([^\.]+)\.[a-z]{1,5}.*'
WEBSITE_NAME_GROUP = 3

def get_body(url):
    """
    Takes in a url and Returns the html string of
    the url or none if the url is malformed
    or there is an error with getting a request.
    """
    try:
        s = requests.Session()
        r = s.get(url, allow_redirects=True)
        root = html.fromstring(r.content)
        return root.body
    except Exception as e:
        print(e)
        return None

def get_handles(url): 
    """
    Main method for getting handles given a url.
    Writes the handle json strings to files.
    """
    d = {} # Dict of the websites of interest as keys and handles as values
    tree = get_body(url)
    if tree is None:
        print('Error with parsing ' + url)
        return
    # Queue to go through html tree in a breadth-first manner
    q = Queue()
    for child in tree: 
        q.put(child)
    while not q.empty(): 
        elem = q.get()
        # Want to get link tags that contain an href attribute
        if elem.tag == 'a' and 'href' in elem.attrib: 
            href = elem.get('href')
            for p in patterns:
                r = re.search(p, href)
                if r:
                    handle = r.group(TARGET_GROUP) 
                    website = patterns[p]
                    if website in d:
                        d[website].add(handle)
                    else:
                        d[website] = set([handle])
        for child in elem:
            q.put(child)
    for key, value in d.items(): 
        # This handles colliding website handles. 
        d[key] = best_handle(url, value)
    write_to_json(url, d)

def edit_dist(url, handle):
    """
    Given two strings, find the edit distance through Dynamic Programming

    >>> edit_dist('ant','ant')
    0
    >>> edit_dist('pants','ant')
    2
    """
    def match(char1, char2):
        if char1 == char2:
            return 0
        return 1
    dist = [
        [0 for j in range(len(handle)+1)]
        for i in range(len(url)+1)
        ]
    for i in range(1, len(url)+1):
        dist[i][0] = i
    for j in range(1, len(handle) + 1):
        dist[0][j] = j
    for i in range(1,len(url)+1):
        for j in range(1,len(handle)+1):
            url_index , handle_index = i - 1 , j - 1
            url_char = url[url_index]
            handle_char = handle[handle_index]
            dist[i][j] = min(
                dist[i-1][j]+1,
                dist[i][j-1]+1,
                dist[i-1][j-1] + match(url_char, handle_char)
                )
    return dist[len(url)][len(handle)]

def best_handle(url, handles):
    """
    If a url has a set of handles with a size greater than
    1 for one of the target websites (ie. twitter), compare
    the edit distance between each of the handles and the url
    and return handle with the minimum edit distance to the 
    Website name.
    """
    if len(handles) == 1:
        return handles.pop()
    r = re.search(WEBSITE_R, url)
    if r is not None:
        website_name = r.group(WEBSITE_NAME_GROUP)
    else:
        website_name = url
    return min(handles, key = lambda x: edit_dist(website_name, x))

def write_to_json(url, d):
    """
    Writing the dictionary of handles to a json with the url
    website name (www.NAME.com) as the filename
    """
    r = re.search(WEBSITE_R, url)
    website_name = r.group(WEBSITE_NAME_GROUP)
    filename = 'json_files/{}.json'.format(website_name)
    with open(filename, 'w') as f:
        json.dump(d, f)
        f.close()

# Main Function
def main():
    company_file = open('company_urls.txt', 'r')
    company_url_list = []
    for line in company_file:
        company_url_list.append(line.rstrip())
    for company in company_url_list:
        get_handles(company)
main()


"""
