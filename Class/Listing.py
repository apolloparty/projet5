import json
import requests
import sys
import os.path


class Listing:

    def __init__(self, product_nb, pages, name):
        self.product_nb = product_nb
        self.pages = pages
        self.name = name

    def listing(self):
        """Extract JSON from ressources path

        Create four list with url, name
        description and store of the product
        """
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
            path = f"projet5/Ressources/{name}/{name}{y}.json"
            # print(path) #indicate which JSON is loaded
            with open(path) as js_loaded:
                dictmp = json.load(js_loaded)
                while x != product_nb:
                    try:
                        codes = dictmp['products'][x]['url']
                        if codes == "":
                            codes = "UNKNOW URL"
                        codes_list.append(codes)
                    except KeyError:
                        codes = "UNKNOW URL"
                        codes_list.append(codes)
                    except IndexError:
                        pass
                    try:
                        names = dictmp['products'][x]['product_name']
                        if names == "":
                            names = "UNKNOW NAME"
                        names_list.append(names)
                    except KeyError:
                        names = "UNKNOW NAME"
                        names_list.append(names)
                    except IndexError:
                        pass
                    try:
                        description = dictmp['products'][x]['categories']
                        if description == "":
                            description = "UNKNOW DESCRIPTION"
                        description_list.append(description)
                    except KeyError:
                        description = "UNKNOW DESCRIPTION"
                        description_list.append(description)
                    except IndexError:
                        pass
                    try:
                        store = dictmp['products'][x]['stores']
                        if store == "":
                            store = "UNKNOW NAME"
                        store_list.append(store)
                    except KeyError:
                        store = "UNKNOW STORE"
                        store_list.append(store)
                    except IndexError:
                        pass
                    x = x + 1
                x = 0
                y = y + 1
        product_show = len(names_list)
        # print(product_show)
        return names_list, codes_list, description_list, \
            store_list, product_show
