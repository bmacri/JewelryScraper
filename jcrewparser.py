from superparser import SuperParser
import re
import settings

class JcrewParser(SuperParser):

    RETAILER_ID = 4

    def __init__(self):
        pass

    def trim_contents(self,contents):
        begin_index = contents.find('"arrayCatFirst"')
        trimmed_contents = contents[begin_index:]
        return trimmed_contents

    def jcrew_product_urls(self,contents):
        jcrew_url_list = []
        trimmed_contents = self.trim_contents(contents)
        start_link = trimmed_contents.find('"arrayProdName"')
        if start_link == -1:
            return jcrew_url_list
        start_quote = trimmed_contents.find('=', start_link + 1)  
        end_quote = trimmed_contents.find('"', start_quote + 2 )
        next_url = trimmed_contents[start_quote + 2:end_quote]
        jcrew_url_list.append(next_url)
        rest_of_urls = trimmed_contents[end_quote + 1:]
        jcrew_url_list.extend(rest_of_urls)
        return jcrew_url_list

    def product_trim_page(self,contents):
        contents = self.file_contents('jcrew_product.html')
        product_begins = contents.find('pdp-title')
        product_ends = contents.find('<!--QUANTITY-->', product_begins + 1)
        contents = contents[product_begins + 1:product_ends]
        return contents

    def get_product_name(self,contents):
        contents = self.product_trim_page(contents)
        find_product_name = contents.find('<div class="product-name">')
        name_begin = contents.find('<h1>', find_product_name + 1)
        name_end = contents.find('</h1>',name_begin + 1)
        product_name = contents[name_begin + 4:name_end]    
        return product_name

    def get_price(self,contents):
        contents = self.product_trim_page(contents)        
        start_price_class = contents.find('price-single')
        contents = contents[start_price_class:]
        match_get_price = re.search(r"\$[0-9]+\.[0-9][0-9]",contents)
        if match_get_price:
            price = match_get_price.group()
        else:
            return None
        return price

    def get_description(self,contents):
        start_desc = contents.find('"product_desc">')
        end_desc = contents.find('<a class="moar-link"', start_desc + 1)
        description = contents[start_desc + 15:end_desc - 2]
        return description

    def get_product_id(self, contents):
        contents = self.product_trim_page(contents)
        begin_itemid_class = contents.find('class="itemid-single"')
        begin_id = contents.find('item', begin_itemid_class + 10)
        end_id = contents.find('<', begin_id + 1)
        product_id = contents[begin_id + 5:end_id]
        return product_id
        

    def get_image(self, contents):
        contents = self.product_trim_page(contents)
        begin_image = contents.find('mainImg="')
        end_image = contents.find('>', begin_image + 1)
        image = contents[begin_image + 9:end_image - 1]
        return image
  



#-------------------------------------------------------------------------------------------------
jcrew = JcrewParser()
contents = jcrew.file_contents(settings.project_path + 'jcrew_alljewelry.html')
jcrew_url_list = jcrew.jcrew_product_urls(contents)
assert jcrew_url_list[0] == 'http://www.jcrew.com/womens_category/jewelry/necklaces/PRDOVR~85042/85042.jsp', jcrew_url_list[0]

contents = jcrew.file_contents(settings.project_path + 'jcrew_product.html')
assert jcrew.get_product_name(contents) == 'Tessellate necklace', jcrew.get_product_name(contents)
assert jcrew.get_price(contents) == '$85.00', jcrew.get_price(contents)
assert jcrew.get_description(contents) == 'Pair this piece with a sweet strapless dress or rock it with a t-shirt and jeans&mdash;this monotone mosaic look goes...', jcrew.get_description(contents)
assert jcrew.get_product_id(contents) == '85042', jcrew.get_product_id(contents)
assert jcrew.get_image(contents) == 'http://s7.jcrew.com/is/image/jcrew/85042_GR6744?$pdp_fs418$', jcrew.get_image(contents)

        
