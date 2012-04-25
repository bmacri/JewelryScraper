from datetime import date
import requests
import string
import re
import MySQLdb
import settings

def get_contents(url):
    #goes to a webpage, and saved the html on that page to the variable contents
    r = requests.get(url)
    contents = r.text
    return contents

def generate_filename(url,file_date=None):
    "generates a filename which will appear as 'date-url'"
    if file_date == None:
        file_date = date.today()
    filename = str(file_date) + '-' + url
    return filename

#Removed the get_urls function used in the anthro.py file

def save_page(url,filepath):
    #writes the contents of a url to file created with generate file and saves it under the filepath given
    if not url.startswith('http'):
        raise Exception('url must start with http')
    contents = get_contents(url)
    filename = generate_filename(url)
    filename = filename.replace('/','_')
    f = open(filepath + '/' + filename,'w')
    f.write(contents)
    f.close()
    return 

def file_contents(filename):
    "opens a file (NOT a webpage, as in get_contents), reads the text of the file, assigns it to variable contents and returns contents"
    f = open(filename, 'r')
    contents = f.read()
    f.close()
    return contents

save_page('http://n-e-r-v-o-u-s.com/shop/product_tags.php?tag=jewelry', '/home/bethany/Jewelry_Crawler')
test_date = date(2012,4,25)
contents = file_contents('2012-04-25-http:__n-e-r-v-o-u-s.com_shop_product_tags.php?tag=jewelry')
assert contents[:22]  == '<!DOCTYPE HTML PUBLIC ', contents[:22]








