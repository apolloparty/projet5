import mysql.connector
from random import randint
from mysql.connector import errorcode

class User_interface:

    def __init__(self, mycursor):
        self.category = ""
        self.product_type = ""
        self.mycursor = mycursor

    def introduct(self):
        mycursor = self.mycursor
        choice = ""

        print("\nWelcome to my program, please make a choice between : ")
        while choice < "1" or choice > "3":
            choice = input("\
                \n1 : Food you would like to surrogate\
                \n2 : Display saved products\
                \n3 : Refresh table product\n")
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
                    print("\nYou don't saved any product")
            elif choice == "3":
                reboot = input("\
                    Are you sure to erase table product ?\n\
                    This action could take many minutes depending on product : \
                    Press 1, else press enter : ")
                return reboot

    def chosen_cat(self):
        category = self.category
        category_name = ""

        print("\
            \n1 : Cheese\
            \n2 : Meat\
            \n3 : Fish\
            \n4 : Chocolate\
            \n5 : Drinks\n")
        while category < "1" or category > "5":
            category = input("Please, enter the number of the category : ")
        if category == "1":
            print("\
                \n1 : Cow cheese\
                \n2 : Goat cheese\
                \n3 : Buffalo cheese\n")
            category_name = "Cheese"
        elif category =="2":
            print("\
                \n1 : Beef\
                \n2 : Porc\
                \n3 : Poultry\n")
            category_name = "Meat"
        elif category == "3":
            print("\
                \n1 : Salmon\
                \n2 : Tuna\
                \n3 : Sardine\n")
            category_name = "Fish"
        elif category == "4":
            print("\
                \n1 : Black chocolate\
                \n2 : Milk chocolate\
                \n3 : White chocolate\n")
            category_name = "Chocolate"
        elif category == "5":
            print("\
                \n1 : Iced-tea\
                \n2 : Waters\
                \n3 : Lemonades\n")
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