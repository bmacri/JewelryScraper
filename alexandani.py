
from datetime import date
import requests
import string
import re
import MySQLdb
import settings

def get_contents(url):
    r = requests.get(url)
    contents = r.text
    return contents

def generate_filename(url, file_date = None):
    if file_date == None:
        file_date = date.today()
    filename = str(file_date) + '-' + url
    return filename

def save_page(url,filepath):
    if not url.startswith('http'):
        raise Exception('url must start with http')
    contents = get_contents(url)
    filename = generate_filename(url)
    filename = filename.replace('/','_')
    f = open(filepath + '/' + filename, 'w')
    f.write(contents)
    f.close
    return

def file_contents(filename):
    f = open(filename, 'r')
    contents = f.read()
    f.close()
    return contents

def trim_contents(contents):
    begin_index = contents.find('<li class="item first">')
    trimmed_contents = contents[begin_index:]
    return trimmed_contents

def alexani_product_urls(contents):
    domain = "http://www.alexandani.com"
    alexani_url_list = []
    trimmed_contents = trim_contents(contents)
    start_link = trimmed_contents.find('<a href=')
    if start_link == -1:
        return alexani_url_list
    start_quote = trimmed_contents.find('"', start_link)
    end_quote = trimmed_contents.find('"',start_quote+1)
    next_url = domain + trimmed_contents[start_quote + 1:end_quote]
    alexani_url_list.append(next_url)
    rest_of_urls = alexani_product_urls(trimmed_contents[end_quote + 1:])
    alexani_product_urls(rest_of_urls)
    return alexani_url_list

def product_trim_page(contents):
    contents = file_contents('alexandani_single_bracelet.html')
    product_begins = contents.find('<li class="product">')
    product_ends = contents.find('<script type="text/javascript">var switchTo5x=true;</script>', product_begins + 1)
    contents = contents[product_begins + 1:product_ends]
    return contents
    

'''def product_details(contents):
    product_dict = {}
    product_dict['name'] = get_product_name(contents)
    product_dict['product_id'] = get_product_id(contents) 
    product_dict['price'] = get_price(contents)
    product_dict['image'] = get_image(contents)
    product_dict['description'] = get_description(contents)
    return product_dict'''
    
def get_product_name(contents):
    contents = product_trim_page(contents)
    find_product_name = contents.find('<div class="product-name">')
    name_begin = contents.find('<h1>', find_product_name + 1)
    name_end = contents.find('</h1>',name_begin + 1)
    product_name = contents[name_begin + 4:name_end]    
    return product_name

                                         
    

#-----------------------------------------------------------------------------

contents = file_contents('alexandani_single_bracelet.html')
assert get_product_name(contents) == 'Young and Strong Expandable Wire Bangle - Russian Silver', get_product_name(contents)
