import json
import requests
import sys
import os.path

class Input_user:

    def __init__(self):
        self.name = ""

    def entry_user(self):
        name = input("Entrez le nom du produit recherché : ")
        return name

class Searching():

    def __init__(self, name):
        self.name = name

    def first_search(self):
        name = self.name
        url = f"https://fr-en.openfoodfacts.org/category/{name}/1.json"
        req = requests.get(url)
        product_dict = json.loads(req.content.decode('UTF-8'))
        #indent = json.dumps(product_dict, indent = 4) #permit indentation of JSON
        product_nb = int(product_dict['page_size']) #products number by pages
        product_gbl = product_dict['count'] #products number globals
        print(product_nb, product_gbl)
        return product_nb, product_gbl, product_dict

    def global_search(self, pages):
        global_dict = {}
        name = self.name
        x = 1
        y = 1 #page number of JSON extracted
        os.mkdir(f'/home/fostin/delivery/pythonorienté/projet5/Class/{name}') #make a new directory for the product
        print(pages)
        while x <= pages:
            url = f"https://fr-en.openfoodfacts.org/category/{name}/{x}.json"
            req = requests.get(url)
            dictmp = json.loads(req.content.decode('UTF-8'))
            global_dict.update(dictmp)
            json.dumps(global_dict)
            completeName = os.path.join(f'/home/fostin/delivery/pythonorienté/projet5/Class/{name}', f"{name}{y}.json")
            f = open(completeName, "w")
            f.write(json.dumps(global_dict))
            f.close()
            x = x + 1
            y = y + 1
            print(x)
        return global_dict

class Calc:

    def __init__(self, product_nb, product_gbl):
        self.product_nb = product_nb
        self.product_gbl = product_gbl 

    def calc_pages(self):
        product_nb = self.product_nb
        product_gbl = self.product_gbl
        pages = product_gbl/product_nb

        if pages == 0:
            print("Wrong product")
            sys.exit()
        if pages != int(pages):
            pages = int(pages) + 1
        print(pages)
        return pages

class Listing:

    def __init__(self, product_nb, pages, name):
        self.product_nb = product_nb
        self.pages = pages
        self.name = name

    def listing(self):
        product_nb = self.product_nb
        pages = self.pages
        name = self.name
        x = 0
        y = 1
        codes_list = []
        names_list = []
        description_list = []
        store_list = []
        while y <= pages:
            path = f"/home/fostin/delivery/pythonorienté/projet5/Class/{name}/{name}{y}.json"
            print(path)
            with open(path) as js_loaded:
                dictmp = json.load(js_loaded)
                while x != product_nb:
                    try:
                        codes = dictmp['products'][x]['code']
                        codes_list.append(codes)
                    except KeyError:
                        codes = "UNKNOW CODE"
                    except IndexError:
                        pass
                    try:
                        names = dictmp['products'][x]['product_name']
                        names_list.append(names)
                    except KeyError:
                        names = "UNKNOW NAME"
                    except IndexError:
                        pass    
                    try:
                        description = dictmp['products'][x]['categories']
                        description_list.append(description)
                    except KeyError:
                        description = "UNKNOW DESCRIPTION"
                    except IndexError:
                        pass            
                    try:
                        store = dictmp['products'][x]['stores']
                        store_list.append(store)
                    except KeyError:
                        store = "UNKNOW STORE"
                    except IndexError:
                        pass                 
                    x = x + 1
                x = 0
                y = y + 1
        print(codes_list, names_list, description_list, store_list)

name = Input_user().entry_user()
product_nb, product_gbl, product_dict = Searching(name).first_search()
pages = Calc(product_nb, product_gbl).calc_pages()
#global_dict = Searching(name).global_search(pages)
#global_dict.update(product_dict)
Listing(product_nb, pages, name).listing()