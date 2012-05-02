from datetime import date
import requests
import MySQLdb
import settings 

class SuperParser:
    def __init__(self):
        pass

    def get_contents(self,url):
    #goes to a webpage, and saved the html on that page to the variable contents
        r = requests.get(url)
        contents = r.text
        return contents

    def generate_filename(self,url,file_date=None):
        "generates a filename which will appear as 'date-url'"
        if file_date == None:
            file_date = date.today()
        filename = str(file_date) + '-' + url
        return filename

    def save_page(self,url,filepath):
        #writes the contents of a url to file created with generate file and saves it under the filepath given
        if not url.startswith('http'):
            raise Exception('url must start with http')
        contents = self.get_contents(url)
        filename = self.generate_filename(url)
        filename = filename.replace('/','_')
        f = open(filepath + '/' + filename,'w')
        f.write(contents)
        f.close()
        return 

    def file_contents(self,filename):
        #opens a file (NOT a webpage, as in get_contents), reads the text of the file, assigns it to variable contents and returns contents
        f = open(filename, 'r')
        contents = f.read()
        f.close()
        return contents

    def product_details(self,contents):
        "takes the contents of a file and creates a dictionary with the string 'name' as key and the value as the name of the product"
        product_dict = {}    
        product_dict['name'] = self.get_product_name(contents) 
        product_dict['product_id'] = self.get_product_id(contents)
        product_dict['price'] = self.get_price(contents)
        product_dict['image'] = self.get_image(contents)
        product_dict['description'] = self.get_description(contents)
        return product_dict

    def product_details_to_db(self,product_dict):
        conn = MySQLdb.connect(host= "localhost",
                      user="root",
                      passwd = settings.db_password,
                      db="jewelryscraperdb")
        cursor = conn.cursor()
        cursor.execute (" SELECT * FROM products WHERE product_id = %s ", (product_dict['product_id']))
        rows = cursor.fetchall()
        if len(rows) == 0: 
            cursor.execute (" INSERT INTO products (product_name,product_id,price,image,description) VALUES (%s,%s,%s,%s,%s) ", (product_dict['name'],product_dict['product_id'],product_dict['price'],product_dict['image'], product_dict['description']))
