import urllib2
import re
import HTMLParser
import lxml
from lxml import html

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
    
def read_table():
    tree = html.parse('http://www.sports-reference.com/cbb/schools/')
    table = tree.findall('//table')[0]
    #print lxml.etree.tostring(table, pretty_print=True)
    for child in table[2]:
        for child2 in child:
            print child2.text_content()
    data = [ [td.text_content().strip() for td in row.findall('td')] for row in table.findall('tr')]
    return data
    
def table_parse(url,parse):
    tree = html.parse(url)
    my_table = tree.findall("//table")[0]
    header_dict = {}
    for child in my_table:
        count = 0
        if child.tag == "thead":
            for headRow in child:
                if not headRow.get("class") == " over_header":
                    for cell in headRow:
                        if not cell.get("data-stat") == None:
                            header_dict[cell.get("data-stat")] = count
                            count+=1
        elif child.tag == "tbody":
            table=[]
            for row in child:
                r=[]
                for col in row:
                    x = col.text_content()
                    if parse == "yes":
                        for subelement in col:
                            if subelement.tag == "a":
                                x = subelement.get("href")
                    r.append(x)
                table.append(r)
    print header_dict
    return header_dict, table
                    
def write_names():               
    header_dict, table = table_parse(SCHOOLS_URL,"yes")    
    ncaa = header_dict['ncaa_count']
    teamname= header_dict['school_name']
    table2 = []
    for row in table:
        try:
            row[ncaa] = int(row[ncaa])
        except ValueError:
            pass
        if row[0] == "Rk":
            pass
        elif (not row[ncaa] == '') & (row[ncaa] > 1):
            print row[ncaa]
            row[teamname] = row[teamname].split("schools/")[1][:-1]
            table2.append(row[teamname].replace("\n",''))
     
    with open("../data/teamnames.txt",'wb') as f:    
        for row in table2:
            f.write(row+"\n")
            
            
def download_gamelogs():
    with open("../data/teamnames.txt","rb") as f:
        names = f.readlines()
    prefix = "20"
    for year in range(11,16):
        for college in names:
            college = college.replace("\n",'')
            fold = str(year-1)+str(year)
            ystring = prefix+str(year)
            url = SCHOOLS_URL+"/"+college+"/"+ystring+"-gamelogs.html"
            print url
            d,tab = table_parse(url,"no")
            with open("../data/"+fold+"/"+college+".txt","wb") as f2:
                for i in range(0,len(d)):
                    for k,v in d.iteritems():
                        if v == i:
                            f2.write(k+"|")
                f2.write("\n")
                for row in tab:
                    if not ((row[0] == "Rk") | (row[1] == "School")):
                        f2.write(("|".join(row).encode('utf8')))                 
                        f2.write("\n")
            print tab
            
 
if __name__ == "__main__":       
    write_names()  
    download_gamelogs()
     
