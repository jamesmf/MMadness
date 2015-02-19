import urllib2
import re
import HTMLParser

BASE_URL = "http://www.sports-reference.com"
SCHOOLS_URL = BASE_URL + "/cbb/schools"

def get_schools_list():
    to_return = []
    schools_conn = urllib2.urlopen(SCHOOLS_URL)
    schools_html = schools_conn.read()
    for line in schools_html.split("\n"):
        match = re.search("<td align=\"left\" ><a href=", line)
        if match:
            school_url = line.split("<td align=\"left\" ><a href=\"")[1]
            to_return.append(school_url.split("\"")[0])
    return to_return

schools_list = get_schools_list()

for school in schools_list:
    BASE_URL + school
