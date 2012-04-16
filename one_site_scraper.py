from datetime import date
import requests



def save_page(url,filepath):
    if not url.startswith('http'):
        raise Exception('url must start with http')
    contents = get_contents(url)
    filename = generate_filename(url)
    filename = filename.replace('/','_')
    f = open(filepath + '/' + filename,'w')
    f.write(contents)
    f.close()
    return 

def get_contents(url):
    r = request.get(url)
    contents = r.text
    return contents

def get_urls(websites_file,filepath): 
    f = open(websites_file,'r')
    url_list = []
    for url in f:
        url_list.append(line)
    for url in url_list:
        save_page(url,filepath)
    return


class AnthroParser:
    def next_level_urls(self,contents):
        pass



    def product_urls(self,contents):
        pass

f = open('jewelryaccessories-shopjewelry.jsp','r')
ap = AnthroParser()
urls = ap.product_urls(f.read())

assert urls[0] == 'http://www.anthropologie.com/anthro/product/jewelryaccessories-shopjewelry/23918493.jsp', urls[0]

def generate_filename(url,file_date=None):
    if file_date == None:
        file_date = date.today()
    filename = str(file_date) + '-' + url
    return filename

assert generate_filename('www.google.com') == '2012-04-15-www.google.com',generate_filename('www.google.com')
 

#https://gist.github.com/973705

get_urls('websites.txt','/home/bethany/Jewelry_Crawler')
    

