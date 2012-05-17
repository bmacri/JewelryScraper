from superparser import SuperParser
import re
import settings

class WinzlebergParser(SuperParser):
    
    RETAILER_ID = 5
    
    def __init__(self):
        pass

    def trim_contents(self,contents):
        begin_index = contents.find('<section id="body"')
        end_index = contents.find('<li class="active"', begin_index + 1)
        trimmed_contents = contents[begin_index:end_index]
        return trimmed_contents

    def winzleberg_product_urls(self,contents):
        domain = 'http://www.jessicawinzelberg.com'
        winzleberg_url_list = []
        trimmed_contents = self.trim_contents(contents)
        start_link = trimmed_contents.find('<a href=')
        if start_link == -1:
            return winzleberg_url_list
        start_quote = trimmed_contents.find('"', start_link)
        end_quote = trimmed_contents.find('"',start_quote+1)
        next_url = domain + trimmed_contents[start_quote + 1:end_quote]
        winzleberg_url_list.append(next_url)
        rest_of_urls = self.winzleberg_product_urls(trimmed_contents[end_quote + 1:])
        winzleberg_url_list.extend(rest_of_urls)
        return winzleberg_url_list
    
    def product_trim_page(self,contents):
        product_begins = contents.find('<div class="image">')
        product_ends = contents.find('More Products')
        contents = contents[product_begins:product_ends]
        return contents

    def get_product_name(self,contents):
        contents = self.product_trim_page(contents)
        find_product_name = contents.find('class="title"')
        name_begin = contents.find('>',find_product_name)
        name_end = contents.find('<', name_begin + 1)
        product_name = contents[name_begin + 1:name_end]
        return product_name

    def get_price(self,contents):
        contents = self.product_trim_page(contents)
        start_price_class = contents.find('"price-preview">')
        contents = contents[start_price_class:]
        match_get_price = re.search(r"\$[0-9]+\.[0-9][0-9]",contents)
        if match_get_price:
            price = match_get_price.group()
        else:
            return None
        return price

    def get_description(self, contents):
        contents = self.product_trim_page(contents)
        desc_element = contents.find('<div class="description">')
        details_begin_index = contents.find('<p>',desc_element)
        details_end_index = contents.find('</p>', details_begin_index + 1)
        description = contents[details_begin_index + 3:details_end_index] 
        return description

    
    def get_product_id(self,contents):
        contents = self.product_trim_page(contents)
        begin_id = contents.find('<option value=')
        end_id= contents.find('>', begin_id + 1)
        product_id = contents[begin_id + 15:end_id -1]
        return product_id
        
    def get_image(self, contents):
        contents = self.product_trim_page(contents)
        begin_image = contents.find('<a href="')
        end_image = contents.find('" class=', begin_image + 1)
        image = contents[begin_image + 9:end_image]
        return image

#-------------------------------------------------------------
winzleberg = WinzlebergParser()

contents = winzleberg.file_contents(settings.project_path + 'winzleberg_necklaces.html')
product_url_list = winzleberg.winzleberg_product_urls(contents)
assert product_url_list[0] == 'http://www.jessicawinzelberg.com/collections/category-necklaces/products/arabesque-candy-necklace-2', product_url_list[0]

contents = winzleberg.file_contents(settings.project_path + 'winzleberg_earrings.html')
product_url_list = winzleberg.winzleberg_product_urls(contents)
#assert product_url_list[0] == 'http://www.jessicawinzelberg.com/collections/category-earrings/products/arabesque-candy-earrings-1', product_url_list[0]

contents = winzleberg.file_contents(settings.project_path + 'winzleberg_bracelets.html')
product_url_list = winzleberg.winzleberg_product_urls(contents)
#assert product_url_list[0] == 'http://www.jessicawinzelberg.com/collections/category-bracelets/products/artifact-tip-cuff-bracelet', product_url_list[0]

contents = winzleberg.file_contents(settings.project_path + 'winzleberg_rings.html')
product_url_list = winzleberg.winzleberg_product_urls(contents)
#assert product_url_list[0] == 'http://www.jessicawinzelberg.com/collections/category-rings/products/arabesque-candy-ring', product_url_list[0]

contents = winzleberg.file_contents(settings.project_path + 'winzleberg_single_necklace.html')
assert winzleberg.get_product_name(contents) == 'Arabesque Candy Necklace', winzleberg.get_product_name(contents)
assert winzleberg.get_price(contents) == '$125.00', winzleberg.get_price(contents)
assert winzleberg.get_description(contents) == 'Arabesque Candy Necklace available in 14k Yellow Gold, 14k Rose Gold or Sterling Silver. &nbsp;Length measures approximately 1 inch long. Available on 16" or 18" chain.', winzleberg.get_description(contents)
assert winzleberg.get_product_id(contents) == '207587610', winzleberg.get_product_id(contents)
assert winzleberg.get_image(contents) == 'http://cdn.shopify.com/s/files/1/0095/0902/products/N9SSCandy_2.jpg?2489', winzleberg.get_image(contents)


