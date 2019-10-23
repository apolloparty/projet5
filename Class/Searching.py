import requests
import json
import sys
import os.path


class Searching():

    def __init__(self, name):
        self.name = name

    def first_search(self):
        name = self.name
        url = f"https://fr-en.openfoodfacts.org/category/{name}/1.json"
        req = requests.get(url)
        product_dict = json.loads(req.content.decode('UTF-8'))
        # indent = json.dumps(product_dict, indent = 4)
        #  # permit indentation of JSON
        product_nb = int(product_dict['page_size'])  # products number by pages
        product_gbl = product_dict['count']  # products number globals
        # print(product_nb, product_gbl)
        return product_nb, product_gbl, product_dict

    def global_search(self, pages):
        global_dict = {}
        name = self.name
        x = 1
        y = 1  # page number of JSON extracted
        try:
            os.mkdir(f'/home/fostin/delivery/pythonorienté/projet5/Ressources/\
                {name}')  # make a new directory for the product
        except FileExistsError:
            return global_dict
        print(pages)
        while x <= pages:
            url = f"https://fr-en.openfoodfacts.org/category/{name}/{x}.json"
            req = requests.get(url)
            dictmp = json.loads(req.content.decode('UTF-8'))
            global_dict.update(dictmp)
            json.dumps(global_dict)
            completeName = \
                os.path.join(f'/home/fostin/delivery/pythonorienté/projet5/Ressources/\
                    {name}', f"{name}{y}.json")
            f = open(completeName, "w")
            f.write(json.dumps(global_dict))
            f.close()
            x = x + 1
            y = y + 1
            print(x)
        return global_dict
