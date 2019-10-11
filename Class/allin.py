import json
import requests
import sys
import os.path
import mysql.connector
from random import randint
from mysql.connector import errorcode

class User_interface:

    def __init__(self):
        self.entry = ""
        self.entry2 = ""

    def category(self):
        entry = self.entry
        entry2 = self.entry2

        print("\n1 = Fromages, 2 = Viandes, 3 = Poissons, 4 = Chocolats, 5 = Boissons")
        while entry < "1" or entry > "5":
            entry = input("Veuillez entrer le chiffre correspondant à une catégorie de produit : ")
        if entry == "1":
            print("\n1 = Fromages de vache, 2 = Fromages de chèvre, 3 = Fromage de bufflone")
        elif entry =="2":
            print("\n1 = Boeuf, 2 = Porc, 3 = Volailles")
        elif entry == "3":
            print("\n1 = Saumon, 2 = Thon, 3 = Sardine")
        elif entry == "4":
            print("\n1 = Chocolats noirs, 2 = Chocolats au lait, 3 = Chocolats blancs")
        elif entry == "5":
            print("\n1 = Thés glacés, 2 = Eaux, 3 = Citronnades")
        while entry2 < "1" or entry2 > "3":
            entry2 = input("Veuillez entrer le chiffre correspondant à un produit : ")
        if entry == "1" and entry2 == "1":
            name = "Fromages_de_vache"
        elif entry == "1" and entry2 == "2":
            name = "Fromage_de_chèvre"
        elif entry == "1" and entry2 == "3":
            name = "Fromage_au_lait_de_bufflonne"
        elif entry =="2" and entry2 == "1":
            name = "Boeuf"
        elif entry =="2" and entry2 == "2":
            name = "Porc"
        elif entry =="2" and entry2 == "3":
            name = "Volailles"
        elif entry =="3" and entry2 == "1":
            name = "Saumon"
        elif entry =="3" and entry2 == "2":
            name = "Thon"
        elif entry =="3" and entry2 == "3":
            name = "Sardine"
        elif entry =="4" and entry2 == "1":
            name = "Chocolats_noirs"
        elif entry =="4" and entry2 == "2":
            name = "Chocolats_au_lait"
        elif entry =="4" and entry2 == "3":
            name = "Chocolats_blancs"
        elif entry =="5" and entry2 == "1":
            name = "Thés_glacés"
        elif entry =="5" and entry2 == "2":
            name = "Eaux"
        elif entry =="5" and entry2 == "3":
            name = "Citronnades"
        print(name)
        return name

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
        try:
            os.mkdir(f'/home/fostin/delivery/pythonorienté/projet5/Class/{name}') #make a new directory for the product
        except FileExistsError:
            return global_dict
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
        return names_list, codes_list, description_list, store_list, product_show

class Sql:

    def __init__(self, names_list, codes_list, description_list, store_list, product_show, name):
        self.names_list = names_list
        self.codes_list = codes_list
        self.description_list = description_list
        self.store_list = store_list
        self.product_show = product_show
        self.name = name

    def connect(self):
        names_list = self.names_list
        codes_list = self.codes_list
        description_list = self.description_list
        store_list = self.store_list
        product_show = self.product_show
        name = self.name

        #print(len(store_list))
        #product = input("Entrez le nom : ") #variable test
        x = 0 #incrementation for product lenght
        y = 0 #increment for lists
        mydb = mysql.connector.connect(
            host="localhost",
            user="testeur",
            passwd="XXX",
            database="test"
            )
        mycursor = mydb.cursor()

        try:
            mycursor.execute(f"CREATE TABLE {name} (id INT AUTO_INCREMENT PRIMARY KEY, nom TEXT(1000000), code TEXT(100000), description TEXT(100000), lieux TEXT(100000))")
            while x != product_show:
                sql = f"INSERT INTO {name} (nom, code, description, lieux) VALUES (%s, %s, %s, %s)"
                val = [
                (f'Nom : {names_list[y]}', f'URL : {codes_list[y]}', f'Description : {description_list[y]}', f'Magasin : {store_list[y]}'),
                ]
                x = x + 1
                y = y + 1
                mycursor.executemany(sql, val)
                mydb.commit()
                #print(mycursor.rowcount, "was inserted.") 
        except mysql.connector.errors.ProgrammingError:
            pass

        rdm_nb = randint(1, product_show)
        print(rdm_nb)

        restart = input("Write Y, if you want to drop the table, else push enter : ")
        if restart == "Y":
            mycursor.execute(f"DROP TABLE {name}") #remise à zéro de la table
        else:
            pass

        selected1 = ""
        selected2 = ""
        selected1 = mycursor.execute(f"SELECT * FROM {name} WHERE id = {rdm_nb}")
        myresult = mycursor.fetchall()
        for x in myresult:
            print(x, "\n")
        save = input("Would you like to see a surrogate product ? Write Y, else press enter : ")
        while save == "Y" and selected1 != selected2:
            rdm_nb = randint(1, product_show)
            selected2 = mycursor.execute(f"SELECT * FROM {name} WHERE id = {rdm_nb}")
            myresult = mycursor.fetchall()
            for x in myresult:
                print(x, "\n")

        save = input("Would you like to save the product in database ? Write Y, else press enter : ")
        if save == "Y":
            mycursor.execute(f"CREATE TABLE IF NOT EXISTS SAVED (id INT AUTO_INCREMENT PRIMARY KEY, nom TEXT(1000000), code TEXT(100000), description TEXT(100000), lieux TEXT(100000))")
            sql = f"INSERT INTO SAVED (nom, code, description, lieux) VALUES (%s, %s, %s, %s)"
            mycursor.executemany(sql, selected2)
            mydb.commit()
            print("Product saved in database in table SAVED")

        #print(len(store_list))

name = User_interface().category()
#name = Input_user().entry_user()
product_nb, product_gbl, product_dict = Searching(name).first_search()
pages = Calc(product_nb, product_gbl).calc_pages()
global_dict = Searching(name).global_search(pages)
global_dict.update(product_dict)
names_list, codes_list, description_list, store_list, product_show = Listing(product_nb, pages, name).listing()
Sql(names_list, codes_list, description_list, store_list, product_show, name).connect()