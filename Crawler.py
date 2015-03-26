#!/usr/bin/env python3
"""
Web Crawler by |MinestoPix|


Downloads the site specified and
all subsites and organizes them
into folders for offline browsing
"""
#########################
#                       #
#      Web Crawler      #
#          by           #
#    - MinestoPix -     #
#                       #
#########################
#                       #
# Download.py           #
#-----------------------#
#                       #
# Downloads the sites   #
#                       #
#########################

import urllib.request
from html.parser import HTMLParser
import os
import sys


# Target url
url = 'https://docs.python.org/3/library/'

# 0 = all
max_sites = 0

save_dir = 'Site/'


# Handle arguments
for index, arg in enumerate(sys.argv):
    if arg in ['-u', '--url'] and len(arg) > index:
        url = sys.argv[index+1]
    elif arg in ['-m', '--max'] and len(arg) > index:
        max_sites = int(sys.argv[index + 1])
    elif arg in ['-h', '--help']:
        print('usage: python3 Crawler.py [-u|--url URL, -m|--max max_number_of_sites]')
        quit()



# List of already downloaded sites
link_list = ['','index.html']
links_to_visit = ['']


class MyParser(HTMLParser):
    # Base for handling folders
    base = ''

    # Gets called when HTMLParser encounters a starting tag
    def handle_starttag(self, tag, attrs):
        global link_list
        global links_to_visit

        # If the tag is an anchor <a>
        if tag=='a':

            # Gets the link attribute (href='')
            for name, cont in attrs:
                if name=='href':
                    # Adds base and removes location links (#)
                    content = self.base + cont.split('#')[0]

                    # Filter out external and reoccuring links
                    if(not(cont.startswith('../') or cont.startswith('http://') or
                        cont.startswith('https://')) and not(content in link_list)):
                        link_list += [content]     # Finally add to list
                        links_to_visit += [content]

def search(mod_url='index.html'):
    global url
    dest_url = url + mod_url
    print(dest_url)

    # Exception handling for 404 and similar errors
    try:

        # Opens and reads url
        req = urllib.request.urlopen(dest_url)
        req_str = req.read()

        # Set name to mod_url or index.html if blank
        if mod_url == '':
            filename = save_dir + 'index.html'
        else:
            filename = save_dir + mod_url

        # Create folders
        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))

        # Save file
        with open(filename, "wb") as f:
            f.write(req_str)

        # Parse url for links
        parser = MyParser()

        # Set 'base' if needed
        if '/' in mod_url:
            parser.base = ''.join( mod_url.split('/')[:-1] ) + '/'
        parser.feed(str(req_str))
    except Exception as e:
        print(str(e))



# Program loop
count = 0
while len(links_to_visit) > 0 and (count < max_sites or max_sites == 0):
    count += 1
    link = links_to_visit[0]
    search(link)
    links_to_visit.remove(link)
