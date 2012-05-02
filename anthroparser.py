from superparser import SuperParser
import settings
import re
from datetime import date

class AnthroParser(SuperParser):
    
    RETAILER_ID = 1

    def __init__(self):
        pass

    def trim_contents(self,contents):
        begin_index = contents.find('<div class="category-item"')
        end_index = contents.find('<a name="pagelast" id="pagelast" href=""></a>')
        trimmed_contents = contents[begin_index:end_index] 
        return trimmed_contents

    def get_product_urls(self,contents):
        domain = "http://www.anthropologie.com"
        anthro_product_url_list = []
        trimmed_contents = self.trim_contents(contents)   
        start_link = trimmed_contents.find('<a href=')
        if start_link == -1:
            return anthro_product_url_list
        start_quote = trimmed_contents.find('"',start_link)
        end_quote = trimmed_contents.find('"', start_quote + 1)
        next_url = domain + trimmed_contents[start_quote + 1:end_quote]
        anthro_product_url_list.append(next_url)
        rest_of_urls = self.get_product_urls(trimmed_contents[end_quote+1:])
        anthro_product_url_list.extend(rest_of_urls)
        return anthro_product_url_list


    def get_product_name(self,contents):
        start_meta = contents.find('<meta property="og:title" content=')
        start_og = contents.find('"', start_meta + 1)
        end_og = contents.find('"', start_og + 1)
        start_quote = contents.find('"', end_og + 1)
        end_quote = contents.find('"', start_quote + 1)
        product_name = contents[start_quote + 1:end_quote]
        return product_name

    def ignore_also_like(self,contents):
        also_like = contents.find('you may also like')
        contents = contents[:also_like]
        return contents
        
    def get_product_id(self,contents):
        contents = self.ignore_also_like(contents)
        find_canonical = contents.find('<link rel="canonical"')
        contents = contents[find_canonical:]
        match_product_id = re.search(r"[A-Z]?[0-9]+",contents)
        if match_product_id:
            product_id = match_product_id.group()
        else:
            return None
        return product_id

    def get_price(self,contents):
        contents = self.ignore_also_like(contents)
        match_get_price = re.search(r"\$[0-9]+\.[0-9][0-9]",contents)
        if match_get_price:
            price = match_get_price.group()
            price = price[1:]
        else:
            return None
        return price

    def get_image(self,contents):
        contents = self.ignore_also_like(contents)
        find_img_tag = contents.find('<img')
        start_img_url = contents.find("src='", find_img_tag)
        end_img_url = contents.find("'",start_img_url+5)
        image = contents[start_img_url+5:end_img_url]
        return image

    def get_description(self,contents):
        contents = self.ignore_also_like(contents)
        desc_element = contents.find('<div id="productDescription">')
        details_index = contents.find('DETAILS',desc_element)
        contents = contents[details_index+7:]
        non_angle = re.split(r"[<>]",contents)
        description = []
        i=0
        while i<len(non_angle):
            if i % 2 == 0:
                description.append(non_angle[i].strip('\n '))
            i = i + 1
        description = filter(None, description)
        description = " ".join(description)
        return description

   

#------------------------------------------------------------------------------------------------------

anthro = AnthroParser()

contents = anthro.file_contents(settings.project_path + 'anthro_alljewelry.jsp')
anthro_url_list = anthro.get_product_urls(contents)
assert anthro_url_list[0] == "http://www.anthropologie.com/anthro/product/jewelryaccessories-shopjewelry/23918493.jsp", anthro_url_list[0]
assert anthro_url_list[1] == "http://www.anthropologie.com/anthro/product/jewelryaccessories-shopjewelry/A23918493.jsp", anthro_url_list[1]
assert anthro_url_list[-1] == "http://www.anthropologie.com/anthro/product/jewelryaccessories-shopjewelry/24111676.jsp", anthro_url_list[-1]
assert anthro.trim_contents(contents)[:27] == '<div class="category-item">', anthro.trim_contents(contents)[:27]

contents = anthro.file_contents(settings.project_path + 'stacked_stone.html')
product = anthro.product_details(contents)
assert product['name'] == "Stacked Stone Drops", product['name']

assert anthro.get_price(contents) == "158.00", anthro.get_price(contents)

assert anthro.get_image(contents) == 'http://images.anthropologie.com/is/image/Anthropologie/23918493_040_b?$product410x615$', anthro.get_image(contents)

assert anthro.get_description(contents) == 'Slabs of turquoise or jade dangle faceted quartz orbs. By Sura Jewelry. Quartz, 24k gold plated bronze, jade 1.5"L, 0.75"W Turkey', anthro.get_description(contents) 

contents = anthro.file_contents('prod_id_with_letter.html')
assert anthro.get_product_id(contents) == 'A23918493', anthro.get_product_id(contents)

test_date = date(2012,4,15)
assert anthro.generate_filename('www.google.com',file_date=test_date) == '2012-04-15-www.google.com',anthro.generate_filename('www.google.com')

assert anthro.get_description(contents) == 'Slabs of turquoise or jade dangle faceted quartz orbs. By Sura Jewelry. Quartz, 24k gold plated bronze, turquoise 1.5"L, 0.75"W Turkey', anthro.get_description(contents)

def manual_test():
    page = anthro.file_contents(settings.project_path + 'stacked_stone.html')
    details = anthro.product_details(page)
    anthro.product_details_to_db(details)
    anthro.product_details_to_db(details)

def create_crawl_list():
    crawl_list = []    
    f = open('websites.txt', 'r')
    for website in f:
        crawl_list.append(website)
    return crawl_list

assert crawl_list[0] == 'http://www.anthropologie.com/anthro/category/shop+all+jewelry/jewelryaccessories-shopjewelry.jsp', crawl_list[0]


#def scrape_all(websites_list):














