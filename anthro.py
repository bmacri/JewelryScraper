from datetime import date
import requests
import string
import re
import MySQLdb
import settings 

def get_urls(websites_file,filepath):
    #reads urls in the websites.txt one by one, adding to a url list and then creating a filename using generate_filename
    f = open(websites_file,'r')
    url_list = []
    for url in f:
        url_list.append(url)
    for url in url_list:
        generate_filename(url)
    return


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

#f = open(filename,'r') #should i call this contents instead of f?

def trim_contents(contents):
    begin_index = contents.find('<div class="category-item"')
    end_index = contents.find('<a name="pagelast" id="pagelast" href=""></a>')
    trimmed_contents = contents[begin_index:end_index] 
    return trimmed_contents

def anthro_product_urls(contents):
    domain = "http://www.anthropologie.com"
    anthro_product_url_list = []
    trimmed_contents = trim_contents(contents)   
    start_link = trimmed_contents.find('<a href=')
    if start_link == -1:
        return anthro_product_url_list
    start_quote = trimmed_contents.find('"',start_link)
    end_quote = trimmed_contents.find('"', start_quote + 1)
    next_url = domain + trimmed_contents[start_quote + 1:end_quote]
    anthro_product_url_list.append(next_url)
    rest_of_urls = anthro_product_urls(trimmed_contents[end_quote+1:])
    anthro_product_url_list.extend(rest_of_urls)
    return anthro_product_url_list

def product_details(contents):
    "takes the contents of a file and creates a dictionary with the string 'name' as key and the value as the name of the product"
    product_dict = {}    
    product_dict['name'] = get_product_name(contents) 
    product_dict['product_id'] = get_product_id(contents)
    product_dict['price'] = get_price(contents)
    product_dict['image'] = get_image(contents)
    return product_dict

def get_product_name(contents):
    start_meta = contents.find('<meta property="og:title" content=')
    start_og = contents.find('"', start_meta + 1)
    end_og = contents.find('"', start_og + 1)
    start_quote = contents.find('"', end_og + 1)
    end_quote = contents.find('"', start_quote + 1)
    product_name = contents[start_quote + 1:end_quote]
    return product_name

def ignore_also_like(contents):
    also_like = contents.find('you may also like')
    contents = contents[:also_like]
    return contents
    
def get_product_id(contents):
    contents = ignore_also_like(contents)
    find_canonical = contents.find('<link rel="canonical"')
    contents = contents[find_canonical:]
    match_product_id = re.search(r"[A-Z]?[0-9]+",contents)
    if match_product_id:
        product_id = match_product_id.group()
    else:
        return None
    return product_id

def get_price(contents):
    contents = ignore_also_like(contents)
    match_get_price = re.search(r"\$[0-9]+\.[0-9][0-9]",contents)
    if match_get_price:
        price = match_get_price.group()
    else:
        return None
    return price

def get_image(contents):
    contents = ignore_also_like(contents)
    find_img_tag = contents.find('<img')
    start_img_url = contents.find("src='", find_img_tag)
    end_img_url = contents.find("'",start_img_url+5)
    image = contents[start_img_url+5:end_img_url]
    return image


def product_details_to_db(product_dict):
    conn = MySQLdb.connect(host= "localhost",
                  user="root",
                  passwd = settings.db_password,
                  db="jewelryscraperdb")
    cursor = conn.cursor()
    cursor.execute (" SELECT * FROM products WHERE product_id = %s ", (product_dict['product_id']))
    rows = cursor.fetchall()
    if len(rows) == 0: 
        cursor.execute (" INSERT INTO products (product_name,product_id) VALUES (%s,%s,%s,%s) ", (product_dict['name'],product_dict['product_id'],product['price'],product['image']))
    #TODO: need to select on retailer_id and on product_id to check that multiple retailers don't have the same product_id

contents = file_contents('/home/bethany/Jewelry_Crawler/anthro_alljewelry.jsp')
assert anthro_product_urls(contents)[0] == "http://www.anthropologie.com/anthro/product/jewelryaccessories-shopjewelry/23918493.jsp", anthro_product_urls(contents)[0]
assert anthro_product_urls(contents)[1] == "http://www.anthropologie.com/anthro/product/jewelryaccessories-shopjewelry/A23918493.jsp", anthro_product_urls(contents)[1]
assert anthro_product_urls(contents)[-1] == "http://www.anthropologie.com/anthro/product/jewelryaccessories-shopjewelry/24111676.jsp", anthro_product_urls(contents)[-1]
assert trim_contents(contents)[:27] == '<div class="category-item">'


contents = file_contents('stacked_stone.html')
product = product_details(contents)
assert product['name'] == "Stacked Stone Drops", product['name']

assert get_price(contents) == "$158.00", get_price(contents)

assert get_image(contents) == 'http://images.anthropologie.com/is/image/Anthropologie/23918493_040_b?$product410x615$', get_image(contents)


contents = file_contents('prod_id_with_letter.html')
assert get_product_id(contents) == 'A23918493', get_product_id(contents)

test_date = date(2012,4,15)
assert generate_filename('www.google.com',file_date=test_date) == '2012-04-15-www.google.com',generate_filename('www.google.com')
 

#get_urls('websites.txt','/home/bethany/Jewelry_Crawler')

#TODO: write out sql commands to create tables in a text file
    
