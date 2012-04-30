
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
    alexani_url_list = []
    trimmed_contents = trim_contents(contents)
    start_link = trimmed_contents.find('<a href=')
    if start_link == -1:
        return alexani_url_list
    start_quote = trimmed_contents.find('"', start_link)
    end_quote = trimmed_contents.find('"',start_quote+1)
    next_url = trimmed_contents[start_quote + 1:end_quote]
    alexani_url_list.append(next_url)
    rest_of_urls = alexani_product_urls(trimmed_contents[end_quote + 1:])
    alexani_url_list.extend(rest_of_urls)
    return alexani_url_list

def product_trim_page(contents):
    contents = file_contents('alexandani_single_bracelet.html')
    product_begins = contents.find('<li class="product">')
    product_ends = contents.find('<script type="text/javascript">var switchTo5x=true;</script>', product_begins + 1)
    contents = contents[product_begins + 1:product_ends]
    return contents
    

def product_details(contents):
    product_dict = {}
    product_dict['name'] = get_product_name(contents)
    product_dict['product_id'] = get_product_id(contents) 
    product_dict['price'] = get_price(contents)
    product_dict['image'] = get_image(contents)
    product_dict['description'] = get_description(contents)
    return product_dict
    
def get_product_name(contents):
    contents = product_trim_page(contents)
    find_product_name = contents.find('<div class="product-name">')
    name_begin = contents.find('<h1>', find_product_name + 1)
    name_end = contents.find('</h1>',name_begin + 1)
    product_name = contents[name_begin + 4:name_end]    
    return product_name

def trim_single_page(contents):
    start_trim = contents.find('<div class="product-shop">')
    contents = contents[start_trim:]
    return contents

def get_price(contents):
    contents = trim_single_page(contents)
    start_price_class = contents.find('<span class="price">')
    contents = contents[start_price_class:]
    match_get_price = re.search(r"\$[0-9]+\.[0-9][0-9]",contents)
    if match_get_price:
        price = match_get_price.group()
    else:
        return None
    return price

def get_description(contents):
    start_class_desc = contents.find('<div class="short-description">')
    start_desc = contents.find('<br><br>', start_class_desc)
    end_desc = contents.find('<br><br>', start_desc + 1)
    description = contents[start_desc + 9:end_desc - 1]
    return description

def get_product_id(contents):
    contents = trim_single_page(contents)
    find_sku_class = contents.find('<div class="product-sku-display">')
    begin_sku = contents.find('"sku">', find_sku_class + 1)
    end_sku= contents.find('</span>', begin_sku + 1)
    product_id = contents[begin_sku + 6:end_sku]
    return product_id

def get_image(contents):
    contents = trim_single_page(contents)
    find_img_class = contents.find('<div class="product-img-box">')
    begin_image = contents.find('<img src=', find_img_class + 1)
    end_image = contents.find('alt=', begin_image + 1)
    image = contents[begin_image + 10:end_image - 2]
    return image
                                         
    

#---------------------------------------------------------------------------------------------------------------------------------------------------

contents = file_contents('alexandani_bracelets.html')
product_url_list = alexani_product_urls(contents)
assert product_url_list[0] == 'http://www.alexandani.com/bracelets/young-and-strong-expandable-wire-bangle-russian-silver.html', product_url_list[0]

contents = file_contents('alexandani_single_bracelet.html')
assert get_product_name(contents) == 'Young and Strong Expandable Wire Bangle - Russian Silver', get_product_name(contents)
assert get_price(contents) == '$28.00', get_price(contents)
assert get_description(contents) == "The Young and Strong symbol is a tribute to remarkable women of courage. Wear this bangle to inspire empowerment, love, and healing through the power of positive thinking. Designed to wear alone, or to layer for a customized look, Alex and Ani's patented Expandable Wire Bangle is the most innovative concept in jewelry, allowing the wearer, with the slide of a hand, to adjust the bangle for a perfect fit. The Young and Strong Bangle is available in a Russian Gold and Russian Silver finish.", get_description(contents)
assert get_product_id(contents) == 'CBD11YS03RS', get_product_id(contents)
assert get_image(contents) == 'http://cdn.alexandani.com/media/catalog/product/cache/1/image/300x/9df78eab33525d08d6e5fb8d27136e95/C/B/CBD11YS03RS_5_3_5_1.JPG', get_image(contents)










