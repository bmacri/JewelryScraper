from datetime import date
import requests
import string
import re

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
       
def get_price(filename):
    product_dict = {}
    trim_contents(filename)
    dict_val = []
    for url in anthro_product_urls:
        begin_price_index = contents.find('$',url)
        end_price_index = contents.find('<', begin_price_index + 1)
        price = contents[begin_price_index:end_price_index]
        dict_val.append(price)
        product_dict[url] = dict_val
    return product_dict

"""def get_image(filename):
    trim_contents(filename)
    for url in anthro_product_urls:
        begin_img_index = contents.find('image src',url)
        end_img_index = contents.find('"', begin_img_index + 1)
        image = contents[begin_img_index:end_img_index]
        dict_val.append(image)
        product_dict[url] = dict_val
    return product_dict"""

def product_details(contents):
    "takes the contents of a file and creates a dictionary with the string 'name' as key and the value as the name of the product"
    product_dict = {}    
    product_dict['name'] = get_product_name(contents) 
    product_dict['product_id'] = get_product_id(contents)  
    return product_dict

def get_product_name(contents):
    start_meta = contents.find('<meta property="og:title" content=')
    start_og = contents.find('"', start_meta + 1)
    end_og = contents.find('"', start_og + 1)
    start_quote = contents.find('"', end_og + 1)
    end_quote = contents.find('"', start_quote + 1)
    product_name = contents[start_quote + 1:end_quote]
    return product_name
    
def get_product_id(contents):
    find_canonical = contents.find('<link rel="canonical"')
    contents = contents[find_canonical:]
    match_product_id = re.search(r"[A-Z]?[0-9]+",contents)
    if match_product_id:
        product_id = match_product_id.group()
    else:
        return None
    return product_id

contents = file_contents('/home/bethany/Jewelry_Crawler/jewelryaccessories-shopjewelry.jsp')
#assert anthro_product_urls(contents)[0] == "/anthro/product/jewelryaccessories-shopjewelry/23918493.jsp", anthro_product_urls(contents)[0]
#assert anthro_product_urls(contents)[1] == "/anthro/product/jewelryaccessories-shopjewelry/A23918493.jsp", anthro_product_urls(contents)[1]
#assert anthro_product_urls(contents)[-1] == "/anthro/product/jewelryaccessories-shopjewelry/24111676.jsp", anthro_product_urls(contents)[-1]
#assert trim_contents(contents)[:27] == '<div class="category-item">'


#contents = file_contents('stacked_stone.html')
product = product_details(contents)
#assert product['name'] == "Stacked Stone Drops", product['name']

contents = file_contents('prod_id_with_letter.html')
assert get_product_id(contents) == 'A23918493', get_product_id(contents)

#assert generate_filename('www.google.com') == '2012-04-15-www.google.com',generate_filename('www.google.com')
 

#get_urls('websites.txt','/home/bethany/Jewelry_Crawler')

#TODO: write out sql commands to create tables in a text file
    
