from superparser import SuperParser
import re
import settings

class NervousParser(SuperParser):

    RETAILER_ID = 3

    def __init__(self):
        pass    

    def trim_contents(self, contents):
        begin_index = contents.find('<div class="products_all"')
        end_index = contents.find('function sortProducts() {')
        contents = contents[begin_index:end_index] 
        return contents

    def nervous_product_urls(self, contents):
        domain = "http://www.n-e-r-v-o-u-s.com/"
        nervous_product_url_list = []
        contents = trim_contents(contents)   
        start_link = contents.find('<a href=')
        if start_link == -1:
            return nervous_product_url_list
        start_quote = contents.find('"',start_link)
        end_quote = contents.find('"', start_quote + 1)
        next_url = domain + contents[start_quote + 1:end_quote]
        nervous_product_url_list.append(next_url)
        rest_of_urls = nervous_product_urls(contents[end_quote+1:])
        nervous_product_url_list.extend(rest_of_urls)
        return nervous_product_url_list

    def trim_product_page(self, contents):
        begin_index = contents.find('<!-- RIGHT COLUMN')
        end_index = contents.find('<!--- right_column -->')
        contents = contents[begin_index:end_index]
        return contents

    def get_price(self,contents):
        

    def get_image(self, contents):
        

    def get_name(self, contents):

    def get_description(self, contents):
        contents = trim_product_page(contents)
        begin_desc = contents.find('<div class="p-description">') + len('<div class="p-description">')
        end_desc = contents.find('</div>', begin_desc + 1 )
        description = contents[begin_desc:end_desc]
        #description = description.lstrip()
        description = description.strip('\n p \t')
        description_list = re.split(r"[<>]",description)
        description = description_list[0].strip() + ' ' + description_list[2].lstrip()
        return description
        



#--------------------------------------------------------------------------------------------------------------------

#save_page('http://n-e-r-v-o-u-s.com/shop/product_tags.php?tag=jewelry', '/home/bethany/Jewelry_Crawler')
#test_date = date(2012,4,25)
contents = file_contents('2012-04-25-http:__n-e-r-v-o-u-s.com_shop_product_tags.php?tag=jewelry')
assert contents[:22]  == '<!DOCTYPE HTML PUBLIC ', contents[:22]
url_list = nervous_product_urls(contents)
assert url_list[0] == "http://www.n-e-r-v-o-u-s.com/product.php?code=109&tag=jewelry&osCsid=lisrvsa68qfu25mmo5u3mju806", url_list[0]

contents = file_contents('nervousproduct.html')
assert get_description(contents) == 'An intricate round pendant with a complex network of veins radiating from its center.  Reticulate, meaning net-like, describes the complex branching patterns that govern the veins in leaves of most flowering plants.  Tiny tertiary veins interconnect the thick primary and secondary ones to create a redundant system for the transportation of water, sugars, and nutrients. The pattern was grown in our computer simulation of leaf venation and etched from a sheet of stainless steel. Comes with an 18" sterling silver or gold-filled chain.  Choose from unfinished stainless steel, black chromium plated or gold plated.', get_description(contents)




