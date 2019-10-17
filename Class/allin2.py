import json
import requests
import sys
import os.path
import mysql.connector
from random import randint
from mysql.connector import errorcode

class User_interface:

    def __init__(self):
        self.category = ""
        self.product_type = ""

    def introduct(self):
        choice = ""

        print("\nWelcome to my program, please make a choice between : \n")
        while choice < "1" or choice > "2":
            choice = input("1 : Choose a category of product\n2 : Display saved products\n")
            if choice == "2":
                try:
                    mycursor.execute(f"SELECT * FROM SAVED")
                    myresult = mycursor.fetchall()
                    for row in myresult:
                        print("\n")
                        print("Name: ", row[2])
                        print("URL: ", row[3])
                        print("Description: ", row[4])
                        print("Store: ", row[5])
                except:
                    print("\nYou don't have saved product")

    def chosen_cat(self):
        category = self.category
        category_name = ""

        print("\n1 : Cheese\n2 : Meat\n3 : Fish\n4 : Chocolate\n5 : Drinks\n")
        while category < "1" or category > "5":
            category = input("Please, enter the number of the category : ")
        if category == "1":
            print("\n1 : Cow cheese \n2 : Goat cheese\n3 : Buffalo cheese\n")
            category_name = "Cheese"
        elif category =="2":
            print("\n1 : Beef\n2 : Porc\n3 : Poultry\n")
            category_name = "Meat"
        elif category == "3":
            print("\n1 : Salmon\n2 : Tuna\n3 : Sardine\n")
            category_name = "Fish"
        elif category == "4":
            print("\n1 : Black chocolate\n2 : Milk chocolate\n3 : White chocolate\n")
            category_name = "Chocolate"
        elif category == "5":
            print("\n1 : Iced-tea\n2 : Waters\n3 : Lemonades\n")
            category_name = "Drinks"
        return category, category_name
        
    def chosen_prod(self, category):
        product_type = self.product_type
        name = ""
        en_name = ""

        while product_type < "1" or product_type > "3":
            product_type = input("Veuillez entrer le chiffre correspondant à un produit : ")
        if category == "1" and product_type == "1":
            name = "Fromages_de_vache"
            en_name = "Cow cheese"
        elif category == "1" and product_type == "2":
            name = "Fromage_de_chèvre"
            en_name = "Goat cheese"
        elif category == "1" and product_type == "3":
            name = "Fromage_au_lait_de_bufflonne"
            en_name = "Buffalo cheese"
        elif category =="2" and product_type == "1":
            name = "Boeuf"
            en_name = "Beef"
        elif category =="2" and product_type == "2":
            name = "Porc"
            en_name = "Porc"
        elif category =="2" and product_type == "3":
            name = "Volailles"
            en_name = "Poultry"
        elif category =="3" and product_type == "1":
            name = "Saumon"
            en_name = "Salmon"
        elif category =="3" and product_type == "2":
            name = "Thon"
            en_name = "Tuna"
        elif category =="3" and product_type == "3":
            name = "Sardine"
            en_name = "Sardine"
        elif category =="4" and product_type == "1":
            name = "Chocolats_noirs"
            en_name = "Black chocolate"
        elif category =="4" and product_type == "2":
            name = "Chocolats_au_lait"
            en_name = "Milk chocolate"
        elif category =="4" and product_type == "3":
            name = "Chocolats_blancs"
            en_name = "White chocolate"
        elif category =="5" and product_type == "1":
            name = "Thés_glacés"
            en_name = "Ice-tea"
        elif category =="5" and product_type == "2":
            name = "Eaux"
            en_name = "Waters"
        elif category =="5" and product_type == "3":
            name = "Citronnades"
            en_name = "Lemonades"
        print(f"\nYou have chosen the product : {en_name}")
        product_type = int(product_type)
        category = int(category)
        return name, product_type, category

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
        #print(product_nb, product_gbl)
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
            #print(path) #indicate which JSON is loaded
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
        print(product_show)
        return names_list, codes_list, description_list, store_list, product_show

class Sql:

    def __init__(self, names_list, codes_list, description_list, store_list, product_show, name, category_name, category):
        self.names_list = names_list
        self.codes_list = codes_list
        self.description_list = description_list
        self.store_list = store_list
        self.product_show = product_show
        self.name = name
        self.category_name = category_name
        self.category = category

    def drop_table(self, mycursor):
        name = self.name

        restart = input("\nWrite Y, if you want to drop the table, else push enter : ")
        if restart == "Y":
            mycursor.execute(f"DROP TABLE PRODUCTS") #remise à zéro de la table
        else:
            pass

    def table_category(self, mycursor):
        names_list = self.names_list
        codes_list = self.codes_list
        description_list = self.description_list
        store_list = self.store_list
        product_show = self.product_show
        name = self.name
        category_name = self.category_name
        category = self.category

        x = 0 #increment for product lenght
        y = 0 #increment for lists
        try:
            mycursor.execute(f"CREATE TABLE IF NOT EXISTS CATEGORY (category_id INT AUTO_INCREMENT PRIMARY KEY, type INT(100), category TEXT(100000))")
            sql = f"INSERT INTO CATEGORY (type, category) VALUES (%s, %s)"
            val = [
            (f'{category}', f'Category : {category_name}'),
            ]
            mycursor.executemany(sql, val)
            mydb.commit()
            #print(mycursor.rowcount, "was inserted.") 
        except mysql.connector.errors.ProgrammingError:
            pass

    def table_product(self, mycursor):
        names_list = self.names_list
        codes_list = self.codes_list
        description_list = self.description_list
        store_list = self.store_list
        product_show = self.product_show
        name = self.name
        x = 0 #increment for product lenght
        y = 0 #increment for lists
        try: 
            mycursor.execute(f"CREATE TABLE PRODUCTS (product_id INT AUTO_INCREMENT PRIMARY KEY, type TEXT(1000000), name TEXT(1000000), url TEXT(100000), description TEXT(100000), lieux TEXT(100000))")
        except mysql.connector.errors.ProgrammingError:
            pass

        while x != product_show:
            sql = f"INSERT IGNORE INTO PRODUCTS (type, name, url, description, lieux) VALUES (%s, %s, %s, %s, %s)"
            val = [
            (f'{name}', f'{names_list[y]}', f'{codes_list[y]}', f'{description_list[y]}', f'{store_list[y]}'),
            ]
            x = x + 1
            y = y + 1
            mycursor.executemany(sql, val)
            mydb.commit()
            #print(mycursor.rowcount, "was inserted.") #indicate that row is inserted

    def show_product(self, mycursor):
        name = self.name
        product_show = self.product_show
        selected1 = []

        rdm_nb = randint(1, product_show)
        mycursor.execute(f"SELECT * FROM PRODUCTS where product_id = {rdm_nb}")
        selected1 = mycursor.fetchall()
        for row in selected1:
                print("\nName: ", row[2])
                print("URL: ", row[3])
                print("Description: ", row[4])
                print("Store: ", row[5])
        return selected1
    
    def alt_product(self, mycursor, selected1):
        selected2 = []
        save = input("\nWould you like to see a surrogate product ? Write Y, else press enter : ")
        rdm_nb = randint(1, product_show)
        while save == "Y" and selected1 != selected2:
            rdm_nb = randint(1, product_show)
            mycursor.execute(f"SELECT * FROM PRODUCTS WHERE product_id = {rdm_nb}")
            selected2 = mycursor.fetchall()
        for row in selected2:
                print("\nName: ", row[2])
                print("URL: ", row[3])
                print("Description: ", row[4])
                print("Store: ", row[5])
        return selected2

    def save_product(self, mycursor, selected2):
        save = input("\nWould you like to save the product in database ? Write Y, else press enter : ")
        if save == "Y":
            try:
                mycursor.execute(f"CREATE TABLE IF NOT EXISTS SAVED (id INT AUTO_INCREMENT PRIMARY KEY, product_id INT(255), type TEXT(1000000), name TEXT(1000000), url TEXT(100000), description TEXT(100000), lieux TEXT(100000))")
            except mysql.connector.errors.ProgrammingError:
                pass
        sql = f"INSERT IGNORE INTO SAVED (product_id, type, name, url, description, lieux) VALUES (%s, %s, %s, %s, %s, %s)"
        mycursor.executemany(sql, selected2)
        mydb.commit()
        print("Product saved in database in table SAVED\n")
    
    def display_saved(self, mycursor):
        save = input("Would you like to display saved products ?  Write Y, else press enter : ")
        if save == "Y" or save == "y":
            mycursor.execute(f"SELECT * FROM SAVED")
            saved = myresult = mycursor.fetchall()
            for row in saved:
                print("\n")
                print("Name: ", row[2])
                print("URL: ", row[3])
                print("Description: ", row[4])
                print("Store: ", row[5])
                print("\n")

mydb = mysql.connector.connect(
            host="localhost",
            user="testeur",
            passwd="testeur",
            database="test"
            )
mycursor = mydb.cursor()
mycursor.execute(f"DROP TABLE IF EXISTS PRODUCTS")
#mycursor.execute(f"DROP TABLE IF EXISTS SAVED")
User_interface().introduct()
category, category_name = User_interface().chosen_cat()
name, product_type, category = User_interface().chosen_prod(category)
#name = Input_user().entry_user()
product_nb, product_gbl, product_dict = Searching(name).first_search()
pages = Calc(product_nb, product_gbl).calc_pages()
global_dict = Searching(name).global_search(pages)
global_dict.update(product_dict)
names_list, codes_list, description_list, store_list, product_show = Listing(product_nb, pages, name).listing()
#Sql(names_list, codes_list, description_list, store_list, product_show, name, category_name, category).drop_table(mycursor)
#mycursor = Sql(names_list, codes_list, description_list, store_list, product_show, name).connect()
Sql(names_list, codes_list, description_list, store_list, product_show, name, category_name, category).table_category(mycursor)
Sql(names_list, codes_list, description_list, store_list, product_show, name, category_name, category).table_product(mycursor)
selected1 = Sql(names_list, codes_list, description_list, store_list, product_show, name, category_name, category).show_product(mycursor)
selected2 = Sql(names_list, codes_list, description_list, store_list, product_show, name, category_name, category).alt_product(mycursor, selected1)
Sql(names_list, codes_list, description_list, store_list, product_show, name, category_name, category).save_product(mycursor, selected2)
Sql(names_list, codes_list, description_list, store_list, product_show, name, category_name, category).display_saved(mycursor)

