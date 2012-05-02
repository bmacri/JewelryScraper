from superparser import SuperParser
import settings



class AnthroParser(SuperParser):
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

anthro = AnthroParser()

contents = anthro.file_contents(settings.project_path + 'anthro_alljewelry.jsp')
assert anthro.get_product_urls(contents)[0] == "http://www.anthropologie.com/anthro/product/jewelryaccessories-shopjewelry/23918493.jsp", anthro.get_product_urls(contents)[0]
assert anthro.get_product_urls(contents)[1] == "http://www.anthropologie.com/anthro/product/jewelryaccessories-shopjewelry/A23918493.jsp", anthro.get_product_urls(contents)[1]
assert anthro.get_product_urls(contents)[-1] == "http://www.anthropologie.com/anthro/product/jewelryaccessories-shopjewelry/24111676.jsp", anthro.get_product_urls(contents)[-1]
assert anthro.trim_contents(contents)[:27] == '<div class="category-item">'
